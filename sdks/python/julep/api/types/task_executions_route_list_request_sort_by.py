# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class TaskExecutionsRouteListRequestSortBy(str, enum.Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    DELETED_AT = "deleted_at"

    def visit(
        self,
        created_at: typing.Callable[[], T_Result],
        updated_at: typing.Callable[[], T_Result],
        deleted_at: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is TaskExecutionsRouteListRequestSortBy.CREATED_AT:
            return created_at()
        if self is TaskExecutionsRouteListRequestSortBy.UPDATED_AT:
            return updated_at()
        if self is TaskExecutionsRouteListRequestSortBy.DELETED_AT:
            return deleted_at()
