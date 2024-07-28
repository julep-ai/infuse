import json
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field

from agents_api.autogen.openapi_model import (
    ChatMLImageContentPart,
    ChatMLRole,
    ChatMLTextContentPart,
)
from agents_api.common.utils.datetime import utcnow

EntrySource = Literal["api_request", "api_response", "internal", "summarizer"]
Tokenizer = Literal["character_count"]


LOW_IMAGE_TOKEN_COUNT = 85
HIGH_IMAGE_TOKEN_COUNT = 85 + 4 * 170


class Entry(BaseModel):
    """Represents an entry in the system, encapsulating all necessary details such as ID, session ID, source, role, and content among others."""

    id: UUID = Field(
        alias="entry_id", default_factory=uuid4
    )  # Uses a default factory to generate a unique UUID
    session_id: UUID
    source: EntrySource = Field(default="api_request")
    role: ChatMLRole
    name: str | None = None
    content: str | list[ChatMLTextContentPart] | list[ChatMLImageContentPart] | dict
    tokenizer: str = Field(default="character_count")
    created_at: float = Field(
        default_factory=lambda: utcnow().timestamp()
    )  # Uses a default factory to set the creation timestamp
    timestamp: float = Field(
        default_factory=lambda: utcnow().timestamp()
    )  # Uses a default factory to set the current timestamp

    @computed_field
    @property
    def token_count(self) -> int:
        """Calculates the token count based on the content's character count. The tokenizer 'character_count' divides the length of the content by 3.5 to estimate the token count. Raises NotImplementedError for unknown tokenizers."""
        if self.tokenizer == "character_count":
            content_length = 0
            if isinstance(self.content, str):
                content_length = len(self.content)
            elif isinstance(self.content, dict):
                content_length = len(json.dumps(self.content))
            elif isinstance(self.content, list):
                for part in self.content:
                    if isinstance(part, ChatMLTextContentPart):
                        content_length += len(part.text)
                    elif isinstance(part, ChatMLImageContentPart):
                        content_length += (
                            LOW_IMAGE_TOKEN_COUNT
                            if part.image_url.detail == "low"
                            else HIGH_IMAGE_TOKEN_COUNT
                        )

            # Divide the content length by 3.5 to estimate token count based on character count.
            return int(content_length // 3.5)

        raise NotImplementedError(f"Unknown tokenizer: {self.tokenizer}")

    class Config:
        """Configuration settings for the Entry model, ensuring enum values are used."""

        use_enum_values = True  # Ensures that enum values are used in serialization
