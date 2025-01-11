import asyncio
import logging
import os
import subprocess
from contextlib import asynccontextmanager, contextmanager
from unittest.mock import patch

from agents_api.worker.codec import pydantic_data_converter
from agents_api.worker.worker import create_worker
from fastapi.testclient import TestClient
from litellm.types.utils import ModelResponse
from temporalio.testing import WorkflowEnvironment
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.localstack import LocalStackContainer
from testcontainers.postgres import PostgresContainer

# Replicated here to prevent circular import
EMBEDDING_SIZE: int = 1024


@asynccontextmanager
async def patch_testing_temporal():
    # Set log level to ERROR to avoid spamming the console
    logger = logging.getLogger("temporalio")
    previous_log_level = logger.getEffectiveLevel()

    logger.setLevel(logging.ERROR)

    # Start a local Temporal environment
    async with await WorkflowEnvironment.start_time_skipping(
        data_converter=pydantic_data_converter
    ) as env:
        # Create a worker with our workflows and start it
        worker = create_worker(client=env.client)
        env.worker_task = asyncio.create_task(worker.run())

        # Mock the Temporal client
        mock_client = worker.client

        with patch("agents_api.clients.temporal.get_client") as mock_get_client:
            mock_get_client.return_value = mock_client

            # Yield the worker and the mock client <---
            yield worker, mock_get_client

        # Shutdown the worker
        await worker.shutdown()

    # Reset log level
    logger.setLevel(previous_log_level)


@asynccontextmanager
async def patch_http_client_with_temporal(*, postgres_pool, developer_id):
    async with patch_testing_temporal() as (_worker, mock_get_client):
        from agents_api.env import api_key, api_key_header_name
        from agents_api.web import app

        client = TestClient(app=app)
        app.state.postgres_pool = postgres_pool

        def make_request(method, url, **kwargs):
            headers = kwargs.pop("headers", {})
            headers = {
                **headers,
                "X-Developer-Id": str(developer_id),
                api_key_header_name: api_key,
            }

            return client.request(method, url, headers=headers, **kwargs)

        temporal_client = await mock_get_client()
        yield make_request, temporal_client


@contextmanager
def patch_embed_acompletion(output={"role": "assistant", "content": "Hello, world!"}):
    mock_model_response = ModelResponse(
        id="fake_id",
        choices=[
            {
                "message": output,
                "tool_calls": [],
                "created_at": 1,
                # finish_reason="stop",
            }
        ],
        created=0,
        object="text_completion",
    )

    with (
        patch("agents_api.clients.litellm.aembedding") as embed,
        patch("agents_api.clients.litellm.acompletion") as acompletion,
    ):
        embed.return_value = [[1.0] * EMBEDDING_SIZE]
        acompletion.return_value = mock_model_response

        yield embed, acompletion


@contextmanager
def patch_integration_service(output: dict = {"result": "ok"}):
    with patch(
        "agents_api.clients.integrations.run_integration_service"
    ) as run_integration_service:
        run_integration_service.return_value = output

        yield run_integration_service


@contextmanager
def get_pg_dsn(start_vectorizer: bool = False):
    with PostgresContainer("timescale/timescaledb-ha:pg17") as postgres:
        test_psql_url = postgres.get_connection_url()
        pg_dsn = f"postgres://{test_psql_url[22:]}?sslmode=disable"
        command = f"migrate -database '{pg_dsn}' -path ../memory-store/migrations/ up"
        process = subprocess.Popen(command, shell=True)
        process.wait()

        if not start_vectorizer:
            yield pg_dsn
            return

        # ELSE:
        with (
            DockerContainer("timescale/pgai-vectorizer-worker:latest")
            .with_network(postgres._network)  # noqa: SLF001
            .with_env(
                "PGAI_VECTORIZER_WORKER_DB_URL",
                pg_dsn.replace("localhost", postgres.get_container_host_ip()),
            )
            .with_env(
                "OPENAI_API_KEY",
                os.environ.get("OPENAI_API_KEY"),
            )
        ) as vectorizer:
            wait_for_logs(
                vectorizer,
                "finished processing vectorizer",
                predicate_streams_and=True,
                raise_on_exit=True,
                timeout=10,
            )

        print("Vectorizer worker started")

        yield pg_dsn


@contextmanager
def get_localstack():
    with LocalStackContainer(image="localstack/localstack:s3-latest").with_services(
        "s3"
    ) as localstack:
        yield localstack
