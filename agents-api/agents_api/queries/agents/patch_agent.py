"""
This module contains the functionality for partially updating an agent in the PostgreSQL database.
It constructs and executes SQL queries to update specific fields of an agent based on agent ID and developer ID.
"""

from typing import Literal
from uuid import UUID

import asyncpg
from beartype import beartype
from fastapi import HTTPException
from sqlglot import parse_one

from ...autogen.openapi_model import PatchAgentRequest, ResourceUpdatedResponse
from ...metrics.counters import increase_counter
from ..utils import (
    partialclass,
    pg_query,
    rewrap_exceptions,
    wrap_in_class,
)

# Define the raw SQL query
agent_query = parse_one("""
UPDATE agents
SET 
    name = CASE 
        WHEN NULLIF($3, '')::text IS NOT NULL THEN NULLIF($3, '')
        ELSE name 
    END,
    about = CASE 
        WHEN NULLIF($4, '')::text IS NOT NULL THEN NULLIF($4, '')
        ELSE about 
    END,
    metadata = CASE 
        WHEN $5::jsonb IS NOT NULL THEN metadata || $5 
        ELSE metadata 
    END,
    model = CASE 
        WHEN NULLIF($6, '')::text IS NOT NULL THEN NULLIF($6, '')
        ELSE model 
    END,
    default_settings = CASE 
        WHEN $7::jsonb IS NOT NULL THEN $7 
        ELSE default_settings 
    END
WHERE agent_id = $2 AND developer_id = $1
RETURNING *;
""").sql(pretty=True)


@rewrap_exceptions(
    {
        asyncpg.exceptions.ForeignKeyViolationError: partialclass(
            HTTPException,
            status_code=404,
            detail="The specified developer does not exist.",
        ),
        asyncpg.exceptions.UniqueViolationError: partialclass(
            HTTPException,
            status_code=409,
            detail="An agent with this canonical name already exists for this developer.",
        ),
        asyncpg.exceptions.CheckViolationError: partialclass(
            HTTPException,
            status_code=400,
            detail="The provided data violates one or more constraints. Please check the input values.",
        ),
        asyncpg.exceptions.DataError: partialclass(
            HTTPException,
            status_code=400,
            detail="Invalid data provided. Please check the input values.",
        ),
        asyncpg.exceptions.NoDataFoundError: partialclass(
            HTTPException,
            status_code=404,
            detail="The specified agent does not exist.",
        ),
    }
)
@wrap_in_class(
    ResourceUpdatedResponse,
    one=True,
    transform=lambda d: {"id": d["agent_id"], **d},
)
@increase_counter("patch_agent")
@pg_query
@beartype
async def patch_agent(
    *, agent_id: UUID, developer_id: UUID, data: PatchAgentRequest
) -> tuple[str, list, Literal["fetch", "fetchrow", "fetchmany"]]:
    """
    Constructs the SQL query to partially update an agent's details.

    Args:
        agent_id (UUID): The UUID of the agent to update.
        developer_id (UUID): The UUID of the developer owning the agent.
        data (PatchAgentRequest): A dictionary of fields to update.

    Returns:
        tuple[str, list]: A tuple containing the SQL query and its parameters.
    """
    params = [
        developer_id,
        agent_id,
        data.name,
        data.about,
        data.metadata,
        data.model,
        data.default_settings.model_dump() if data.default_settings else None,
    ]

    return (
        agent_query,
        params,
        "fetchrow",
    )
