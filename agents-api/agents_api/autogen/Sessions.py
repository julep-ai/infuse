# generated by datamodel-codegen:
#   filename:  openapi-1.0.0.yaml

from __future__ import annotations

from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel, StrictBool


class CreateSessionRequest(BaseModel):
    """
    Payload for creating a session
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    user: UUID | None = None
    """
    User ID of user associated with this session
    """
    users: list[UUID] | None = None
    agent: UUID | None = None
    """
    Agent ID of agent associated with this session
    """
    agents: list[UUID] | None = None
    situation: str = '{%- if agent.name -%}\nYou are {{agent.name}}.{{" "}}\n{%- endif -%}\n\n{%- if agent.about -%}\nAbout you: {{agent.about}}.{{" "}}\n{%- endif -%}\n\n{%- if user -%}\nYou are talking to a user\n  {%- if user.name -%}{{" "}} and their name is {{user.name}}\n    {%- if user.about -%}. About the user: {{user.about}}.{%- else -%}.{%- endif -%}\n  {%- endif -%}\n{%- endif -%}\n\n{{NEWLINE+NEWLINE}}\n\n{%- if agent.instructions -%}\nInstructions:{{NEWLINE}}\n  {%- if agent.instructions is string -%}\n    {{agent.instructions}}{{NEWLINE}}\n  {%- else -%}\n    {%- for instruction in agent.instructions -%}\n      - {{instruction}}{{NEWLINE}}\n    {%- endfor -%}\n  {%- endif -%}\n  {{NEWLINE}}\n{%- endif -%}\n\n{%- if docs -%}\nRelevant documents:{{NEWLINE}}\n  {%- for doc in docs -%}\n    {{doc.title}}{{NEWLINE}}\n    {%- if doc.content is string -%}\n      {{doc.content}}{{NEWLINE}}\n    {%- else -%}\n      {%- for snippet in doc.content -%}\n        {{snippet}}{{NEWLINE}}\n      {%- endfor -%}\n    {%- endif -%}\n    {{"---"}}\n  {%- endfor -%}\n{%- endif -%}'
    """
    A specific situation that sets the background for this session
    """
    system_template: str | None = None
    """
    System prompt for this session
    """
    render_templates: StrictBool = True
    """
    Render system and assistant message content as jinja templates
    """
    token_budget: int | None = None
    """
    Threshold value for the adaptive context functionality
    """
    context_overflow: Literal["truncate", "adaptive"] | None = None
    """
    Action to start on context window overflow
    """
    auto_run_tools: StrictBool = False
    """
    Whether to auto-run the tool and send the tool results to the model when available.
    (default: false for sessions, true for tasks)

    If a tool call is made, the tool's output will be sent back to the model as the model's input.
    If a tool call is not made, the model's output will be returned as is.
    """
    forward_tool_calls: StrictBool = False
    """
    Whether to forward tool calls to the model
    """
    recall_options: RecallOptions | None = None
    metadata: dict[str, Any] | None = None


class PatchSessionRequest(BaseModel):
    """
    Payload for patching a session
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    situation: str = '{%- if agent.name -%}\nYou are {{agent.name}}.{{" "}}\n{%- endif -%}\n\n{%- if agent.about -%}\nAbout you: {{agent.about}}.{{" "}}\n{%- endif -%}\n\n{%- if user -%}\nYou are talking to a user\n  {%- if user.name -%}{{" "}} and their name is {{user.name}}\n    {%- if user.about -%}. About the user: {{user.about}}.{%- else -%}.{%- endif -%}\n  {%- endif -%}\n{%- endif -%}\n\n{{NEWLINE+NEWLINE}}\n\n{%- if agent.instructions -%}\nInstructions:{{NEWLINE}}\n  {%- if agent.instructions is string -%}\n    {{agent.instructions}}{{NEWLINE}}\n  {%- else -%}\n    {%- for instruction in agent.instructions -%}\n      - {{instruction}}{{NEWLINE}}\n    {%- endfor -%}\n  {%- endif -%}\n  {{NEWLINE}}\n{%- endif -%}\n\n{%- if docs -%}\nRelevant documents:{{NEWLINE}}\n  {%- for doc in docs -%}\n    {{doc.title}}{{NEWLINE}}\n    {%- if doc.content is string -%}\n      {{doc.content}}{{NEWLINE}}\n    {%- else -%}\n      {%- for snippet in doc.content -%}\n        {{snippet}}{{NEWLINE}}\n      {%- endfor -%}\n    {%- endif -%}\n    {{"---"}}\n  {%- endfor -%}\n{%- endif -%}'
    """
    A specific situation that sets the background for this session
    """
    system_template: str | None = None
    """
    System prompt for this session
    """
    render_templates: StrictBool = True
    """
    Render system and assistant message content as jinja templates
    """
    token_budget: int | None = None
    """
    Threshold value for the adaptive context functionality
    """
    context_overflow: Literal["truncate", "adaptive"] | None = None
    """
    Action to start on context window overflow
    """
    auto_run_tools: StrictBool = False
    """
    Whether to auto-run the tool and send the tool results to the model when available.
    (default: false for sessions, true for tasks)

    If a tool call is made, the tool's output will be sent back to the model as the model's input.
    If a tool call is not made, the model's output will be returned as is.
    """
    forward_tool_calls: StrictBool = False
    """
    Whether to forward tool calls to the model
    """
    recall_options: RecallOptionsUpdate | None = None
    metadata: dict[str, Any] | None = None


