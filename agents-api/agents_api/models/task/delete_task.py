from beartype import beartype

from uuid import UUID


from ...autogen.openapi_model import ResourceDeletedResponse
from ...common.utils.cozo import cozo_process_mutate_data
from ...common.utils.datetime import utcnow
from ..utils import (
    cozo_query,
    verify_developer_id_query,
    verify_developer_owns_resource_query,
    wrap_in_class,
)


@wrap_in_class(
    ResourceDeletedResponse,
    one=True,
    transform=lambda d: {
        "id": UUID(d.pop("task_id")),
        "jobs": [],
        "deleted_at": utcnow(),
        **d,
    },
)
@cozo_query
@beartype
def delete_task(
    *,
    developer_id: UUID,
    agent_id: UUID,
    task_id: UUID,
) -> tuple[str, dict]:
    delete_query = """
    input[agent_id, task_id] <- [[
        to_uuid($agent_id),
        to_uuid($task_id),
    ]]

    ?[agent_id, task_id, updated_at_ms] :=
        input[agent_id, task_id],
        *tasks{
            agent_id,
            task_id,
            updated_at_ms,
        }

    :delete tasks {
        agent_id,
        task_id,
        updated_at_ms,
    }

    :returning
    """

    queries = [
        verify_developer_id_query(developer_id),
        verify_developer_owns_resource_query(developer_id, "agents", agent_id=agent_id),
        delete_query,
    ]

    query = "}\n\n{\n".join(queries)
    query = f"{{ {query} }}"

    return (query, {"agent_id": str(agent_id), "task_id": str(task_id)})
