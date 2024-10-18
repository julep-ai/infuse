from typing import Annotated, Optional
from uuid import UUID, uuid4

from fastapi import BackgroundTasks, Depends, Header
from starlette.status import HTTP_201_CREATED

from ...autogen.openapi_model import (
    ChatInput,
    ChatResponse,
    ChunkChatResponse,
    CreateEntryRequest,
    MessageChatResponse,
)
from ...clients import litellm
from ...common.protocol.developers import Developer
from ...common.protocol.sessions import ChatContext
from ...common.utils.datetime import utcnow
from ...common.utils.template import render_template
from ...dependencies.developer_id import get_developer_data
from ...models.chat.gather_messages import gather_messages
from ...models.chat.prepare_chat_context import prepare_chat_context
from ...models.entry.create_entries import create_entries
from .metrics import total_tokens_per_user
from .router import router


@router.post(
    "/sessions/{session_id}/chat",
    status_code=HTTP_201_CREATED,
    tags=["sessions", "chat"],
)
async def chat(
    developer: Annotated[Developer, Depends(get_developer_data)],
    session_id: UUID,
    chat_input: ChatInput,
    background_tasks: BackgroundTasks,
    x_custom_api_key: Optional[str] = Header(None, alias="X-Custom-Api-Key"),
) -> ChatResponse:
    if chat_input.stream:
        raise NotImplementedError("Streaming is not yet implemented")

    # First get the chat context
    chat_context: ChatContext = prepare_chat_context(
        developer_id=developer.id,
        session_id=session_id,
    )

    # Merge the settings and prepare environment
    chat_context.merge_settings(chat_input)
    settings: dict = chat_context.settings.model_dump()

    # Get the past messages and doc references
    past_messages, doc_references = await gather_messages(
        developer=developer,
        session_id=session_id,
        chat_context=chat_context,
        chat_input=chat_input,
    )

    # Prepare the environment
    env: dict = chat_context.get_chat_environment()
    env["docs"] = [
        dict(
            title=ref.title,
            content=[snippet.content for snippet in ref.snippets],
        )
        for ref in doc_references
    ]

    # Render the system message
    if situation := chat_context.session.situation:
        system_message = dict(
            role="system",
            content=situation,
        )

        system_messages: list[dict] = await render_template(
            [system_message], variables=env
        )
        past_messages = system_messages + past_messages

    # Render the incoming messages
    new_raw_messages = [msg.model_dump() for msg in chat_input.messages]

    if chat_context.session.render_templates:
        new_messages = await render_template(new_raw_messages, variables=env)
    else:
        new_messages = new_raw_messages

    # Combine the past messages with the new messages
    messages = past_messages + new_messages

    # Get the tools
    tools = settings.get("tools") or chat_context.get_active_tools()

    # FIXME: Truncate chat messages in the chat context
    # SCRUM-7
    if chat_context.session.context_overflow == "truncate":
        # messages = messages[-settings["max_tokens"] :]
        raise NotImplementedError("Truncation is not yet implemented")

    # FIXME: Hotfix for datetime not serializable. Needs investigation
    messages = [
        msg.model_dump() if hasattr(msg, "model_dump") else msg for msg in messages
    ]

    messages = [
        dict(role=m["role"], content=m["content"], user=m.get("user")) for m in messages
    ]

    # Get the response from the model
    model_response = await litellm.acompletion(
        messages=messages,
        tools=tools or None,
        user=str(developer.id),  # For tracking usage
        tags=developer.tags,  # For filtering models in litellm
        custom_api_key=x_custom_api_key,
        **settings,
    )

    # Save the input and the response to the session history
    if chat_input.save:
        new_entries = [
            CreateEntryRequest.from_model_input(
                model=settings["model"], **msg, source="api_request"
            )
            for msg in new_messages
        ]

        # Add the response to the new entries
        # FIXME: We need to save all the choices
        new_entries.append(
            CreateEntryRequest.from_model_input(
                model=settings["model"],
                **model_response.choices[0].model_dump()["message"],
                source="api_response",
            )
        )
        background_tasks.add_task(
            create_entries,
            developer_id=developer.id,
            session_id=session_id,
            data=new_entries,
            mark_session_as_updated=True,
        )

    # Adaptive context handling
    jobs = []
    if chat_context.session.context_overflow == "adaptive":
        # FIXME: Start the adaptive context workflow
        # SCRUM-8

        # jobs = [await start_adaptive_context_workflow]
        raise NotImplementedError("Adaptive context is not yet implemented")

    # Return the response
    # FIXME: Implement streaming for chat
    chat_response_class = (
        ChunkChatResponse if chat_input.stream else MessageChatResponse
    )
    chat_response: ChatResponse = chat_response_class(
        id=uuid4(),
        created_at=utcnow(),
        jobs=jobs,
        docs=doc_references,
        usage=model_response.usage.model_dump(),
        choices=[choice.model_dump() for choice in model_response.choices],
    )

    total_tokens_per_user.labels(str(developer.id)).inc(
        amount=chat_response.usage.total_tokens or 0
    )

    return chat_response
