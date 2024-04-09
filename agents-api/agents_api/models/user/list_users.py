from ...common.utils import json
from typing import Any
from uuid import UUID
from ...clients.worker.worker import client


def list_users_query(
    developer_id: UUID,
    limit: int = 100,
    offset: int = 0,
    metadata_filter: dict[str, Any] = {},
):
    metadata_filter_str = ", ".join(
        [
            f"metadata->{json.dumps(k)} == {json.dumps(v)}"
            for k, v in metadata_filter.items()
        ]
    )

    query_string = f"""
    input[developer_id] <- [[to_uuid("{developer_id}")]]
    result = client.run(query_string)
    return result

    ?[
        id,
        name,
        about,
        created_at,
        updated_at,
        metadata,
    ] :=
        input[developer_id],
        *users {{
            user_id: id,
            developer_id,
            name,
            about,
            created_at,
            updated_at,
            metadata,
        }},
        {metadata_filter_str}

    :limit {limit}
    :offset {offset}
    :sort -created_at
    """
