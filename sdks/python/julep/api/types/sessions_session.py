# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

import typing_extensions

from ..core.datetime_utils import serialize_datetime
from .common_uuid import CommonUuid
from .sessions_multi_agent_multi_user_session import SessionsMultiAgentMultiUserSession
from .sessions_multi_agent_no_user_session import SessionsMultiAgentNoUserSession
from .sessions_multi_agent_single_user_session import (
    SessionsMultiAgentSingleUserSession,
)
from .sessions_single_agent_multi_user_session import (
    SessionsSingleAgentMultiUserSession,
)
from .sessions_single_agent_no_user_session import SessionsSingleAgentNoUserSession
from .sessions_single_agent_single_user_session import (
    SessionsSingleAgentSingleUserSession,
)

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Base(pydantic.BaseModel):
    situation: str = pydantic.Field(
        description="A specific situation that sets the background for this session"
    )
    summary: typing.Optional[str] = pydantic.Field(
        description="Summary (null at the beginning) - generated automatically after every interaction"
    )
    render_templates: bool = pydantic.Field(
        description="Render system and assistant message content as jinja templates"
    )
    token_budget: typing.Optional[int] = pydantic.Field(
        description="Threshold value for the adaptive context functionality"
    )
    context_overflow: typing.Optional[str] = pydantic.Field(
        description="Action to start on context window overflow"
    )
    id: CommonUuid
    metadata: typing.Optional[typing.Dict[str, typing.Any]]
    created_at: dt.datetime = pydantic.Field(
        description="When this resource was created as UTC date-time"
    )
    updated_at: dt.datetime = pydantic.Field(
        description="When this resource was updated as UTC date-time"
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


class SessionsSession_SingleAgentNoUser(SessionsSingleAgentNoUserSession, Base):
    kind: typing_extensions.Literal["single_agent_no_user"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class SessionsSession_SingleAgentSingleUser(SessionsSingleAgentSingleUserSession, Base):
    kind: typing_extensions.Literal["single_agent_single_user"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class SessionsSession_SingleAgentMultiUser(SessionsSingleAgentMultiUserSession, Base):
    kind: typing_extensions.Literal["single_agent_multi_user"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class SessionsSession_MultiAgentNoUser(SessionsMultiAgentNoUserSession, Base):
    kind: typing_extensions.Literal["multi_agent_no_user"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class SessionsSession_MultiAgentSingleUser(SessionsMultiAgentSingleUserSession, Base):
    kind: typing_extensions.Literal["multi_agent_single_user"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class SessionsSession_MultiAgentMultiUser(SessionsMultiAgentMultiUserSession, Base):
    kind: typing_extensions.Literal["multi_agent_multi_user"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


SessionsSession = typing.Union[
    SessionsSession_SingleAgentNoUser,
    SessionsSession_SingleAgentSingleUser,
    SessionsSession_SingleAgentMultiUser,
    SessionsSession_MultiAgentNoUser,
    SessionsSession_MultiAgentSingleUser,
    SessionsSession_MultiAgentMultiUser,
]
