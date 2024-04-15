from ward import test

from julep.api.types import (
    Agent,
)

from .fixtures import (
    client,
    async_client,
    test_agent,
    test_agent_async,
    mock_agent,
    mock_agent_update,
)


@test("agents: agents.create")
def _(agent=test_agent):
    assert isinstance(agent, Agent)
    assert hasattr(agent, "created_at")
    assert agent.name == mock_agent["name"]
    assert agent.about == mock_agent["about"]


@test("agents: agents.get")
def _(client=client, agent=test_agent):
    response = client.agents.get(agent.id)
    assert isinstance(response, Agent)
    assert response.id == agent.id
    assert response.name == agent.name
    assert response.about == agent.about


@test("agents: async agents.create, agents.get, agents.update & agents.delete")
async def _(client=async_client, agent=test_agent_async):
    assert isinstance(agent, Agent)
    assert agent.name == mock_agent["name"]
    assert agent.about == mock_agent["about"]

    response = await client.agents.get(agent.id)
    assert isinstance(response, Agent)
    assert response.id == agent.id
    assert response.name == agent.name
    assert response.about == agent.about

    updated = await client.agents.update(agent_id=agent.id, **mock_agent_update)
    assert updated.name == mock_agent_update["name"]
    assert updated.about == mock_agent_update["about"]


@test("agents: agents.list")
def _(client=client, _=test_agent):
    response = client.agents.list()
    assert len(response) > 0
    assert isinstance(response[0], Agent)


@test("agents: async agents.list")
async def _(client=async_client, _=test_agent_async):
    response = await client.agents.list()
    assert len(response) > 0
    assert isinstance(response[0], Agent)


@test("agents: agents.update")
def _(client=client, agent=test_agent):
    response = client.agents.update(agent_id=agent.id, name=mock_agent_update["name"])

    assert isinstance(response, Agent)
    assert response.name == mock_agent_update["name"]


@test("agents: agents.update with overwrite")
def _(client=client, agent=test_agent):
    response = client.agents.update(
        agent_id=agent.id, overwrite=True, name="overwritten name"
    )

    assert isinstance(response, Agent)
    assert hasattr(response, "updated_at")
    assert response.name
    assert not response.about


@test("agents: agents.delete")
def _(client=client, agent=test_agent):
    response = client.agents.delete(agent.id)

    assert response is None
