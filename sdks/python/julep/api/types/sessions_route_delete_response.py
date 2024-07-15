# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .common_uuid import CommonUuid

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class SessionsRouteDeleteResponse(pydantic.BaseModel):
    id: CommonUuid = pydantic.Field(description="ID of deleted undefined")
    deleted_at: dt.datetime = pydantic.Field(
        description="When this resource was deleted as UTC date-time"
    )
    jobs: typing.List[CommonUuid] = pydantic.Field(
        description="IDs (if any) of jobs created as part of this request"
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
