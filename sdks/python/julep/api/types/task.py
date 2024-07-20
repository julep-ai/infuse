# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .common_uuid import CommonUuid
from .tasks_workflow_step import TasksWorkflowStep
from .tools_create_tool_request import ToolsCreateToolRequest


class Task(pydantic_v1.BaseModel):
    """
    Object describing a Task
    """

    name: str
    description: str
    main: typing.List[TasksWorkflowStep] = pydantic_v1.Field()
    """
    The entrypoint of the task.
    """

    input_schema: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(
        default=None
    )
    """
    The schema for the input to the task. `null` means all inputs are valid.
    """

    tools: typing.List[ToolsCreateToolRequest] = pydantic_v1.Field()
    """
    Tools defined specifically for this task not included in the Agent itself.
    """

    inherit_tools: bool = pydantic_v1.Field()
    """
    Whether to inherit tools from the parent agent or not. Defaults to true.
    """

    agent_id: CommonUuid
    id: CommonUuid
    created_at: dt.datetime = pydantic_v1.Field()
    """
    When this resource was created as UTC date-time
    """

    updated_at: dt.datetime = pydantic_v1.Field()
    """
    When this resource was updated as UTC date-time
    """

    metadata: typing.Optional[typing.Dict[str, typing.Any]] = None

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        kwargs_with_defaults_exclude_none: typing.Any = {
            "by_alias": True,
            "exclude_none": True,
            **kwargs,
        }

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset),
            super().dict(**kwargs_with_defaults_exclude_none),
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
