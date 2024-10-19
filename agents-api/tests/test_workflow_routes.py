# Tests for task queries

from uuid import uuid4

from ward import test

from tests.fixtures import cozo_client, test_agent, test_developer_id
from tests.utils import patch_http_client_with_temporal


@test("workflow route: evaluate step single")
async def _(
    cozo_client=cozo_client,
    developer_id=test_developer_id,
    agent=test_agent,
):
    agent_id = str(agent.id)
    task_id = str(uuid4())

    async with patch_http_client_with_temporal(
        cozo_client=cozo_client, developer_id=developer_id
    ) as (
        make_request,
        client,
    ):
        task_data = {
            "name": "test task",
            "description": "test task about",
            "input_schema": {"type": "object", "additionalProperties": True},
            "main": [{"evaluate": {"hello": '"world"'}}],
        }

        make_request(
            method="POST",
            url=f"/agents/{agent_id}/tasks/{task_id}",
            json=task_data,
        ).raise_for_status()

        execution_data = dict(input={"test": "input"})

        make_request(
            method="POST",
            url=f"/tasks/{task_id}/executions",
            json=execution_data,
        ).raise_for_status()


@test("workflow route: evaluate step single with yaml")
async def _(
    cozo_client=cozo_client,
    developer_id=test_developer_id,
    agent=test_agent,
):
    agent_id = str(agent.id)

    async with patch_http_client_with_temporal(
        cozo_client=cozo_client, developer_id=developer_id
    ) as (
        make_request,
        client,
    ):
        task_data = """
name: test task
description: test task about
input_schema:
  type: object
  additionalProperties: true

main:
  - evaluate:
      hello: '"world"'
"""

        result = (
            make_request(
                method="POST",
                url=f"/agents/{agent_id}/tasks",
                content=task_data.encode("utf-8"),
                headers={"Content-Type": "text/yaml"},
            )
            .raise_for_status()
            .json()
        )

        task_id = result["id"]

        execution_data = dict(input={"test": "input"})

        make_request(
            method="POST",
            url=f"/tasks/{task_id}/executions",
            json=execution_data,
        ).raise_for_status()


@test("workflow route: create or update: evaluate step single with yaml")
async def _(
    cozo_client=cozo_client,
    developer_id=test_developer_id,
    agent=test_agent,
):
    agent_id = str(agent.id)
    task_id = str(uuid4())

    async with patch_http_client_with_temporal(
        cozo_client=cozo_client, developer_id=developer_id
    ) as (
        make_request,
        client,
    ):
        task_data = """
name: test task
description: test task about
input_schema:
  type: object
  additionalProperties: true

main:
  - evaluate:
      hello: '"world"'
"""

        make_request(
            method="POST",
            url=f"/agents/{agent_id}/tasks/{task_id}",
            content=task_data.encode("utf-8"),
            headers={"Content-Type": "text/yaml"},
        ).raise_for_status()

        execution_data = dict(input={"test": "input"})

        make_request(
            method="POST",
            url=f"/tasks/{task_id}/executions",
            json=execution_data,
        ).raise_for_status()
