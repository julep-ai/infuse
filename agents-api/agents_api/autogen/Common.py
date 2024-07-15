# generated by datamodel-codegen:
#   filename:  openapi-0.4.0.yaml
#   timestamp: 2024-07-15T21:10:09+00:00

from __future__ import annotations

from typing import Annotated

from pydantic import Field, RootModel


class Limit(RootModel[int]):
    root: Annotated[int, Field(ge=1, lt=1000)]
    """
    Limit the number of results
    """


class LogitBias(RootModel[float]):
    root: Annotated[float, Field(ge=-100.0, le=100.0)]


class Offset(RootModel[int]):
    root: Annotated[int, Field(ge=0)]
    """
    Offset to apply to the results
    """
