from uuid import UUID

from beartype import beartype
from temporalio import activity

from ..autogen.openapi_model import Entry

# from agents_api.models.entry.entries_summarization import get_toplevel_entries_query

# TODO: Reimplement truncation queries
# SCRUM-5


def get_extra_entries(messages: list[Entry], token_count_threshold: int) -> list[UUID]:
    raise NotImplementedError()

    if not len(messages):
        return messages

    _token_cnt, _offset = 0, 0
    # if messages[0].role == Role.system:
    #     token_cnt, offset = messages[0].token_count, 1

    # for m in reversed(messages[offset:]):
    #     token_cnt += m.token_count
    #     if token_cnt < token_count_threshold:
    #         continue
    #     else:
    #         result.append(m.id)

    # return result


# TODO: Reimplement truncation activities
# SCRUM-6
@activity.defn
@beartype
async def truncation(session_id: str, token_count_threshold: int) -> None:
    session_id = UUID(session_id)

    # delete_entries(
    #     get_extra_entries(
    #         [
    #             Entry(
    #                 entry_id=row["entry_id"],
    #                 session_id=session_id,
    #                 source=row["source"],
    #                 role=Role(row["role"]),
    #                 name=row["name"],
    #                 content=row["content"],
    #                 created_at=row["created_at"],
    #                 timestamp=row["timestamp"],
    #             )
    #             for _, row in get_toplevel_entries_query(
    #                 session_id=session_id
    #             ).iterrows()
    #         ],
    #         token_count_threshold,
    #     ),
    # )
