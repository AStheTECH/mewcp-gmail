from pydantic import BaseModel, ConfigDict, Field

from ._base import ToolResult


class CriteriaData(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True, serialize_by_alias=True)

    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    subject: str | None = None
    query: str | None = None
    negatedQuery: str | None = None
    hasAttachment: bool | None = None
    excludeChats: bool | None = None
    size: int | None = None
    sizeComparison: str | None = None


class ActionData(BaseModel):
    model_config = ConfigDict(extra="allow")

    addLabelIds: list[str] | None = None
    removeLabelIds: list[str] | None = None
    forward: str | None = None


class FilterData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    criteria: CriteriaData | None = None
    action: ActionData | None = None


class FilterResult(ToolResult):
    data: FilterData | None = None


class FiltersData(BaseModel):
    model_config = ConfigDict(extra="allow")

    # The Gmail API's actual list response field is literally named `filter`
    # (singular), not `filters` — this is documented and correct, not a typo.
    filter: list[FilterData] | None = None


class FiltersResult(ToolResult):
    data: FiltersData | None = None


class DeleteFilterData(BaseModel):
    model_config = ConfigDict(extra="allow")


class DeleteFilterResult(ToolResult):
    data: DeleteFilterData | None = None
