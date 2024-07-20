# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .chat_completion_response_format import ChatCompletionResponseFormat
from .chat_generation_preset import ChatGenerationPreset
from .common_identifier_safe_unicode import CommonIdentifierSafeUnicode
from .common_logit_bias import CommonLogitBias
from .common_uuid import CommonUuid


class TasksPromptStepSettingsPreset(pydantic_v1.BaseModel):
    model: typing.Optional[CommonIdentifierSafeUnicode] = pydantic_v1.Field(
        default=None
    )
    """
    Identifier of the model to be used
    """

    stream: bool = pydantic_v1.Field()
    """
    Indicates if the server should stream the response as it's generated
    """

    stop: typing.Optional[typing.List[str]] = pydantic_v1.Field(default=None)
    """
    Up to 4 sequences where the API will stop generating further tokens.
    """

    seed: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    If specified, the system will make a best effort to sample deterministically for that particular seed value
    """

    max_tokens: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    The maximum number of tokens to generate in the chat completion
    """

    logit_bias: typing.Optional[typing.Dict[str, CommonLogitBias]] = pydantic_v1.Field(
        default=None
    )
    """
    Modify the likelihood of specified tokens appearing in the completion
    """

    response_format: typing.Optional[ChatCompletionResponseFormat] = pydantic_v1.Field(
        default=None
    )
    """
    Response format (set to `json_object` to restrict output to JSON)
    """

    agent: typing.Optional[CommonUuid] = pydantic_v1.Field(default=None)
    """
    Agent ID of the agent to use for this interaction. (Only applicable for multi-agent sessions)
    """

    preset: typing.Optional[ChatGenerationPreset] = pydantic_v1.Field(default=None)
    """
    Generation preset (one of: problem_solving, conversational, fun, prose, creative, business, deterministic, code, multilingual)
    """

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
