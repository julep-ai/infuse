# Tests for execution queries
from uuid import uuid4

from cozo_migrate.api import init, apply
from pycozo import Client
from ward import test

from .create_execution import create_execution_query
from .get_execution_status import get_execution_status_query
from .get_execution import get_execution_query
from .list_executions import list_task_executions_query
from .update_execution_status import update_execution_status_query
from .create_execution_transition import create_execution_transition_query
from .get_execution_transition import get_execution_transition_query
from .list_execution_transitions import list_execution_transitions_query
from .update_execution_transition import update_execution_transition_query


def cozo_client(migrations_dir: str = "./migrations"):
    # Create a new client for each test
    # and initialize the schema.
    client = Client()

    init(client)
    apply(client, migrations_dir=migrations_dir, all_=True)

    return client


@test("model: create execution")
def _():
    client = cozo_client()
    developer_id = uuid4()
    agent_id = uuid4()
    task_id = uuid4()
    execution_id = uuid4()

    create_execution_query(
        developer_id=developer_id,
        agent_id=agent_id,
        task_id=task_id,
        execution_id=execution_id,
        arguments={"input": "test"},
        client=client,
    )


@test("model: get execution")
def _():
    client = cozo_client()
    developer_id = uuid4()
    agent_id = uuid4()
    task_id = uuid4()
    execution_id = uuid4()

    create_execution_query(
        developer_id=developer_id,
        agent_id=agent_id,
        task_id=task_id,
        execution_id=execution_id,
        arguments={"input": "test"},
        client=client,
    )

    result = get_execution_query(
        task_id=task_id, execution_id=execution_id, client=client
    )

    assert len(result["status"]) == 1
    assert result["status"][0] == "queued"


@test("model: get execution status")
def _():
    client = cozo_client()
    developer_id = uuid4()
    agent_id = uuid4()
    task_id = uuid4()
    execution_id = uuid4()

    create_execution_query(
        developer_id=developer_id,
        agent_id=agent_id,
        task_id=task_id,
        execution_id=execution_id,
        arguments={"input": "test"},
        client=client,
    )

    result = get_execution_status_query(
        task_id=task_id, execution_id=execution_id, client=client
    )

    assert len(result["status"]) == 1
    assert result["status"][0] == "queued"


@test("model: list executions empty")
def _():
    client = cozo_client()
    developer_id = uuid4()
    agent_id = uuid4()
    task_id = uuid4()

    result = list_task_executions_query(
        task_id=task_id, agent_id=agent_id, developer_id=developer_id, client=client
    )

    assert len(result) == 0


@test("model: list executions")
def _():
    client = cozo_client()
    developer_id = uuid4()
    agent_id = uuid4()
    task_id = uuid4()
    execution_id = uuid4()

    create_execution_query(
        developer_id=developer_id,
        agent_id=agent_id,
        task_id=task_id,
        execution_id=execution_id,
        arguments={"input": "test"},
        client=client,
    )

    result = list_task_executions_query(
        task_id=task_id, agent_id=agent_id, developer_id=developer_id, client=client
    )

    assert len(result["status"]) == 1
    assert result["status"][0] == "queued"


@test("model: update execution status")
def _():
    client = cozo_client()
    developer_id = uuid4()
    agent_id = uuid4()
    task_id = uuid4()
    execution_id = uuid4()

    create_execution_query(
        developer_id=developer_id,
        agent_id=agent_id,
        task_id=task_id,
        execution_id=execution_id,
        arguments={"input": "test"},
        client=client,
    )

    result = update_execution_status_query(
        task_id=task_id, execution_id=execution_id, status="running", client=client
    )

    updated_rows = result[result["_kind"] == "inserted"].reset_index()
    assert len(updated_rows) == 1
    assert updated_rows["status"][0] == "running"


@test("model: create execution transition")
def _():
    client = cozo_client()
    developer_id = uuid4()
    execution_id = uuid4()
    transition_id = uuid4()

    create_execution_transition_query(
        developer_id=developer_id,
        execution_id=execution_id,
        transition_id=transition_id,
        type_="step",
        from_=("test", 1),
        to=("test", 2),
        output={"input": "test"},
        client=client,
    )


@test("model: get execution transition")
def _():
    client = cozo_client()
    developer_id = uuid4()
    execution_id = uuid4()
    transition_id = uuid4()

    create_execution_transition_query(
        developer_id=developer_id,
        execution_id=execution_id,
        transition_id=transition_id,
        type_="step",
        from_=("test", 1),
        to=("test", 2),
        output={"input": "test"},
        client=client,
    )

    result = get_execution_transition_query(
        execution_id=execution_id, transition_id=transition_id, client=client
    )

    assert len(result["type"]) == 1


@test("model: list execution transitions")
def _():
    client = cozo_client()
    developer_id = uuid4()
    execution_id = uuid4()
    transition_id = uuid4()

    create_execution_transition_query(
        developer_id=developer_id,
        execution_id=execution_id,
        transition_id=transition_id,
        type_="step",
        from_=("test", 1),
        to=("test", 2),
        output={"input": "test"},
        client=client,
    )

    result = list_execution_transitions_query(execution_id=execution_id, client=client)

    assert len(result["type"]) == 1


@test("model: update execution transitions")
def _():
    client = cozo_client()
    developer_id = uuid4()
    execution_id = uuid4()
    transition_id = uuid4()

    create_execution_transition_query(
        developer_id=developer_id,
        execution_id=execution_id,
        transition_id=transition_id,
        type_="step",
        from_=("test", 1),
        to=("test", 2),
        output={"input": "test"},
        client=client,
    )

    result = update_execution_transition_query(
        execution_id=execution_id,
        transition_id=transition_id,
        type="finished",
        client=client,
    )

    updated_rows = result[result["_kind"] == "inserted"].reset_index()
    assert len(updated_rows) == 1
    assert updated_rows["type"][0] == "finished"
