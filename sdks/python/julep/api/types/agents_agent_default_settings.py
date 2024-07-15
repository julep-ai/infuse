# This file was auto-generated by Fern from our API Definition.

import typing

from .chat_generation_preset import ChatGenerationPreset
from .chat_generation_preset_settings import ChatGenerationPresetSettings
from .chat_open_ai_settings import ChatOpenAiSettings
from .chat_v_llm_settings import ChatVLlmSettings

AgentsAgentDefaultSettings = typing.Union[
    ChatGenerationPresetSettings, ChatOpenAiSettings, ChatVLlmSettings
]
