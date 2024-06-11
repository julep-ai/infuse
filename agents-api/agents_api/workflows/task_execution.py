#!/usr/bin/env python3


from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():

    from ..activities.task_steps import (
        prompt_step,
        evaluate_step,
        yield_step,
        tool_call_step,
        error_step,
        if_else_step,
        transition_step,
    )

    from ..common.protocol.tasks import (
        ExecutionInput,
        PromptWorkflowStep,
        EvaluateWorkflowStep,
        YieldWorkflowStep,
        ToolCallWorkflowStep,
        ErrorWorkflowStep,
        IfElseWorkflowStep,
        StepContext,
    )


@workflow.defn
class TaskExecutionWorkflow:
    @workflow.run
    async def run(
        self,
        execution_input: ExecutionInput,
        start: tuple[str, int] = ("main", 0),
        previous_inputs: list[dict] = [],
    ) -> None:
        wf_name, step_idx = start
        spec = execution_input.task.spec
        workflow_map = {wf.name: wf.steps for wf in spec.workflows}
        current_workflow = workflow_map[wf_name]
        previous_inputs = previous_inputs or [execution_input.arguments]
        step = current_workflow[step_idx]

        context = StepContext(
            # execution=execution_input.execution,
            task=execution_input.task,
            # agent=execution_input.agent,
            # user=execution_input.user,
            # session=execution_input.session,
            # tools=execution_input.tools,
            arguments=execution_input.arguments,
            definition=step,
            inputs=previous_inputs,
        )

        # Run the step
        match step:
            case PromptWorkflowStep():
                result = await workflow.execute_activity(
                    prompt_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )
            case EvaluateWorkflowStep():
                result = await workflow.execute_activity(
                    evaluate_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )
            case YieldWorkflowStep():
                result = await workflow.execute_activity(
                    yield_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )
            case ToolCallWorkflowStep():
                result = await workflow.execute_activity(
                    tool_call_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )
            case ErrorWorkflowStep():
                result = await workflow.execute_activity(
                    error_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )
            case IfElseWorkflowStep():
                result = await workflow.execute_activity(
                    if_else_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )

        # Transition to the next step
        await workflow.execute_activity(
            transition_step,
            args=[
                context,
                start,
                result,
            ],
            schedule_to_close_timeout=timedelta(seconds=600),
        )

        # FIXME: this is just a demo, we should handle the end of the workflow properly
        # -----

        # End if the last step
        if step_idx + 1 == len(current_workflow):
            return result

        # Recurse to the next step
        workflow.continue_as_new(
            execution_input, (wf_name, step_idx + 1), previous_inputs + [result]
        )
