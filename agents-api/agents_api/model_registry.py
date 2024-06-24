"""
Model Registry maintains a list of supported models and their configs.
"""

import ast
import datetime
import json
import os
from typing import Dict
from agents_api.clients.worker.types import ChatML
from agents_api.common.exceptions.agents import (
    AgentModelNotValid,
    MissingAgentModelAPIKeyError,
)
import litellm
from litellm.utils import get_valid_models
import yaml
from pydantic import BaseModel
from typing import List, Dict, Literal, Optional
import xml.etree.ElementTree as ET


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

LOCAL_MODELS = {
    "julep-ai/samantha-1-turbo": 32768,
    "julep-ai/samantha-1-turbo-awq": 32768,
    "TinyLlama/TinyLlama_v1.1": 2048,
    "casperhansen/llama-3-8b-instruct-awq": 8192,
    "NousResearch/Hermes-2-Theta-Llama-3-8B": 8192
}

LOCAL_MODELS_WITH_TOOL_CALLS = {
    "NousResearch/Hermes-2-Theta-Llama-3-8B": 8192
}

CHAT_MODELS = {**GPT4_MODELS, **TURBO_MODELS, **CLAUDE_MODELS}

ALL_AVAILABLE_MODELS = litellm.model_list + list(LOCAL_MODELS.keys())
VALID_MODELS = get_valid_models() + list(LOCAL_MODELS.keys())

class FunctionCall(BaseModel):
    arguments: dict
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: str
    """The name of the function to call."""


class FunctionDefinition(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, object]] = None


class FunctionSignature(BaseModel):
    function: FunctionDefinition
    type: Literal["function"]

class PromptSchema(BaseModel):
    Role: str
    Objective: str
    Tools: str
    Schema: str
    Instructions: str


class PromptManager:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def format_yaml_prompt(self, prompt_schema: PromptSchema, variables: Dict) -> str:
        formatted_prompt = ""
        for field, value in prompt_schema.dict().items():
            formatted_value = value.format(**variables)
            if field == "Instructions":
                formatted_prompt += f"{formatted_value}"
            else:
                formatted_value = formatted_value.replace("\n", " ")
                formatted_prompt += f"{formatted_value}"
        return formatted_prompt

    def read_yaml_file(self, file_path: str) -> PromptSchema:
        with open(file_path, "r") as file:
            yaml_content = yaml.safe_load(file)

        prompt_schema = PromptSchema(
            Role=yaml_content.get("Role", ""),
            Objective=yaml_content.get("Objective", ""),
            Tools=yaml_content.get("Tools", ""),
            Schema=yaml_content.get("Schema", ""),
            Instructions=yaml_content.get("Instructions", ""),
        )
        return prompt_schema

    def generate_prompt(self, user_prompt, tools):
        prompt_path = os.path.join(self.script_dir, "prompt_assets", "sys_prompt.yml")
        prompt_schema = self.read_yaml_file(prompt_path)

        schema_json = json.loads(FunctionCall.schema_json())
        # schema = schema_json.get("properties", {})

        variables = {
            "date": datetime.date.today(),
            "tools": tools,
            "schema": schema_json,
        }
        sys_prompt = self.format_yaml_prompt(prompt_schema, variables)

        prompt = [{"content": sys_prompt, "role": "system"}]
        # prompt.extend(user_prompt)
        return prompt


def validate_and_extract_tool_calls(assistant_content):
    validation_result = False
    tool_calls = []
    error_message = None

    try:
        # wrap content in root element
        xml_root_element = f"<root>{assistant_content}</root>"
        root = ET.fromstring(xml_root_element)

        # extract JSON data
        for element in root.findall(".//tool_call"):
            json_data = None
            try:
                json_text = element.text.strip()

                try:
                    # Prioritize json.loads for better error handling
                    json_data = json.loads(json_text)
                except json.JSONDecodeError as json_err:
                    try:
                        # Fallback to ast.literal_eval if json.loads fails
                        json_data = ast.literal_eval(json_text)
                    except (SyntaxError, ValueError) as eval_err:
                        error_message = f"JSON parsing failed with both json.loads and ast.literal_eval:\n"\
                                        f"- JSON Decode Error: {json_err}\n"\
                                        f"- Fallback Syntax/Value Error: {eval_err}\n"\
                                        f"- Problematic JSON text: {json_text}"
                        continue
            except Exception as e:
                error_message = f"Cannot strip text: {e}"

            if json_data is not None:
                tool_calls.append(json_data)
                validation_result = True

    except ET.ParseError as err:
        error_message = f"XML Parse Error: {err}"

    # Return default values if no valid data is extracted
    return validation_result, tool_calls, error_message



def validate_configuration(model: str):
    """
    Validates the model specified in the request
    """
    if model not in ALL_AVAILABLE_MODELS:
        raise AgentModelNotValid(model, ALL_AVAILABLE_MODELS)
    elif model not in VALID_MODELS:
        raise MissingAgentModelAPIKeyError(model)


def load_context(init_context: list[ChatML], model: str):
    """
    Converts the message history into a format supported by the model.
    """
    if model in litellm.utils.get_valid_models():
        init_context = [
            {
                "role": "assistant" if msg.role == "function_call" else msg.role,
                "content": msg.content,
            }
            for msg in init_context
        ]
    elif model in LOCAL_MODELS:
        init_context = [
            {"name": msg.name, "role": msg.role, "content": msg.content}
            for msg in init_context
        ]
    else:
        raise AgentModelNotValid(model, ALL_AVAILABLE_MODELS)
    return init_context


def get_extra_settings(settings):
    extra_settings = (
        dict(
            repetition_penalty=settings.repetition_penalty,
            best_of=1,
            top_k=1,
            length_penalty=settings.length_penalty,
            logit_bias=settings.logit_bias,
            preset=settings.preset.name if settings.preset else None,
        )
        if settings.model in LOCAL_MODELS
        else {}
    )

    return extra_settings


# TODO: implement and use this to work with the response from different model formats
def parse_response():
    """
    method that converts the response from the provider back into the openai format
    """
    pass
