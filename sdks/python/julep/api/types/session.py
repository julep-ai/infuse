# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .session_metadata import SessionMetadata

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Session(pydantic.BaseModel):
    id: str = pydantic.Field(description="Session id (UUID)")
    user_id: typing.Optional[str] = pydantic.Field(
        description="User ID of user associated with this session"
    )
    agent_id: str = pydantic.Field(
        description="Agent ID of agent associated with this session"
    )
    situation: typing.Optional[str] = pydantic.Field(
        description="A specific situation that sets the background for this session"
    )
    summary: typing.Optional[str] = pydantic.Field(
        description="(null at the beginning) - generated automatically after every interaction"
    )
    created_at: typing.Optional[dt.datetime] = pydantic.Field(
        description="Session created at (RFC-3339 format)"
    )
    updated_at: typing.Optional[dt.datetime] = pydantic.Field(
        description="Session updated at (RFC-3339 format)"
    )
    metadata: typing.Optional[SessionMetadata] = pydantic.Field(
        description="Optional metadata"
    )
    render_templates: typing.Optional[bool] = pydantic.Field(
        description="Render system and assistant message content as jinja templates"
    )
    token_budget: typing.Optional[int] = pydantic.Field(
        description="Threshold value for the adaptive context functionality"
    )
    context_overflow: typing.Optional[str] = pydantic.Field(
        description="Action to start on context window overflow"
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
