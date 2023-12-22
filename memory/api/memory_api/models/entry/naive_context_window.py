# Phase 1

naive_context_window_query = """
# In this query, we are going to collect all session entries for a `session_id`.
# - filter(source=="api_request" or source=="api_response")

    input[session_id] <- [[
        to_uuid("{session_id}"),
    ]]

    ?[role, name, content, token_count, created_at] :=
        input[session_id],
        *entries{{
            session_id,
            source,
            role,
            name,
            content,
            token_count,
            created_at,
        }},
        source == "api_request" || source == "api_response",

    :sort -created_at
"""
