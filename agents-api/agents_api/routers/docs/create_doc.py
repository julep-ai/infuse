from typing import Annotated
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, Depends
from starlette.status import HTTP_201_CREATED
from temporalio.client import Client as TemporalClient

from ...activities.types import EmbedDocsPayload
from ...autogen.openapi_model import CreateDocRequest, Doc, ResourceCreatedResponse
from ...clients import temporal
from ...common.retry_policies import DEFAULT_RETRY_POLICY
from ...dependencies.developer_id import get_developer_id
from ...env import temporal_task_queue, testing
from ...models.docs.create_doc import create_doc as create_doc_query
from .router import router


async def run_embed_docs_task(
    *,
    developer_id: UUID,
    doc_id: UUID,
    title: str,
    content: list[str],
    embed_instruction: str | None = None,
    job_id: UUID,
    background_tasks: BackgroundTasks,
    client: TemporalClient | None = None,
):
    from ...workflows.embed_docs import EmbedDocsWorkflow

    client = client or (await temporal.get_client())

    embed_payload = EmbedDocsPayload(
        developer_id=developer_id,
        doc_id=doc_id,
        content=content,
        title=title,
        embed_instruction=embed_instruction,
    )

    handle = await client.start_workflow(
        EmbedDocsWorkflow.run,
        embed_payload,
        task_queue=temporal_task_queue,
        id=str(job_id),
        retry_policy=DEFAULT_RETRY_POLICY,
    )

    # TODO: Remove this conditional once we have a way to run workflows in
    #       a test environment.
    if not testing:
        background_tasks.add_task(handle.result)

    return handle


@router.post("/users/{user_id}/docs", status_code=HTTP_201_CREATED, tags=["docs"])
async def create_user_doc(
    user_id: UUID,
    data: CreateDocRequest,
    x_developer_id: Annotated[UUID, Depends(get_developer_id)],
    background_tasks: BackgroundTasks,
) -> ResourceCreatedResponse:
    doc: Doc = create_doc_query(
        developer_id=x_developer_id,
        owner_type="user",
        owner_id=user_id,
        data=data,
    )

    embed_job_id = uuid4()

    await run_embed_docs_task(
        developer_id=x_developer_id,
        doc_id=doc.id,
        title=doc.title,
        content=doc.content,
        embed_instruction=data.embed_instruction,
        job_id=embed_job_id,
        background_tasks=background_tasks,
    )

    return ResourceCreatedResponse(
        id=doc.id, created_at=doc.created_at, jobs=[embed_job_id]
    )


@router.post("/agents/{agent_id}/docs", status_code=HTTP_201_CREATED, tags=["docs"])
async def create_agent_doc(
    agent_id: UUID,
    data: CreateDocRequest,
    x_developer_id: Annotated[UUID, Depends(get_developer_id)],
    background_tasks: BackgroundTasks,
) -> ResourceCreatedResponse:
    doc: Doc = create_doc_query(
        developer_id=x_developer_id,
        owner_type="agent",
        owner_id=agent_id,
        data=data,
    )

    embed_job_id = uuid4()

    await run_embed_docs_task(
        developer_id=x_developer_id,
        doc_id=doc.id,
        title=doc.title,
        content=doc.content,
        embed_instruction=data.embed_instruction,
        job_id=embed_job_id,
        background_tasks=background_tasks,
    )

    return ResourceCreatedResponse(
        id=doc.id, created_at=doc.created_at, jobs=[embed_job_id]
    )
