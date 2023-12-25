from uuid import UUID


def get_user_query(user_id: UUID):
    user_id = str(user_id)

    return f"""
    input[user_id] <- [[to_uuid("{user_id}")]]

    ?[
        user_id,
        name,
        about,
        created_at,
    ] := input[user_id],
        *users {{
            user_id,
            name,
            about,
            created_at,
        }}"""
