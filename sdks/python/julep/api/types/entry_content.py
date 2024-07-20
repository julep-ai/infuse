# This file was auto-generated by Fern from our API Definition.

import typing

from .entry_content_item import EntryContentItem
from .tools_chosen_tool_call import ToolsChosenToolCall
from .tools_tool import ToolsTool
from .tools_tool_response import ToolsToolResponse

EntryContent = typing.Union[
    typing.List[EntryContentItem],
    ToolsTool,
    ToolsChosenToolCall,
    str,
    ToolsToolResponse,
    typing.List[EntryContentItem],
]
