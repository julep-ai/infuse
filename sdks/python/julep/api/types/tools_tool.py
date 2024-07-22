# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .common_identifier_safe_unicode import CommonIdentifierSafeUnicode
from .common_uuid import CommonUuid
from .common_valid_python_identifier import CommonValidPythonIdentifier
from .tools_function_def import ToolsFunctionDef


class Base(pydantic_v1.BaseModel):
    name: CommonValidPythonIdentifier = pydantic_v1.Field()
    """
    Name of the tool (must be unique for this agent and a valid python identifier string )
    """

    function: typing.Optional[ToolsFunctionDef] = None
    integration: typing.Any
    system: typing.Any
    api_call: typing.Any
    created_at: dt.datetime = pydantic_v1.Field()
    """
    When this resource was created as UTC date-time
    """

    updated_at: dt.datetime = pydantic_v1.Field()
    """
    When this resource was updated as UTC date-time
    """

    id: CommonUuid

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


class ToolsTool_Function(Base):
    background: bool
    function: ToolsFunctionDef
    type: typing.Literal["function"] = "function"

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
        allow_population_by_field_name = True
        populate_by_name = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


ToolsTool = ToolsTool_Function
