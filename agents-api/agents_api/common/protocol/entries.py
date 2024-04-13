from datetime import datetime
import json
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field, validator
from agents_api.autogen.openapi_model import Role

EntrySource = Literal["api_request", "api_response", "internal", "summarizer"]
Tokenizer = Literal["character_count"]


class Entry(BaseModel):
    """Represents an entry in the system, encapsulating all necessary details such as ID, session ID, source, role, and content among others."""
    id: UUID = Field(alias="entry_id", default_factory=uuid4)  # Uses a default factory to generate a unique UUID
    session_id: UUID
    source: EntrySource = Field(default="api_request")
    role: Role
    name: str | None = None
    content: str
    tokenizer: str = Field(default="character_count")
    created_at: float = Field(default_factory=lambda: datetime.utcnow().timestamp())  # Uses a default factory to set the creation timestamp
    timestamp: float = Field(default_factory=lambda: datetime.utcnow().timestamp())  # Uses a default factory to set the current timestamp

    @computed_field
    @property
    def token_count(self) -> int:
        """Calculates the token count based on the content's character count. The tokenizer 'character_count' divides the length of the content by 3.5 to estimate the token count. Raises NotImplementedError for unknown tokenizers."""
        if self.tokenizer == "character_count":
            content_length = (
                len(self.content)
                if isinstance(self.content, str)
                else len(json.dumps(self.content))
            )
            # Divide the content length by 3.5 to estimate token count based on character count.
            return int(content_length // 3.5)

        raise NotImplementedError(f"Unknown tokenizer: {self.tokenizer}")

    class Config:
        """Configuration settings for the Entry model, ensuring enum values are used."""
        use_enum_values = True  # Ensures that enum values are used in serialization
        use_enum_values = True  # <--
