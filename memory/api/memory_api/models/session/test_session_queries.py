# Tests for session queries
from pycozo import Client
from uuid import uuid4
from ward import skip, test

from ..agent.create_agent import create_agent_query
from ..agent.schema import init as init_agent
from ..user.create_user import create_user_query
from ..user.schema import init as init_user

from .create_session import create_session_query
from .get_session import get_session_query
from .list_sessions import list_sessions_query
from .session_data import get_session_data, session_data_query
from .schema import init


def cozo_client():
    # Create a new client for each test
    # and initialize the schema.
    client = Client()

    init(client)

    return client


@test("create session")
def _():
    client = cozo_client()
    session_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    situation = "test situation"

    query = create_session_query(
        session_id=session_id,
        user_id=user_id,
        agent_id=agent_id,
        situation="test session about",
    )

    result = client.run(query)


@test("get session not exists")
def _():
    client = cozo_client()
    session_id = uuid4()

    query = get_session_query(
        session_id=session_id,
    )

    result = client.run(query)

    assert len(result["session_id"]) == 0


@test("get session exists")
def _():
    client = cozo_client()
    session_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    situation = "test situation"

    query = create_session_query(
        session_id=session_id,
        user_id=user_id,
        agent_id=agent_id,
        situation="test session about",
    )

    client.run(query)

    query = get_session_query(
        session_id=session_id,
    )

    result = client.run(query)

    assert len(result["session_id"]) == 1


@test("get session data")
def _():
    # Setup client for user and agent
    client = cozo_client()
    init_agent(client)
    init_user(client)

    session_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()

    # Create a user
    client.run(create_user_query(
        user_id=user_id,
        about="test user about",
        name="test user name",
    ))

    # Create an agent
    client.run(create_agent_query(
        agent_id=agent_id,
        about="test agent about",
        name="test agent name",
    ))

    # Create a session
    situation = "test situation"

    query = create_session_query(
        session_id=session_id,
        user_id=user_id,
        agent_id=agent_id,
        situation="test session about",
    )

    client.run(query)

    query = session_data_query(
        session_id=session_id,
    )

    result = client.run(query)

    assert len(result["user_about"]) == 1


@test("get session data using get_session_data")
def _():
    # Setup client for user and agent
    client = cozo_client()
    init_agent(client)
    init_user(client)

    session_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()

    # Create a user
    client.run(create_user_query(
        user_id=user_id,
        about="test user about",
        name="test user name",
    ))

    # Create an agent
    client.run(create_agent_query(
        agent_id=agent_id,
        about="test agent about",
        name="test agent name",
    ))

    # Create a session
    situation = "test situation"

    query = create_session_query(
        session_id=session_id,
        user_id=user_id,
        agent_id=agent_id,
        situation="test session about",
    )

    client.run(query)

    session_data = get_session_data(
        session_id=session_id,
        client=client,
    )

    assert session_data is not None
    assert session_data.user_about == "test user about"


@test("list sessions")
def _():
    client = cozo_client()
    session_id = uuid4()

    query = list_sessions_query()

    result = client.run(query)

    assert len(result["session_id"]) == 0
