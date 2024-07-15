# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .common_uuid import CommonUuid
from .entries_chat_ml_role import EntriesChatMlRole
from .entries_entry_content import EntriesEntryContent
from .entries_entry_source import EntriesEntrySource

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class EntriesEntry(pydantic.BaseModel):
    role: EntriesChatMlRole
    name: typing.Optional[str]
    content: EntriesEntryContent
    source: EntriesEntrySource
    timestamp: int = pydantic.Field(
        description="This is the time that this event refers to."
    )
    created_at: dt.datetime = pydantic.Field(
        description="When this resource was created as UTC date-time"
    )
    id: CommonUuid

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
