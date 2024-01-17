# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import typing_extensions

from ..core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class Belief(pydantic.BaseModel):
    type: typing_extensions.Literal["belief"]
    subject: typing.Optional[str] = pydantic.Field(description="(Optional) ID of the subject user")
    content: str = pydantic.Field(description="Content of the memory")
    rationale: typing.Optional[str] = pydantic.Field(
        description="Rationale: Why did the model decide to form this memory"
    )
    weight: float = pydantic.Field(description="Weight (importance) of the memory on a scale of 0-100")
    sentiment: float = pydantic.Field(description="Sentiment (valence) of the memory on a scale of -1 to 1")
    created_at: dt.datetime = pydantic.Field(description="Belief created at (RFC-3339 format)")
    id: str = pydantic.Field(description="Belief id (UUID)")

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
