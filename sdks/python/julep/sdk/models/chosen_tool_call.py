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

from ..models.tool_type import ToolType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.function_call_option import FunctionCallOption


T = TypeVar("T", bound="ChosenToolCall")


@_attrs_define
class ChosenToolCall:
    """The response tool value generated by the model

    Attributes:
        type (ToolType):
        id (str):
        function (Union[Unset, FunctionCallOption]):
        integration (Union[Unset, Any]):
        system (Union[Unset, Any]):
        api_call (Union[Unset, Any]):
    """

    type: ToolType
    id: str
    function: Union[Unset, "FunctionCallOption"] = UNSET
    integration: Union[Unset, Any] = UNSET
    system: Union[Unset, Any] = UNSET
    api_call: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.function_call_option import FunctionCallOption

        type = self.type.value

        id = self.id

        function: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.function, Unset):
            function = self.function.to_dict()

        integration = self.integration

        system = self.system

        api_call = self.api_call

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "id": id,
            }
        )
        if function is not UNSET:
            field_dict["function"] = function
        if integration is not UNSET:
            field_dict["integration"] = integration
        if system is not UNSET:
            field_dict["system"] = system
        if api_call is not UNSET:
            field_dict["api_call"] = api_call

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.function_call_option import FunctionCallOption

        d = src_dict.copy()
        type = ToolType(d.pop("type"))

        id = d.pop("id")

        _function = d.pop("function", UNSET)
        function: Union[Unset, FunctionCallOption]
        if isinstance(_function, Unset):
            function = UNSET
        else:
            function = FunctionCallOption.from_dict(_function)

        integration = d.pop("integration", UNSET)

        system = d.pop("system", UNSET)

        api_call = d.pop("api_call", UNSET)

        chosen_tool_call = cls(
            type=type,
            id=id,
            function=function,
            integration=integration,
            system=system,
            api_call=api_call,
        )

        chosen_tool_call.additional_properties = d
        return chosen_tool_call

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
