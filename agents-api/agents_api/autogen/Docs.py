# generated by datamodel-codegen:
#   filename:  openapi-1.0.0.yaml

from __future__ import annotations

from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StrictBool


class BaseDocSearchRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    limit: Annotated[int, Field(ge=1, le=50)] = 10
    lang: Literal["en-US"] = "en-US"
    """
    The language to be used for text-only search. Support for other languages coming soon.
    """
    metadata_filter: dict[str, float | str | StrictBool | None] = {}
    mmr_strength: Annotated[float, Field(0, ge=0.0, lt=1.0)]
    """
    MMR Strength (mmr_strength = 1 - mmr_lambda)
    """


class CreateDocRequest(BaseModel):
    """
    Payload for creating a doc
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    metadata: dict[str, Any] | None = None
    title: Annotated[str, Field(max_length=800)]
    """
    Title describing what this document contains
    """
    content: str | list[str]
    """
    Contents of the document
    """
    embed_instruction: str | None = None
    """
    Instruction for the embedding model.
    """


class Doc(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: Annotated[UUID, Field(json_schema_extra={"readOnly": True})]
    metadata: dict[str, Any] | None = None
    created_at: Annotated[AwareDatetime, Field(json_schema_extra={"readOnly": True})]
    """
    When this resource was created as UTC date-time
    """
    title: Annotated[str, Field(max_length=800)]
    """
    Title describing what this document contains
    """
    content: str | list[str]
    """
    Contents of the document
    """
    embeddings: Annotated[
        list[float] | list[list[float]] | None,
        Field(json_schema_extra={"readOnly": True}),
    ] = None
    """
    Embeddings for the document
    """


class DocOwner(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: UUID
    role: Literal["user", "agent"]


class DocReference(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    owner: DocOwner
    """
    The owner of this document.
    """
    id: Annotated[UUID, Field(json_schema_extra={"readOnly": True})]
    """
    ID of the document
    """
    title: str | None = None
    snippets: Annotated[list[Snippet], Field(min_length=1)]
    distance: float | None = None


class DocSearchResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    docs: list[DocReference]
    """
    The documents that were found
    """
    time: Annotated[float, Field(gt=0.0)]
    """
    The time taken to search in seconds
    """


class EmbedQueryResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    vectors: list[list[float]]
    """
    The embedded vectors
    """


class HybridDocSearchRequest(BaseDocSearchRequest):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = 0.5
    """
    The confidence cutoff level
    """
    alpha: Annotated[float, Field(ge=0.0, le=1.0)] = 0.75
    """
    The weight to apply to BM25 vs Vector search results. 0 => pure BM25; 1 => pure vector;
    """
    text: str
    """
    Text to use in the search. In `hybrid` search mode, either `text` or both `text` and `vector` fields are required.
    """
    vector: list[float]
    """
    Vector to use in the search. Must be the same dimensions as the embedding model or else an error will be thrown.
    """


class MultipleEmbedQueryRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    text: Annotated[list[str], Field(max_length=100, min_length=1)]
    """
    Texts to embed
    """
    embed_instruction: str = ""
    """
    Instruction for the embedding model.
    """


class SingleEmbedQueryRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    text: str
    """
    Text to embed
    """
    embed_instruction: str = ""
    """
    Instruction for the embedding model.
    """


class Snippet(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    index: int
    content: str


class TextOnlyDocSearchRequest(BaseDocSearchRequest):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    text: str
    """
    Text to use in the search.
    """


class VectorDocSearchRequest(BaseDocSearchRequest):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = 0.5
    """
    The confidence cutoff level
    """
    vector: list[float]
    """
    Vector to use in the search. Must be the same dimensions as the embedding model or else an error will be thrown.
    """
