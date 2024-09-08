from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    List,
    Optional,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.entries_chat_ml_role import EntriesChatMLRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_input_messages_item_content_type_2_item_type_0 import (
        ChatInputMessagesItemContentType2ItemType0,
    )
    from ..models.chat_input_messages_item_content_type_2_item_type_1 import (
        ChatInputMessagesItemContentType2ItemType1,
    )


T = TypeVar("T", bound="ChatInputMessagesItem")


@_attrs_define
class ChatInputMessagesItem:
    """
    Attributes:
        role (EntriesChatMLRole): ChatML role (system|assistant|user|function_call|function|function_response|auto)
        content (Union[List[Union['ChatInputMessagesItemContentType2ItemType0',
            'ChatInputMessagesItemContentType2ItemType1']], List[str], str]): The content parts of the message
        name (Union[Unset, str]): Name
        continue_ (Union[Unset, bool]): Whether to continue this message or return a new one
    """

    role: EntriesChatMLRole
    content: Union[
        List[
            Union[
                "ChatInputMessagesItemContentType2ItemType0",
                "ChatInputMessagesItemContentType2ItemType1",
            ]
        ],
        List[str],
        str,
    ]
    name: Union[Unset, str] = UNSET
    continue_: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.chat_input_messages_item_content_type_2_item_type_0 import (
            ChatInputMessagesItemContentType2ItemType0,
        )
        from ..models.chat_input_messages_item_content_type_2_item_type_1 import (
            ChatInputMessagesItemContentType2ItemType1,
        )

        role = self.role.value

        content: Union[List[Dict[str, Any]], List[str], str]
        if isinstance(self.content, list):
            content = self.content

        elif isinstance(self.content, list):
            content = []
            for content_type_2_item_data in self.content:
                content_type_2_item: Dict[str, Any]
                if isinstance(
                    content_type_2_item_data, ChatInputMessagesItemContentType2ItemType0
                ):
                    content_type_2_item = content_type_2_item_data.to_dict()
                else:
                    content_type_2_item = content_type_2_item_data.to_dict()

                content.append(content_type_2_item)

        else:
            content = self.content

        name = self.name

        continue_ = self.continue_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "content": content,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if continue_ is not UNSET:
            field_dict["continue"] = continue_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_input_messages_item_content_type_2_item_type_0 import (
            ChatInputMessagesItemContentType2ItemType0,
        )
        from ..models.chat_input_messages_item_content_type_2_item_type_1 import (
            ChatInputMessagesItemContentType2ItemType1,
        )

        d = src_dict.copy()
        role = EntriesChatMLRole(d.pop("role"))

        def _parse_content(
            data: object,
        ) -> Union[
            List[
                Union[
                    "ChatInputMessagesItemContentType2ItemType0",
                    "ChatInputMessagesItemContentType2ItemType1",
                ]
            ],
            List[str],
            str,
        ]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_1 = cast(List[str], data)

                return content_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                content_type_2 = []
                _content_type_2 = data
                for content_type_2_item_data in _content_type_2:

                    def _parse_content_type_2_item(
                        data: object,
                    ) -> Union[
                        "ChatInputMessagesItemContentType2ItemType0",
                        "ChatInputMessagesItemContentType2ItemType1",
                    ]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            content_type_2_item_type_0 = (
                                ChatInputMessagesItemContentType2ItemType0.from_dict(
                                    data
                                )
                            )

                            return content_type_2_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        content_type_2_item_type_1 = (
                            ChatInputMessagesItemContentType2ItemType1.from_dict(data)
                        )

                        return content_type_2_item_type_1

                    content_type_2_item = _parse_content_type_2_item(
                        content_type_2_item_data
                    )

                    content_type_2.append(content_type_2_item)

                return content_type_2
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    List[
                        Union[
                            "ChatInputMessagesItemContentType2ItemType0",
                            "ChatInputMessagesItemContentType2ItemType1",
                        ]
                    ],
                    List[str],
                    str,
                ],
                data,
            )

        content = _parse_content(d.pop("content"))

        name = d.pop("name", UNSET)

        continue_ = d.pop("continue", UNSET)

        chat_input_messages_item = cls(
            role=role,
            content=content,
            name=name,
            continue_=continue_,
        )

        chat_input_messages_item.additional_properties = d
        return chat_input_messages_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
