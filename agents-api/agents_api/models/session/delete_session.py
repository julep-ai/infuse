from uuid import UUID

import pandas as pd
from pycozo.client import Client as CozoClient

from ...clients.cozo import client


def delete_session_query(
    developer_id: UUID,
    session_id: UUID,
    client: CozoClient = client,
) -> pd.DataFrame:
    session_id = str(session_id)
    developer_id = str(developer_id)

    query = """
    {
        input[session_id] <- [[
            to_uuid($session_id),
        ]]

        ?[
            agent_id,
            user_id,
            session_id,
        ] :=
            input[session_id],
            *session_lookup{
                agent_id,
                user_id,
                session_id,
            }

        :delete session_lookup {
            agent_id,
            user_id,
            session_id,
        }
    } {
        input[developer_id, session_id] <- [[
            to_uuid($developer_id),
            to_uuid($session_id),
        ]]

        ?[developer_id, session_id, updated_at] :=
            input[developer_id, session_id],
            *sessions {
                developer_id, 
                session_id,
                updated_at,
            }

        :delete sessions {
            developer_id,
            session_id,
            updated_at,
        }
    }
    """

    return client.run(query, {"session_id": session_id, "developer_id": developer_id})
