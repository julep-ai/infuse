# generated by datamodel-codegen:
#   filename:  openapi-0.4.0.yaml

from __future__ import annotations

from typing import Annotated, Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from .Chat import GenerationPresetSettings, OpenAISettings, VLLMSettings
from .Common import IdentifierSafeUnicode, Uuid


class Agent(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: Annotated[Uuid, Field(json_schema_extra={"readOnly": True})]
    metadata: dict[str, Any] | None = None
    created_at: Annotated[AwareDatetime, Field(json_schema_extra={"readOnly": True})]
    """
    When this resource was created as UTC date-time
    """
    updated_at: Annotated[AwareDatetime, Field(json_schema_extra={"readOnly": True})]
    """
    When this resource was updated as UTC date-time
    """
    name: IdentifierSafeUnicode = ""
    """
    Name of the agent
    """
    about: str = ""
    """
    About the agent
    """
    model: str = ""
    """
    Model name to use (gpt-4-turbo, gemini-nano etc)
    """
    instructions: str | list[str] = ""
    """
    Instructions for the agent
    """
    default_settings: (
        GenerationPresetSettings | OpenAISettings | VLLMSettings | None
    ) = None
    """
    Default settings for all sessions created by this agent
    """
