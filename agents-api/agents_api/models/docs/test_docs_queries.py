# Tests for entry queries
from uuid import uuid4

from cozo_migrate.api import apply, init
from pycozo import Client
from ward import test

from .create_doc import create_doc
from .delete_doc import delete_doc
from .embed_snippets import embed_snippets
from .get_doc import get_doc
from .list_docs import list_docs
from .search_docs import search_docs_by_embedding

EMBEDDING_SIZE: int = 1024


def cozo_client(migrations_dir: str = "./migrations"):
    # Create a new client for each test
    # and initialize the schema.
    client = Client()

    init(client)
    apply(client, migrations_dir=migrations_dir, all_=True)

    return client


@test("model: create docs")
def _():
    client = cozo_client()

    for owner_type in ("user", "agent"):
        owner_id = uuid4()
        doc_id = uuid4()
        developer_id = uuid4()

        create_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            data={"title": "Hello", "content": ["World"]},
            client=client,
        )


@test("model: get docs")
def _():
    client = cozo_client()

    for owner_type in ("user", "agent"):
        owner_id = uuid4()
        doc_id = uuid4()
        developer_id = uuid4()

        create_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            data={"title": "Hello", "content": ["World"]},
            client=client,
        )

        result = get_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            doc_id=doc_id,
            client=client,
        )

        assert len(result["id"]) == 1, "Only 1 should have been found"


@test("model: delete docs")
def _():
    client = cozo_client()

    for owner_type in ("user", "agent"):
        owner_id = uuid4()
        doc_id = uuid4()
        developer_id = uuid4()

        create_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            data={"title": "Hello", "content": ["World"]},
            client=client,
        )

        delete_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            client=client,
        )

        result = get_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            doc_id=doc_id,
            client=client,
        )

        assert len(result["id"]) == 0, "Delete operation found the row"


@test("model: list docs")
def _():
    client = cozo_client()

    for owner_type in ("user", "agent"):
        owner_id = uuid4()
        doc_id = uuid4()
        developer_id = uuid4()

        create_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            data={"title": "Hello", "content": ["World"]},
            client=client,
        )

        result = list_docs(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            client=client,
        )

        assert len(result["id"]) == 1, "Only 1 should have been found"


@test("model: search docs")
def _():
    client = cozo_client()

    for owner_type in ("user", "agent"):
        owner_id = uuid4()
        doc_id = uuid4()
        developer_id = uuid4()

        create_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            data={"title": "Hello", "content": ["World"]},
            client=client,
        )

        ### Add embedding to the snippet
        embed_snippets(
            developer_id=developer_id,
            doc_id=doc_id,
            snippet_indices=[0],
            embeddings=[[1.0] * EMBEDDING_SIZE],
            client=client,
        )

        ### Search
        query_embedding = [0.99] * EMBEDDING_SIZE

        result = search_docs_by_embedding(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            query_embedding=query_embedding,
            client=client,
        )

        assert len(result["id"]) == 1, "Only 1 should have been found"


@test("model: embed docs")
def _():
    client = cozo_client()

    for owner_type in ("user", "agent"):
        owner_id = uuid4()
        doc_id = uuid4()
        developer_id = uuid4()

        snippets = [
            "Hello World",
            "Hello Banana",
            "Hello Apple",
        ]

        create_doc(
            developer_id=developer_id,
            owner_type=owner_type,
            owner_id=owner_id,
            doc_id=doc_id,
            data={"title": "Hi", "content": snippets},
            client=client,
        )

        ### Add embedding to the snippet
        snippet_indices = [*range(len(snippets))]

        embeddings = [[1.0] * EMBEDDING_SIZE for _ in snippets]

        embed_snippets(
            developer_id=developer_id,
            doc_id=doc_id,
            snippet_indices=snippet_indices,
            embeddings=embeddings,
            client=client,
        )
