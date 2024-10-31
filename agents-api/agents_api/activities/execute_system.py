import asyncio
from typing import Any, Callable
from uuid import UUID

from beartype import beartype
from box import Box, BoxList
from fastapi.background import BackgroundTasks
from temporalio import activity

from ..autogen.Docs import (
    CreateDocRequest,
    HybridDocSearchRequest,
    TextOnlyDocSearchRequest,
    VectorDocSearchRequest,
)
from ..autogen.Tools import SystemDef
from ..common.protocol.tasks import StepContext
from ..common.storage_handler import auto_blob_store
from ..env import testing
from .utils import get_handler


@auto_blob_store
@beartype
async def execute_system(
    context: StepContext,
    system: SystemDef,
) -> Any:
    """Execute a system call with the appropriate handler and transformed arguments."""
    arguments: dict[str, Any] = system.arguments or {}
    arguments["developer_id"] = context.execution_input.developer_id

    # Unbox all the arguments
    for key, value in arguments.items():
        if isinstance(value, Box):
            arguments[key] = value.to_dict()
        elif isinstance(value, BoxList):
            arguments[key] = value.to_list()

    # Convert all UUIDs to UUID objects
    uuid_fields = ["agent_id", "user_id", "task_id", "session_id", "doc_id"]
    for field in uuid_fields:
        if field in arguments:
            arguments[field] = UUID(arguments[field])

    try:
        handler = get_handler(system)

        # Transform arguments for doc-related operations
        if system.subresource == "doc":
            owner_id_field = f"{system.resource}_id"
            if owner_id_field in arguments:
                doc_args = {
                    "owner_type": system.resource,
                    "owner_id": arguments[owner_id_field],
                    **arguments,
                }
                doc_args.pop(owner_id_field)
                arguments = doc_args

        # Handle special cases for doc operations
        if system.operation == "create" and system.subresource == "doc":
            arguments["x_developer_id"] = arguments.pop("developer_id")
            return await handler(
                data=CreateDocRequest(**arguments.pop("data")),
                background_tasks=BackgroundTasks(),
                **arguments,
            )

        # Handle search operations
        if system.operation == "search" and system.subresource == "doc":
            arguments["x_developer_id"] = arguments.pop("developer_id")
            search_params = _create_search_request(arguments)
            return await handler(search_params=search_params, **arguments)

        # Handle regular operations
        if asyncio.iscoroutinefunction(handler):
            return await handler(**arguments)
        return handler(**arguments)

    except BaseException as e:
        if activity.in_activity():
            activity.logger.error(f"Error in execute_system_call: {e}")
        raise


def _create_search_request(arguments: dict) -> Any:
    """Create appropriate search request based on available parameters."""
    if "text" in arguments and "vector" in arguments:
        return HybridDocSearchRequest(
            text=arguments.pop("text"),
            vector=arguments.pop("vector"),
            alpha=arguments.pop("alpha", 0.75),
            confidence=arguments.pop("confidence", 0.5),
            limit=arguments.get("limit", 10),
        )
    elif "text" in arguments:
        return TextOnlyDocSearchRequest(
            text=arguments.pop("text"),
            limit=arguments.get("limit", 10),
        )
    elif "vector" in arguments:
        return VectorDocSearchRequest(
            vector=arguments.pop("vector"),
            confidence=arguments.pop("confidence", 0.7),
            limit=arguments.get("limit", 10),
        )


# Keep the existing mock and activity definition
mock_execute_system = execute_system

execute_system = activity.defn(name="execute_system")(
    execute_system if not testing else mock_execute_system
)
