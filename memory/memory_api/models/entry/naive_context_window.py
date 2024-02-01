from uuid import UUID


def naive_context_window_query(session_id: UUID):
    session_id = str(session_id)

    return f"""
    {{
        # In this query, we are going to collect all session entries for a `session_id`.
        # - filter(source=="api_request" or source=="api_response")

        input[session_id] <- [[
            to_uuid("{session_id}"),
        ]]

        ?[role, name, content, token_count, created_at, timestamp] :=
            input[session_id],
            *entries{{
                session_id,
                source,
                role,
                name,
                content,
                token_count,
                created_at,
                timestamp,
            }},
            source == "api_request" || source == "api_response",

        :sort timestamp
    }}
    """
