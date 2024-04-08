from typing import Literal
from uuid import UUID


def ensure_owner_exists_query(
    owner_type: Literal["user", "agent"],
    owner_id: UUID,
):
    owner_id = str(owner_id)

    return f"""{{
        input[{owner_type}_id] <- [[to_uuid("{owner_id}")]]

        ?[
            {owner_type}_id,
        ] := input[{owner_type}_id],
            *{owner_type}s {{
                {owner_type}_id,
            }}
    }}"""


def list_docs_snippets_by_owner_query(
    owner_type: Literal["user", "agent"],
    owner_id: UUID,
):
    owner_id = str(owner_id)

    return f"""
    {{
        input[{owner_type}_id] <- [[to_uuid("{owner_id}")]]

        ?[
            {owner_type}_id,
            doc_id,
            title,
            snippet,
            snippet_idx,
            created_at,
            metadata,
        ] := input[{owner_type}_id],
            *{owner_type}_docs {{
                {owner_type}_id,
                doc_id,
                created_at,
                metadata,
            }},
            *information_snippets {{
                doc_id,
                snippet_idx,
                title,
                snippet,
            }}
    }}"""
