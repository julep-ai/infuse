from typing import Literal
from uuid import UUID

import asyncpg
from beartype import beartype
from fastapi import HTTPException
from sqlglot import parse_one

from ...autogen.openapi_model import ResourceDeletedResponse
from ...common.utils.datetime import utcnow
from ..utils import partialclass, pg_query, rewrap_exceptions, wrap_in_class

# Delete doc query + ownership check
delete_doc_query = parse_one("""
WITH deleted_owners AS (
    DELETE FROM doc_owners
    WHERE developer_id = $1
      AND doc_id = $2
      AND owner_type = $3 
      AND owner_id = $4
)
DELETE FROM docs
WHERE developer_id = $1
  AND doc_id = $2
  AND EXISTS (
    SELECT 1 FROM doc_owners
    WHERE developer_id = $1
      AND doc_id = $2
      AND owner_type = $3
      AND owner_id = $4
  )
RETURNING doc_id;
""").sql(pretty=True)


@rewrap_exceptions(
    {
        asyncpg.NoDataFoundError: partialclass(
            HTTPException,
            status_code=404,
            detail="Doc not found",
        )
    }
)
@wrap_in_class(
    ResourceDeletedResponse,
    one=True,
    transform=lambda d: {
        "id": d["doc_id"],
        "deleted_at": utcnow(),
        "jobs": [],
    },
)
@pg_query
@beartype
async def delete_doc(
    *,
    developer_id: UUID,
    doc_id: UUID,
    owner_type: Literal["user", "agent"],
    owner_id: UUID,
) -> tuple[str, list]:
    """
    Deletes a doc (and associated doc_owners) for the given developer and doc_id.
    If owner_type/owner_id is specified, only remove doc if that matches.

    Parameters:
        developer_id (UUID): The ID of the developer.
        doc_id (UUID): The ID of the document.
        owner_type (Literal["user", "agent"]): The type of the owner of the documents.
        owner_id (UUID): The ID of the owner of the documents.

    Returns:
        tuple[str, list]: SQL query and parameters for deleting the document.
    """
    return (
        delete_doc_query,
        [developer_id, doc_id, owner_type, owner_id],
    )