class RecallOptions(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    mode: Literal["hybrid", "vector", "text"] = "vector"
    num_search_messages: int = 4
    max_query_length: int = 1000
    hybrid_alpha: float = 0.7
    confidence: float = 0.6


class RecallOptionsUpdate(RecallOptions):
    pass


class SearchMode(RootModel[Literal["hybrid", "vector", "text"]]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Literal["hybrid", "vector", "text"]


class Session(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    situation: str = '{%- if agent.name -%}\nYou are {{agent.name}}.{{" "}}\n{%- endif -%}\n\n{%- if agent.about -%}\nAbout you: {{agent.about}}.{{" "}}\n{%- endif -%}\n\n{%- if user -%}\nYou are talking to a user\n  {%- if user.name -%}{{" "}} and their name is {{user.name}}\n    {%- if user.about -%}. About the user: {{user.about}}.{%- else -%}.{%- endif -%}\n  {%- endif -%}\n{%- endif -%}\n\n{{NEWLINE+NEWLINE}}\n\n{%- if agent.instructions -%}\nInstructions:{{NEWLINE}}\n  {%- if agent.instructions is string -%}\n    {{agent.instructions}}{{NEWLINE}}\n  {%- else -%}\n    {%- for instruction in agent.instructions -%}\n      - {{instruction}}{{NEWLINE}}\n    {%- endfor -%}\n  {%- endif -%}\n  {{NEWLINE}}\n{%- endif -%}\n\n{%- if docs -%}\nRelevant documents:{{NEWLINE}}\n  {%- for doc in docs -%}\n    {{doc.title}}{{NEWLINE}}\n    {%- if doc.content is string -%}\n      {{doc.content}}{{NEWLINE}}\n    {%- else -%}\n      {%- for snippet in doc.content -%}\n        {{snippet}}{{NEWLINE}}\n      {%- endfor -%}\n    {%- endif -%}\n    {{"---"}}\n  {%- endfor -%}\n{%- endif -%}'
    """
    A specific situation that sets the background for this session
    """
    system_template: str | None = None
    """
    System prompt for this session
    """
    summary: Annotated[str | None, Field(json_schema_extra={"readOnly": True})] = None
    """
    Summary (null at the beginning) - generated automatically after every interaction
    """
    render_templates: StrictBool = True
    """
    Render system and assistant message content as jinja templates
    """
    token_budget: int | None = None
    """
    Threshold value for the adaptive context functionality
    """
    context_overflow: Literal["truncate", "adaptive"] | None = None
    """
    Action to start on context window overflow
    """
    auto_run_tools: StrictBool = False
    """
    Whether to auto-run the tool and send the tool results to the model when available.
    (default: false for sessions, true for tasks)

    If a tool call is made, the tool's output will be sent back to the model as the model's input.
    If a tool call is not made, the model's output will be returned as is.
    """
    forward_tool_calls: StrictBool = False
    """
    Whether to forward tool calls to the model
    """
    recall_options: RecallOptions | None = None
    id: Annotated[UUID, Field(json_schema_extra={"readOnly": True})]
    metadata: dict[str, Any] | None = None
    created_at: Annotated[AwareDatetime, Field(json_schema_extra={"readOnly": True})]
    """
    When this resource was created as UTC date-time
    """
    updated_at: Annotated[AwareDatetime, Field(json_schema_extra={"readOnly": True})]
    """
    When this resource was updated as UTC date-time
    """
    kind: str | None = None
    """
    Discriminator property for Session.
    """


class SingleAgentMultiUserSession(Session):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    agent: UUID
    users: Annotated[list[UUID], Field(min_length=2)]


class SingleAgentNoUserSession(Session):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    agent: UUID


class SingleAgentSingleUserSession(Session):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    agent: UUID
    user: UUID


class UpdateSessionRequest(BaseModel):
    """
    Payload for updating a session
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    situation: str = '{%- if agent.name -%}\nYou are {{agent.name}}.{{" "}}\n{%- endif -%}\n\n{%- if agent.about -%}\nAbout you: {{agent.about}}.{{" "}}\n{%- endif -%}\n\n{%- if user -%}\nYou are talking to a user\n  {%- if user.name -%}{{" "}} and their name is {{user.name}}\n    {%- if user.about -%}. About the user: {{user.about}}.{%- else -%}.{%- endif -%}\n  {%- endif -%}\n{%- endif -%}\n\n{{NEWLINE+NEWLINE}}\n\n{%- if agent.instructions -%}\nInstructions:{{NEWLINE}}\n  {%- if agent.instructions is string -%}\n    {{agent.instructions}}{{NEWLINE}}\n  {%- else -%}\n    {%- for instruction in agent.instructions -%}\n      - {{instruction}}{{NEWLINE}}\n    {%- endfor -%}\n  {%- endif -%}\n  {{NEWLINE}}\n{%- endif -%}\n\n{%- if docs -%}\nRelevant documents:{{NEWLINE}}\n  {%- for doc in docs -%}\n    {{doc.title}}{{NEWLINE}}\n    {%- if doc.content is string -%}\n      {{doc.content}}{{NEWLINE}}\n    {%- else -%}\n      {%- for snippet in doc.content -%}\n        {{snippet}}{{NEWLINE}}\n      {%- endfor -%}\n    {%- endif -%}\n    {{"---"}}\n  {%- endfor -%}\n{%- endif -%}'
    """
    A specific situation that sets the background for this session
    """
    system_template: str | None = None
    """
    System prompt for this session
    """
    render_templates: StrictBool = True
    """
    Render system and assistant message content as jinja templates
    """
    token_budget: int | None = None
    """
    Threshold value for the adaptive context functionality
    """
    context_overflow: Literal["truncate", "adaptive"] | None = None
    """
    Action to start on context window overflow
    """
    auto_run_tools: StrictBool = False
    """
    Whether to auto-run the tool and send the tool results to the model when available.
    (default: false for sessions, true for tasks)

    If a tool call is made, the tool's output will be sent back to the model as the model's input.
    If a tool call is not made, the model's output will be returned as is.
    """
    forward_tool_calls: StrictBool = False
    """
    Whether to forward tool calls to the model
    """
    recall_options: RecallOptions | None = None
    metadata: dict[str, Any] | None = None


class CreateOrUpdateSessionRequest(CreateSessionRequest):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: UUID
    user: UUID | None = None
    """
    User ID of user associated with this session
    """
    users: list[UUID] | None = None
    agent: UUID | None = None
    """
    Agent ID of agent associated with this session
    """
    agents: list[UUID] | None = None
    situation: str = '{%- if agent.name -%}\nYou are {{agent.name}}.{{" "}}\n{%- endif -%}\n\n{%- if agent.about -%}\nAbout you: {{agent.about}}.{{" "}}\n{%- endif -%}\n\n{%- if user -%}\nYou are talking to a user\n  {%- if user.name -%}{{" "}} and their name is {{user.name}}\n    {%- if user.about -%}. About the user: {{user.about}}.{%- else -%}.{%- endif -%}\n  {%- endif -%}\n{%- endif -%}\n\n{{NEWLINE+NEWLINE}}\n\n{%- if agent.instructions -%}\nInstructions:{{NEWLINE}}\n  {%- if agent.instructions is string -%}\n    {{agent.instructions}}{{NEWLINE}}\n  {%- else -%}\n    {%- for instruction in agent.instructions -%}\n      - {{instruction}}{{NEWLINE}}\n    {%- endfor -%}\n  {%- endif -%}\n  {{NEWLINE}}\n{%- endif -%}\n\n{%- if docs -%}\nRelevant documents:{{NEWLINE}}\n  {%- for doc in docs -%}\n    {{doc.title}}{{NEWLINE}}\n    {%- if doc.content is string -%}\n      {{doc.content}}{{NEWLINE}}\n    {%- else -%}\n      {%- for snippet in doc.content -%}\n        {{snippet}}{{NEWLINE}}\n      {%- endfor -%}\n    {%- endif -%}\n    {{"---"}}\n  {%- endfor -%}\n{%- endif -%}'
    """
    A specific situation that sets the background for this session
    """
    system_template: str | None = None
    """
    System prompt for this session
    """
    render_templates: StrictBool = True
    """
    Render system and assistant message content as jinja templates
    """
    token_budget: int | None = None
    """
    Threshold value for the adaptive context functionality
    """
    context_overflow: Literal["truncate", "adaptive"] | None = None
    """
    Action to start on context window overflow
    """
    auto_run_tools: StrictBool = False
    """
    Whether to auto-run the tool and send the tool results to the model when available.
    (default: false for sessions, true for tasks)

    If a tool call is made, the tool's output will be sent back to the model as the model's input.
    If a tool call is not made, the model's output will be returned as is.
    """
    forward_tool_calls: StrictBool = False
    """
    Whether to forward tool calls to the model
    """
    recall_options: RecallOptions | None = None
    metadata: dict[str, Any] | None = None


class MultiAgentMultiUserSession(Session):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    agents: Annotated[list[UUID], Field(min_length=2)]
    users: Annotated[list[UUID], Field(min_length=2)]


class MultiAgentNoUserSession(Session):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    agents: Annotated[list[UUID], Field(min_length=2)]


class MultiAgentSingleUserSession(Session):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    agents: Annotated[list[UUID], Field(min_length=2)]
    user: UUID
