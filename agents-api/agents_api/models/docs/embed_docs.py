from uuid import UUID

import pandas as pd

from ...clients.cozo import client


def embed_docs_snippets_query(
    doc_id: UUID,
    snippet_indices: list[int],
    embeddings: list[list[float]],
) -> pd.DataFrame:
    doc_id = str(doc_id)
    assert len(snippet_indices) == len(embeddings)

    records = "\n".join(
        [
            f'[to_uuid("{doc_id}"), {snippet_idx}, vec({embedding})],'
            for snippet_idx, embedding in zip(snippet_indices, embeddings)
        ]
    )

    query = f"""
    {{
        ?[doc_id, snippet_idx, embedding] <- [
            {records}
        ]

        :update information_snippets {{
            doc_id,
            snippet_idx,
            embedding,
        }}
        :returning
    }}"""

    return client.run(query)
