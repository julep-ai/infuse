from datetime import timedelta

from temporalio import workflow
from temporalio.exceptions import ApplicationError

from ...activities import task_steps
from ...autogen.openapi_model import (
    CreateTransitionRequest,
    Transition,
    TransitionTarget,
)
from ...common.protocol.tasks import PartialTransition, StepContext
from ...common.retry_policies import DEFAULT_RETRY_POLICY


async def transition(
    context: StepContext, state: PartialTransition | None = None, **kwargs
) -> Transition:
    if state is None:
        state = PartialTransition()

    match context.is_last_step, context.cursor:
        case (True, TransitionTarget(workflow="main")):
            state.type = "finish"
        case (True, _):
            state.type = "finish_branch"
        case _, _:
            state.type = "step"

    transition_request = CreateTransitionRequest(
        current=context.cursor,
        **{
            "next": None
            if context.is_last_step
            else TransitionTarget(
                workflow=context.cursor.workflow, step=context.cursor.step + 1
            ),
            "metadata": {"step_type": type(context.current_step).__name__},
            "output": state.output,
            **state.model_dump(exclude_unset=True, exclude={"output"}),
            **kwargs,  # Override with any additional kwargs
        },
    )

    try:
        return await workflow.execute_activity(
            task_steps.transition_step,
            args=[context, transition_request],
            schedule_to_close_timeout=timedelta(seconds=30),
            retry_policy=DEFAULT_RETRY_POLICY,
        )

    except Exception as e:
        workflow.logger.error(f"Error in transition: {str(e)}")
        raise ApplicationError(f"Error in transition: {e}") from e
