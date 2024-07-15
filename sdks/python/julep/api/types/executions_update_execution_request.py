# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .executions_resume_execution_request import ExecutionsResumeExecutionRequest
from .executions_stop_execution_request import ExecutionsStopExecutionRequest


class ExecutionsUpdateExecutionRequest_Cancelled(ExecutionsStopExecutionRequest):
    status: typing_extensions.Literal["cancelled"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ExecutionsUpdateExecutionRequest_Running(ExecutionsResumeExecutionRequest):
    status: typing_extensions.Literal["running"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


ExecutionsUpdateExecutionRequest = typing.Union[
    ExecutionsUpdateExecutionRequest_Cancelled, ExecutionsUpdateExecutionRequest_Running
]
