from typing import Any, TypeVar
from uuid import UUID

from beartype import beartype
from fastapi import HTTPException
from pycozo.client import QueryException
from pydantic import ValidationError

from ...autogen.openapi_model import Execution
from ..utils import (
    cozo_query,
    partialclass,
    rewrap_exceptions,
    wrap_in_class,
)
from .constants import OUTPUT_UNNEST_KEY

ModelT = TypeVar("ModelT", bound=Any)
T = TypeVar("T")


@rewrap_exceptions(
    {
        AssertionError: partialclass(HTTPException, status_code=404),
        QueryException: partialclass(HTTPException, status_code=400),
        ValidationError: partialclass(HTTPException, status_code=400),
        TypeError: partialclass(HTTPException, status_code=400),
    }
)
@wrap_in_class(
    Execution,
    one=True,
    transform=lambda d: {
        **d,
        "output": d["output"][OUTPUT_UNNEST_KEY]
        if OUTPUT_UNNEST_KEY in d["output"]
        else d["output"],
    },
)
@cozo_query
@beartype
def get_execution(
    *,
    execution_id: UUID,
) -> tuple[str, dict]:
    # Executions are allowed direct GET access if they have execution_id

    # NOTE: Do not remove outer curly braces
    query = """
    {
      input[execution_id] <- [[to_uuid($execution_id)]]

      ?[id, task_id, status, input, output, error, session_id, metadata, created_at, updated_at] := 
          input[execution_id],
          *executions {
              task_id,
              execution_id,
              status,
              input,
              output,
              error,
              session_id,
              metadata,
              created_at,
              updated_at,
          },
          id = execution_id

      :limit 1
    }
    """

    return (
        query,
        {
            "execution_id": str(execution_id),
        },
    )
