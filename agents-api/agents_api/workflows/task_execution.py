#!/usr/bin/env python3


from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from ..activities.task_steps import (
        if_else_step,
        prompt_step,
        transition_step,
    )
    from ..common.protocol.tasks import (
        ExecutionInput,
        # ToolCallWorkflowStep,
        # ErrorWorkflowStep,
        IfElseWorkflowStep,
        PromptWorkflowStep,
        StepContext,
        TransitionInfo,
        # EvaluateWorkflowStep,
        YieldWorkflowStep,
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
            developer_id=execution_input.developer_id,
            execution=execution_input.execution,
            task=execution_input.task,
            agent=execution_input.agent,
            user=execution_input.user,
            session=execution_input.session,
            tools=execution_input.tools,
            arguments=execution_input.arguments,
            definition=step,
            inputs=previous_inputs,
        )

        should_wait = False
        # Run the step
        match step:
            case PromptWorkflowStep():
                outputs = await workflow.execute_activity(
                    prompt_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )

                # TODO: ChatCompletion does not have tool_calls
                # if outputs.tool_calls is not None:
                #     should_wait = True

            # case EvaluateWorkflowStep():
            #     result = await workflow.execute_activity(
            #         evaluate_step,
            #         context,
            #         schedule_to_close_timeout=timedelta(seconds=600),
            #     )
            case YieldWorkflowStep():
                outputs = await workflow.execute_child_workflow(
                    TaskExecutionWorkflow.run,
                    args=[execution_input, (step.workflow, 0), previous_inputs],
                )
            # case ToolCallWorkflowStep():
            #     outputs = await workflow.execute_activity(
            #         tool_call_step,
            #         context,
            #         schedule_to_close_timeout=timedelta(seconds=600),
            #     )
            # case ErrorWorkflowStep():
            #     result = await workflow.execute_activity(
            #         error_step,
            #         context,
            #         schedule_to_close_timeout=timedelta(seconds=600),
            #     )
            case IfElseWorkflowStep():
                outputs = await workflow.execute_activity(
                    if_else_step,
                    context,
                    schedule_to_close_timeout=timedelta(seconds=600),
                )
                workflow_step = YieldWorkflowStep(**outputs["goto_workflow"])

                outputs = await workflow.execute_child_workflow(
                    TaskExecutionWorkflow.run,
                    args=[
                        execution_input,
                        (workflow_step.workflow, 0),
                        previous_inputs,
                    ],
                )

        is_last = step_idx + 1 == len(current_workflow)
        # Transition type
        transition_type = (
            "awaiting_input" if should_wait else ("finish" if is_last else "step")
        )

        # Transition to the next step
        transition_info = TransitionInfo(
            from_=(wf_name, step_idx),
            to=None if (is_last or should_wait) else (wf_name, step_idx + 1),
            type=transition_type,
        )

        await workflow.execute_activity(
            transition_step,
            args=[
                context,
                transition_info,
            ],
            schedule_to_close_timeout=timedelta(seconds=600),
        )

        # FIXME: this is just a demo, we should handle the end of the workflow properly
        # -----

        # End if the last step
        if is_last:
            return outputs

        # Otherwise, recurse to the next step
        workflow.continue_as_new(
            execution_input, (wf_name, step_idx + 1), previous_inputs + [outputs]
        )
