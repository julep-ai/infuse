"""
Model Registry maintains a list of supported models and their configs.
"""

from typing import Dict
from agents_api.clients.model import julep_client, openai_client
from agents_api.common.exceptions.agents import (
    AgentModelNotValid,
    MissingAgentModelAPIKeyError,
)
from openai import AsyncOpenAI


GPT4_MODELS: Dict[str, int] = {
    # stable model names:
    #   resolves to gpt-4-0314 before 2023-06-27,
    #   resolves to gpt-4-0613 after
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    # turbo models (Turbo, JSON mode)
    "gpt-4-turbo": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4-0125-preview": 128000,
    "gpt-4-turbo-preview": 128000,
    # multimodal model
    "gpt-4-vision-preview": 128000,
    # 0613 models (function calling):
    #   https://openai.com/blog/function-calling-and-other-api-updates
    "gpt-4-0613": 8192,
    "gpt-4-32k-0613": 32768,
    # 0314 models
    "gpt-4-0314": 8192,
    "gpt-4-32k-0314": 32768,
}

TURBO_MODELS: Dict[str, int] = {
    # stable model names:
    #   resolves to gpt-3.5-turbo-0301 before 2023-06-27,
    #   resolves to gpt-3.5-turbo-0613 until 2023-12-11,
    #   resolves to gpt-3.5-turbo-1106 after
    "gpt-3.5-turbo": 4096,
    # resolves to gpt-3.5-turbo-16k-0613 until 2023-12-11
    # resolves to gpt-3.5-turbo-1106 after
    "gpt-3.5-turbo-16k": 16384,
    # 0125 (2024) model (JSON mode)
    "gpt-3.5-turbo-0125": 16385,
    # 1106 model (JSON mode)
    "gpt-3.5-turbo-1106": 16384,
    # 0613 models (function calling):
    #   https://openai.com/blog/function-calling-and-other-api-updates
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-16k-0613": 16384,
    # 0301 models
    "gpt-3.5-turbo-0301": 4096,
}

GPT3_5_MODELS: Dict[str, int] = {
    "text-davinci-003": 4097,
    "text-davinci-002": 4097,
    # instruct models
    "gpt-3.5-turbo-instruct": 4096,
}

GPT3_MODELS: Dict[str, int] = {
    "text-ada-001": 2049,
    "text-babbage-001": 2040,
    "text-curie-001": 2049,
    "ada": 2049,
    "babbage": 2049,
    "curie": 2049,
    "davinci": 2049,
}


DISCONTINUED_MODELS = {
    "code-davinci-002": 8001,
    "code-davinci-001": 8001,
    "code-cushman-002": 2048,
    "code-cushman-001": 2048,
}

CLAUDE_MODELS: Dict[str, int] = {
    "claude-instant-1": 100000,
    "claude-instant-1.2": 100000,
    "claude-2": 100000,
    "claude-2.0": 100000,
    "claude-2.1": 200000,
    "claude-3-opus-20240229": 180000,
    "claude-3-sonnet-20240229": 180000,
    "claude-3-haiku-20240307": 180000,
}

OPENAI_MODELS = {**GPT4_MODELS, **TURBO_MODELS, **GPT3_5_MODELS, **GPT3_MODELS}

JULEP_MODELS = {
    "julep-ai/samantha-1-turbo": 32768,
    "julep-ai/samantha-1-turbo-awq": 32768,
}

CHAT_MODELS = {**GPT4_MODELS, **TURBO_MODELS, **CLAUDE_MODELS}

ALL_AVAILABLE_MODELS = {
    **JULEP_MODELS,
    **GPT4_MODELS,
    **TURBO_MODELS,
    **GPT3_5_MODELS,
    **GPT3_MODELS,
    # **CLAUDE_MODELS,
}


def validate_configuration(model: str):
    """
    Validates the model specified in the request
    """
    if model not in ALL_AVAILABLE_MODELS:
        raise AgentModelNotValid(model, list(ALL_AVAILABLE_MODELS.keys()))
    model_client = get_model_client(model)
    if model_client.api_key == "":
        raise MissingAgentModelAPIKeyError(model)


def get_model_client(model: str) -> AsyncOpenAI:
    """
    Returns the model serving client based on the model
    """
    if model in JULEP_MODELS:
        return julep_client
    elif model in OPENAI_MODELS:
        return openai_client


# TODO: implement and use this to work with the response from different model formats
def parse_response():
    """
    method that converts the response from the provider back into the openai format
    """
    pass
