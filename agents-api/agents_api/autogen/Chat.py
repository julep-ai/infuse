# generated by datamodel-codegen:
#   filename:  openapi-0.4.0.yaml

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from .Common import LogitBias
from .Docs import DocReference
from .Entries import InputChatMLMessage
from .Tools import FunctionTool, NamedToolChoice


class BaseChatOutput(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    index: int
    finish_reason: Literal["stop", "length", "content_filter", "tool_calls"]
    """
    The reason the model stopped generating tokens
    """
    logprobs: LogProbResponse | None = None
    """
    The log probabilities of tokens
    """


class BaseChatResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    usage: CompetionUsage | None = None
    """
    Usage statistics for the completion request
    """
    jobs: list[UUID]
    """
    Background job IDs that may have been spawned from this interaction.
    """
    docs: list[DocReference]
    """
    Documents referenced for this request (for citation purposes).
    """
    created_at: Annotated[AwareDatetime, Field(json_schema_extra={"readOnly": True})]
    """
    When this resource was created as UTC date-time
    """
    id: Annotated[UUID, Field(json_schema_extra={"readOnly": True})]


class BaseTokenLogProb(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    token: str
    logprob: float
    """
    The log probability of the token
    """
    bytes: list[int] | None = None


class ChatInputData(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    messages: Annotated[list[InputChatMLMessage], Field(min_length=1)]
    """
    A list of new input messages comprising the conversation so far.
    """
    tools: Annotated[list[FunctionTool] | None, Field(None, min_length=1)]
    """
    (Advanced) List of tools that are provided in addition to agent's default set of tools.
    """
    tool_choice: Literal["auto", "none"] | NamedToolChoice | None = None
    """
    Can be one of existing tools given to the agent earlier or the ones provided in this request.
    """


class ChatOutputChunk(BaseChatOutput):
    """
    Streaming chat completion output
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    delta: InputChatMLMessage
    """
    The message generated by the model
    """


class ChunkChatResponse(BaseChatResponse):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    choices: list[ChatOutputChunk]
    """
    The deltas generated by the model
    """


class CompetionUsage(BaseModel):
    """
    Usage statistics for the completion request
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    completion_tokens: Annotated[
        int | None, Field(None, json_schema_extra={"readOnly": True})
    ]
    """
    Number of tokens in the generated completion
    """
    prompt_tokens: Annotated[
        int | None, Field(None, json_schema_extra={"readOnly": True})
    ]
    """
    Number of tokens in the prompt
    """
    total_tokens: Annotated[
        int | None, Field(None, json_schema_extra={"readOnly": True})
    ]
    """
    Total number of tokens used in the request (prompt + completion)
    """


class CompletionResponseFormat(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    type: Literal["text", "json_object"] = "text"
    """
    The format of the response
    """


class LogProbResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Annotated[list[TokenLogProb] | None, Field(...)]
    """
    The log probabilities of the tokens
    """


class MessageChatResponse(BaseChatResponse):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    choices: list[SingleChatOutput | MultipleChatOutput]
    """
    The deltas generated by the model
    """


class MultipleChatOutput(BaseChatOutput):
    """
    The output returned by the model. Note that, depending on the model provider, they might return more than one message.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    messages: list[InputChatMLMessage]


class OpenAISettings(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    frequency_penalty: Annotated[float | None, Field(None, ge=-2.0, le=2.0)]
    """
    Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    presence_penalty: Annotated[float | None, Field(None, ge=-2.0, le=2.0)]
    """
    Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    temperature: Annotated[float | None, Field(None, ge=0.0, le=5.0)]
    """
    What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    """
    top_p: Annotated[float | None, Field(None, ge=0.0, le=1.0)]
    """
    Defaults to 1 An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or temperature but not both.
    """


class SingleChatOutput(BaseChatOutput):
    """
    The output returned by the model. Note that, depending on the model provider, they might return more than one message.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    message: InputChatMLMessage


class TokenLogProb(BaseTokenLogProb):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    top_logprobs: list[BaseTokenLogProb]


class ChatInput(ChatInputData):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    remember: Annotated[bool, Field(False, json_schema_extra={"readOnly": True})]
    """
    DISABLED: Whether this interaction should form new memories or not (will be enabled in a future release)
    """
    recall: bool = True
    """
    Whether previous memories and docs should be recalled or not
    """
    save: bool = True
    """
    Whether this interaction should be stored in the session history or not
    """
    model: Annotated[
        str | None,
        Field(
            None,
            pattern="^[\\p{L}\\p{Nl}\\p{Pattern_Syntax}\\p{Pattern_White_Space}]+[\\p{ID_Start}\\p{Mn}\\p{Mc}\\p{Nd}\\p{Pc}\\p{Pattern_Syntax}\\p{Pattern_White_Space}]*$",
        ),
    ]
    """
    Identifier of the model to be used
    """
    stream: bool = False
    """
    Indicates if the server should stream the response as it's generated
    """
    stop: Annotated[list[str] | None, Field(None, max_length=4, min_length=1)]
    """
    Up to 4 sequences where the API will stop generating further tokens.
    """
    seed: Annotated[int | None, Field(None, ge=-1, le=1000)]
    """
    If specified, the system will make a best effort to sample deterministically for that particular seed value
    """
    max_tokens: Annotated[int | None, Field(None, ge=1)]
    """
    The maximum number of tokens to generate in the chat completion
    """
    logit_bias: dict[str, LogitBias] | None = None
    """
    Modify the likelihood of specified tokens appearing in the completion
    """
    response_format: CompletionResponseFormat | None = None
    """
    Response format (set to `json_object` to restrict output to JSON)
    """
    agent: UUID | None = None
    """
    Agent ID of the agent to use for this interaction. (Only applicable for multi-agent sessions)
    """
    repetition_penalty: Annotated[float | None, Field(None, ge=0.0, le=2.0)]
    """
    Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    length_penalty: Annotated[float | None, Field(None, ge=0.0, le=2.0)]
    """
    Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize number of tokens generated.
    """
    min_p: Annotated[float | None, Field(None, ge=0.0, le=1.0)]
    """
    Minimum probability compared to leading token to be considered
    """
    frequency_penalty: Annotated[float | None, Field(None, ge=-2.0, le=2.0)]
    """
    Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    presence_penalty: Annotated[float | None, Field(None, ge=-2.0, le=2.0)]
    """
    Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    temperature: Annotated[float | None, Field(None, ge=0.0, le=5.0)]
    """
    What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    """
    top_p: Annotated[float | None, Field(None, ge=0.0, le=1.0)]
    """
    Defaults to 1 An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or temperature but not both.
    """


class DefaultChatSettings(OpenAISettings):
    """
    Default settings for the chat session (also used by the agent)
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    repetition_penalty: Annotated[float | None, Field(None, ge=0.0, le=2.0)]
    """
    Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    length_penalty: Annotated[float | None, Field(None, ge=0.0, le=2.0)]
    """
    Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize number of tokens generated.
    """
    min_p: Annotated[float | None, Field(None, ge=0.0, le=1.0)]
    """
    Minimum probability compared to leading token to be considered
    """


class ChatSettings(DefaultChatSettings):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    model: Annotated[
        str | None,
        Field(
            None,
            pattern="^[\\p{L}\\p{Nl}\\p{Pattern_Syntax}\\p{Pattern_White_Space}]+[\\p{ID_Start}\\p{Mn}\\p{Mc}\\p{Nd}\\p{Pc}\\p{Pattern_Syntax}\\p{Pattern_White_Space}]*$",
        ),
    ]
    """
    Identifier of the model to be used
    """
    stream: bool = False
    """
    Indicates if the server should stream the response as it's generated
    """
    stop: Annotated[list[str] | None, Field(None, max_length=4, min_length=1)]
    """
    Up to 4 sequences where the API will stop generating further tokens.
    """
    seed: Annotated[int | None, Field(None, ge=-1, le=1000)]
    """
    If specified, the system will make a best effort to sample deterministically for that particular seed value
    """
    max_tokens: Annotated[int | None, Field(None, ge=1)]
    """
    The maximum number of tokens to generate in the chat completion
    """
    logit_bias: dict[str, LogitBias] | None = None
    """
    Modify the likelihood of specified tokens appearing in the completion
    """
    response_format: CompletionResponseFormat | None = None
    """
    Response format (set to `json_object` to restrict output to JSON)
    """
    agent: UUID | None = None
    """
    Agent ID of the agent to use for this interaction. (Only applicable for multi-agent sessions)
    """
