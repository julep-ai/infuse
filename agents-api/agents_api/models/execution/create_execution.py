from uuid import UUID, uuid4

from beartype import beartype


from ...autogen.openapi_model import Execution, CreateExecutionRequest
from ...common.utils.cozo import cozo_process_mutate_data
from ..utils import (
    cozo_query,
    verify_developer_id_query,
    verify_developer_owns_resource_query,
    wrap_in_class,
)


@wrap_in_class(
    Execution,
    one=True,
    transform=lambda d: {"id": d["execution_id"], **d},
)
@cozo_query
@beartype
def create_execution(
    *,
    developer_id: UUID,
    task_id: UUID,
    execution_id: UUID | None = None,
    data: CreateExecutionRequest,
) -> tuple[str, dict]:
    execution_id = execution_id or uuid4()

    developer_id = str(developer_id)
    task_id = str(task_id)
    execution_id = str(execution_id)

    data.metadata = data.metadata or {}
    execution_data = data.model_dump()

    columns, values = cozo_process_mutate_data(
        {
            **execution_data,
            "task_id": task_id,
            "execution_id": execution_id,
        }
    )

    insert_query = f"""
    ?[{columns}] <- $values

    :insert executions {{
        {columns}
    }}

    :returning
    """

    queries = [
        verify_developer_id_query(developer_id),
        verify_developer_owns_resource_query(
            developer_id,
            "tasks",
            task_id=task_id,
            parents=[("agents", "agent_id")],
        ),
        insert_query,
    ]

    query = "}\n\n{\n".join(queries)
    query = f"{{ {query} }}"

    return (query, {"values": values})
