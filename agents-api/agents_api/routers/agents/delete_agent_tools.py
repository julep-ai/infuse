from typing import Annotated
from uuid import UUID

from fastapi import Depends
from pydantic import UUID4

from ...autogen.openapi_model import ResourceDeletedResponse
from ...dependencies.developer_id import get_developer_id
from ...models.tools.delete_tool import delete_tool
from .router import router


@router.delete("/agents/{agent_id}/tools/{tool_id}", tags=["agents"])
async def delete_agent_tools(
    agent_id: UUID,
    tool_id: UUID,
    x_developer_id: Annotated[UUID4, Depends(get_developer_id)],
) -> ResourceDeletedResponse:
    return delete_tool(
        developer_id=x_developer_id,
        agent_id=agent_id,
        tool_id=tool_id,
    )
