#!/usr/bin/env python3


from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from ..activities.truncation import truncation
    from ..common.retry_policies import DEFAULT_RETRY_POLICY
    from ..env import temporal_heartbeat_timeout, temporal_schedule_to_close_timeout


@workflow.defn
class TruncationWorkflow:
    @workflow.run
    async def run(self, session_id: str, token_count_threshold: int) -> None:
        return await workflow.execute_activity(
            truncation,
            args=[session_id, token_count_threshold],
            schedule_to_close_timeout=timedelta(
                seconds=temporal_schedule_to_close_timeout
            ),
            retry_policy=DEFAULT_RETRY_POLICY,
            heartbeat_timeout=timedelta(seconds=temporal_heartbeat_timeout),
        )
