from uuid import uuid4
from typing import Any
from fastapi import APIRouter, HTTPException, status
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from pydantic import UUID4

from memory_api.clients.cozo import client
from memory_api.models.agent.create_agent import create_agent_query
from memory_api.models.agent.get_agent import get_agent_query
from memory_api.models.agent.list_agents import list_agents_query
from memory_api.autogen.openapi_model import Agent, CreateAgentRequest, UpdateAgentRequest


router = APIRouter()


async def get_agent(agent_id: UUID4) -> Agent:
    try:
        res = [
            row.to_dict()
            for _, row in client.run(get_agent_query(agent_id=agent_id)).iterrows()
        ][0]
        return Agent(**res)
    except (IndexError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )


@router.delete("/agents/{agent_id}", status_code=HTTP_202_ACCEPTED, tags=["agents"])
async def delete_agent(agent_id: UUID4):
    try:
        client.rm("agents", {"agent_id": str(agent_id)})
    except (IndexError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )


@router.put("/agents/{agent_id}", tags=["agents"])
async def update_agent(agent_id: UUID4, request: UpdateAgentRequest):
    try:
        client.update(
            "agents",
            {
                "agent_id": str(agent_id),
                "about": request.about,
            },
        )
    except (IndexError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )


@router.post("/agents", status_code=HTTP_201_CREATED, tags=["agents"])
async def create_agent(agent: CreateAgentRequest) -> Agent:
    client.run(
        create_agent_query(agent_id=uuid4(), name=agent.name, about=agent.about),
    )

    return await get_agent(agent_id=agent.id)


@router.get("/agents", tags=["agents"])
async def list_agents(limit: int = 100, offset: int = 0) -> list[Agent]:
    return [
        Agent(**row.to_dict())
        for _, row in client.run(
            list_agents_query(limit=limit, offset=offset)
        ).iterrows()
    ]


@router.get("/agents/{agent_id}/memories", tags=["agents"])
async def list_memories(agent_id: UUID4) -> list[Any]:
    # TODO: implement later
    return []
