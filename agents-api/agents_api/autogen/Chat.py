# generated by datamodel-codegen:
#   filename:  openapi-0.4.0.yaml
#   timestamp: 2024-07-15T21:10:09+00:00

from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class Type(str, Enum):
    """
    The format of the response
    """

    text = "text"
    json_object = "json_object"


class CompletionResponseFormat(BaseModel):
    type: Type
    """
    The format of the response
    """


class GenerationPreset(str, Enum):
    """
    Generation preset (one of: problem_solving, conversational, fun, prose, creative, business, deterministic, code, multilingual)
    """

    problem_solving = "problem_solving"
    conversational = "conversational"
    fun = "fun"
    prose = "prose"
    creative = "creative"
    business = "business"
    deterministic = "deterministic"
    code = "code"
    multilingual = "multilingual"


class GenerationPresetSettings(BaseModel):
    preset: GenerationPreset | None = None
    """
    Generation preset (one of: problem_solving, conversational, fun, prose, creative, business, deterministic, code, multilingual)
    """


class OpenAISettings(BaseModel):
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


class VLLMSettings(BaseModel):
    repetition_penalty: Annotated[float | None, Field(None, ge=0.0, le=2.0)]
    """
    Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    """
    length_penalty: Annotated[float | None, Field(None, ge=0.0, le=2.0)]
    """
    Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize number of tokens generated.
    """
    temperature: Annotated[float | None, Field(None, ge=0.0, le=5.0)]
    """
    What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    """
    top_p: Annotated[float | None, Field(None, ge=0.0, le=1.0)]
    """
    Defaults to 1 An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or temperature but not both.
    """
    min_p: Annotated[float | None, Field(None, ge=0.0, le=1.0)]
    """
    Minimum probability compared to leading token to be considered
    """
