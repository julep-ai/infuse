# This file was auto-generated by Fern from our API Definition.

import typing

from .chat_ml_image_content_part import ChatMlImageContentPart
from .chat_ml_image_content_part_image_url import ChatMlImageContentPartImageUrl
from .chat_ml_image_content_part_image_url_detail import (
    ChatMlImageContentPartImageUrlDetail,
)
from .chat_ml_text_content_part import ChatMlTextContentPart

InputChatMlMessageContent = typing.Union[
    str, typing.List[ChatMlTextContentPart], typing.List[ChatMlImageContentPart]
]
