import ast
from typing import Any

import simpleeval
from beartype import beartype
from box import Box
from openai import BaseModel

# Increase the max string length to 2048000
simpleeval.MAX_STRING_LENGTH = 2048000

from simpleeval import NameNotDefined, SimpleEval
from temporalio import activity
from thefuzz import fuzz

from ..utils import get_evaluator


class EvaluateError(Exception):
    def __init__(self, error, expression, values):
        error_message = error.message if hasattr(error, "message") else str(error)
        message = error_message

        # Catch a possible jinja template error
        if "unhashable" in error_message and "{{" in expression:
            message += "\nSuggestion: It seems like you used a jinja template, did you mean to use a python expression?"

        # Catch a possible misspell in a variable name
        if isinstance(error, NameNotDefined):
            misspelledName = error_message.split("'")[1]
            for variableName in values:
                if fuzz.ratio(variableName, misspelledName) >= 90.0:
                    message += f"\nDid you mean '{variableName}' instead of '{misspelledName}'?"
        super().__init__(message)


# Recursive evaluation helper function
def _recursive_evaluate(expr, evaluator: SimpleEval):
    if isinstance(expr, str):
        try:
            return evaluator.eval(expr)
        except Exception as e:
            if activity.in_activity():
                evaluate_error = EvaluateError(e, expr, evaluator.names)
                activity.logger.error(f"Error in base_evaluate: {evaluate_error}\n")
            raise evaluate_error from e
    elif isinstance(expr, list):
        return [_recursive_evaluate(e, evaluator) for e in expr]
    elif isinstance(expr, dict):
        return {k: _recursive_evaluate(v, evaluator) for k, v in expr.items()}
    else:
        msg = f"Invalid expression: {expr}"
        raise ValueError(msg)


@activity.defn
@beartype
async def base_evaluate(
    exprs: Any,
    values: dict[str, Any] = {},
    extra_lambda_strs: dict[str, str] | None = None,
) -> Any | list[Any] | dict[str, Any]:
    input_len = 1 if isinstance(exprs, str) else len(exprs)
    assert input_len > 0, "exprs must be a non-empty string, list or dict"

    extra_lambdas = {}
    if extra_lambda_strs:
        for k, v in extra_lambda_strs.items():
            v = v.strip()

            # Check that all extra lambdas are valid
            assert v.startswith("lambda "), "All extra lambdas must start with 'lambda'"

            try:
                ast.parse(v)
            except Exception as e:
                msg = f"Invalid lambda: {v}"
                raise ValueError(msg) from e

            # Eval the lambda and add it to the extra lambdas
            extra_lambdas[k] = eval(v)

    # Turn the nested dict values from pydantic to dicts where possible
    values = {k: v.model_dump() if isinstance(v, BaseModel) else v for k, v in values.items()}

    # frozen_box doesn't work coz we need some mutability in the values
    values = Box(values, frozen_box=False, conversion_box=True)

    evaluator: SimpleEval = get_evaluator(names=values, extra_functions=extra_lambdas)

    # Recursively evaluate the expression
    return _recursive_evaluate(exprs, evaluator)
