from typing import Literal
from uuid import UUID

from beartype import beartype
from uuid_extensions import uuid7

from ...autogen.openapi_model import CreateOrUpdateTaskRequest, ResourceUpdatedResponse
from ...common.protocol.tasks import task_to_spec
from ...common.utils.db_exceptions import common_db_exceptions
from ...metrics.counters import increase_counter
from ..utils import generate_canonical_name, pg_query, rewrap_exceptions, wrap_in_class

# Define the raw SQL query for creating or updating a task
tools_query = """
INSERT INTO tools (
    developer_id,
    agent_id,
    task_id,
    tool_id,
    type,
    name,
    description,
    spec
)
VALUES (
    $1,                 -- developer_id
    $2,                 -- agent_id
    $3,                 -- task_id
    $4,                 -- tool_id
    $5,                 -- type
    $6,                 -- name
    $7,                 -- description
    $8                  -- spec
)
ON CONFLICT (agent_id, task_id, name) DO UPDATE SET
    type = EXCLUDED.type,
    description = EXCLUDED.description,
    spec = EXCLUDED.spec
RETURNING *;
"""

task_query = """
INSERT INTO tasks (
    "version",
    developer_id,
    canonical_name,
    agent_id,
    task_id,
    name,
    description,
    inherit_tools,
    input_schema,
    metadata
)
SELECT
    next_version,                 -- version
    $1,                          -- developer_id
    effective_canonical_name,     -- canonical_name
    $3,                          -- agent_id
    $4,                          -- task_id
    $5,                          -- name
    $6,                          -- description
    $7,                          -- inherit_tools
    $8::jsonb,                   -- input_schema
    $9::jsonb                    -- metadata
FROM current_version
ON CONFLICT (developer_id, task_id, "version") DO UPDATE SET
    version = tasks.version + 1,
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    inherit_tools = EXCLUDED.inherit_tools,
    input_schema = EXCLUDED.input_schema,
    metadata = EXCLUDED.metadata
RETURNING *, (SELECT next_version FROM current_version) as next_version;
"""

# Define the raw SQL query for inserting workflows
workflows_query = """
WITH version AS (
    SELECT COALESCE(MAX("version"), 0) as current_version
    FROM tasks
    WHERE developer_id = $1
      AND task_id = $2
)
INSERT INTO workflows (
    developer_id,
    task_id,
    "version",
    name,
    step_idx,
    step_type,
    step_definition
)
SELECT
    $1,                 -- developer_id
    $2,                 -- task_id
    current_version,    -- version
    $3,                 -- name
    $4,                 -- step_idx
    $5,                 -- step_type
    $6                  -- step_definition
FROM version
"""


@rewrap_exceptions(common_db_exceptions("task", ["create_or_update"]))
@wrap_in_class(
    ResourceUpdatedResponse,
    one=True,
    transform=lambda d: {
        "id": d["task_id"],
        "updated_at": d["updated_at"].timestamp(),
        **d,
    },
)
@increase_counter("create_or_update_task")
@pg_query(return_index=0)
@beartype
async def create_or_update_task(
    *,
    developer_id: UUID,
    agent_id: UUID,
    task_id: UUID,
    data: CreateOrUpdateTaskRequest,
) -> list[tuple[str, list, Literal["fetch", "fetchmany"]]]:
    """
    Constructs an SQL query to create or update a task.

    Args:
        developer_id (UUID): The UUID of the developer.
        agent_id (UUID): The UUID of the agent.
        task_id (UUID): The UUID of the task.
        data (CreateOrUpdateTaskRequest): The task data to insert or update.

    Returns:
        list[tuple[str, list, Literal["fetch", "fetchmany"]]]: List of SQL queries and parameters.

    Raises:
        HTTPException: If developer/agent doesn't exist (404) or on unique constraint violation (409)
    """

    # Generate canonical name from task name if not provided
    canonical_name = data.canonical_name or generate_canonical_name()

    # Version will be determined by the CTE
    task_params = [
        developer_id,  # $1
        canonical_name,  # $2
        agent_id,  # $3
        task_id,  # $4
        data.name,  # $5
        data.description,  # $6
        data.inherit_tools,  # $7
        data.input_schema or {},  # $8
        data.metadata or {},  # $9
    ]

    # Prepare tool parameters for the tools table
    tool_params = [
        [
            developer_id,
            agent_id,
            task_id,
            uuid7(),  # tool_id
            tool.type,
            tool.name,
            tool.description,
            getattr(tool, tool.type)
            and getattr(tool, tool.type).model_dump(mode="json"),  # spec
        ]
        for tool in data.tools or []
    ]

    # Generate workflows from task data using task_to_spec
    workflows_spec = task_to_spec(data).model_dump(mode="json")
    workflow_params = []
    for workflow in workflows_spec.get("workflows", []):
        workflow_name = workflow.get("name")
        steps = workflow.get("steps", [])
        for step_idx, step in enumerate(steps):
            workflow_params.append([
                developer_id,  # $1
                task_id,  # $2
                workflow_name,  # $3
                step_idx,  # $4
                step["kind_"],  # $5
                step,  # $6
            ])

    return [
        (
            task_query,
            task_params,
            "fetch",
        ),
        (
            tools_query,
            tool_params,
            "fetchmany",
        ),
        (
            workflows_query,
            workflow_params,
            "fetchmany",
        ),
    ]
