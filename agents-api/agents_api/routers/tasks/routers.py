from typing import Annotated
from uuid import uuid4
from agents_api.models.execution.create_execution import create_execution_query
from agents_api.models.execution.get_execution import get_execution_query
from agents_api.models.execution.get_execution_transition import (
    get_execution_transition_query,
)
from agents_api.models.execution.list_execution_transitions import (
    list_execution_transition_query,
)
from agents_api.models.execution.list_executions import list_task_executions_query
from agents_api.models.task.create_task import create_task_query
from agents_api.models.task.get_task import get_task_query
from agents_api.models.task.list_tasks import list_tasks_query
from fastapi import APIRouter, HTTPException, status, Depends
import pandas as pd
from pydantic import BaseModel
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED

from pycozo.client import QueryException
from agents_api.autogen.openapi_model import (
    CreateTask,
    CreateExecution,
    Task,
    Execution,
    ExecutionTransition,
    ResourceCreatedResponse,
    ResourceUpdatedResponse,
)
from agents_api.dependencies.developer_id import get_developer_id


class TaskList(BaseModel):
    items: list[Task]


class ExecutionList(BaseModel):
    items: list[Execution]


class ExecutionTransitionList(BaseModel):
    items: list[ExecutionTransition]


router = APIRouter()

# TODO: Fix arguments (named or positional)
# TODO: Add :limit 1 to all get queries from cozo


@router.get("/agents/{agent_id}/tasks", tags=["tasks"])
async def list_tasks(
    agent_id: UUID4,
    x_developer_id: Annotated[UUID4, Depends(get_developer_id)],
) -> TaskList:
    query_results = list_tasks_query(agent_id, x_developer_id)
    return TaskList(
        items=[Task(**row.to_dict()) for _, row in query_results.iterrows()]
    )


@router.post("/agents/{agent_id}/tasks", status_code=HTTP_201_CREATED, tags=["tasks"])
async def create_task(
    request: CreateTask,
    agent_id: UUID4,
    x_developer_id: Annotated[UUID4, Depends(get_developer_id)],
) -> ResourceCreatedResponse:
    task_id = uuid4()

    # TODO: Do thorough validation of the task spec

    workflows = [
        {"name": "main", "steps": request.main},
    ] + [{"name": name, "steps": steps} for name, steps in request.model_extra]

    resp: pd.DataFrame = create_task_query(
        agent_id=agent_id,
        task_id=task_id,
        developer_id=x_developer_id,
        name=request.name,
        description=request.description,
        input_schema=request.input_schema,
        tools_available=request.tools_available,
        workflows=workflows,
    )
    return ResourceCreatedResponse(
        id=resp["task_id"][0], created_at=resp["created_at"][0]
    )


@router.get("/agents/{agent_id}/tasks/{task_id}", tags=["tasks"])
async def get_task(
    task_id: UUID4,
    agent_id: UUID4,
    x_developer_id: Annotated[UUID4, Depends(get_developer_id)],
) -> Task:
    try:
        resp = [
            row.to_dict()
            for _, row in get_task_query(agent_id, task_id, x_developer_id).iterrows()
        ][0]

        return Task(**resp)
    except (IndexError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    except QueryException as e:
        if e.code == "transact::assertion_failure":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        raise


@router.post(
    "/agents/{agent_id}/tasks/{task_id}/executions",
    status_code=HTTP_201_CREATED,
    tags=["tasks"],
)
async def create_task_execution(
    agent_id: UUID4,
    task_id: UUID4,
    request: CreateExecution,
    x_developer_id: Annotated[UUID4, Depends(get_developer_id)],
) -> ResourceCreatedResponse:
    # TODO: Do thorough validation of the input against task input schema
    # DO NOT let the user specify the status

    resp = create_execution_query(
        agent_id=agent_id,
        task_id=task_id,
        execution_id=uuid4(),
        developer_id=x_developer_id,
        status=request.status,
        arguments=request.arguments,
    )
    return ResourceCreatedResponse(
        id=resp["execution_id"][0], created_at=resp["created_at"][0]
    )


@router.get("/agents/{agent_id}/tasks/{task_id}/executions", tags=["tasks"])
async def list_task_executions(
    agent_id: UUID4,
    task_id: UUID4,
    x_developer_id: Annotated[UUID4, Depends(get_developer_id)],
) -> ExecutionList:
    res = list_task_executions_query(agent_id, task_id, x_developer_id)
    return ExecutionList(
        items=[Execution(**row.to_dict()) for _, row in res.iterrows()]
    )


@router.get("/tasks/{task_id}/executions/{execution_id}")
async def get_execution(task_id: UUID4, execution_id: UUID4) -> Execution:
    try:
        res = [
            row.to_dict()
            for _, row in get_execution_query(task_id, execution_id).iterrows()
        ][0]
        return Execution(**res)
    except (IndexError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found",
        )


# @router.get("/tasks/{task_id}/executions/{execution_id}/status", tags=["tasks"])
# async def get_task_execution_status(
#     task_id: UUID4,
#     execution_id: UUID4,
# ) -> Literal["queued", "starting", "running", "waiting_for_input", "success", "failed"]:
#     try:
#         res = [
#             row.to_dict()
#             for _, row in get_execution_status_query(task_id, execution_id).iterrows()
#         ][0]
#         return res["status"]
#     except (IndexError, KeyError):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Execution not found",
#         )


@router.get("/executions/{execution_id}/transitions/{transition_id}")
async def get_execution_transition(
    execution_id: UUID4,
    transition_id: UUID4,
) -> ExecutionTransition:
    try:
        res = [
            row.to_dict()
            for _, row in get_execution_transition_query(
                execution_id, transition_id
            ).iterrows()
        ][0]
        return ExecutionTransition(**res)
    except (IndexError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transition not found",
        )


# TODO: Later; for resuming waiting transitions
# TODO: Ask for a task token to resume a waiting transition
@router.put("/executions/{execution_id}/transitions/{transition_id}")
async def update_execution_transition(
    execution_id: UUID4, transition_id: UUID4, request
) -> ResourceUpdatedResponse:
    # try:
    #     resp = update_execution_transition_query(execution_id, transition_id, request)

    # OpenAPI Model doesn't have update execution transition

    raise NotImplementedError("Not implemented yet")


@router.get("/executions/{execution_id}/transitions")
async def list_execution_transitions(execution_id: UUID4) -> ExecutionTransitionList:
    res = list_execution_transition_query(execution_id)
    return ExecutionTransitionList(
        items=[ExecutionTransition(**row.to_dict()) for _, row in res.iterrows()]
    )
