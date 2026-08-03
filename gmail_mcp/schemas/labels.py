from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class LabelColor(BaseModel):
    model_config = ConfigDict(extra="allow")

    textColor: str | None = None
    backgroundColor: str | None = None


class LabelData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    name: str | None = None
    messageListVisibility: str | None = None
    labelListVisibility: str | None = None
    type: str | None = None
    messagesTotal: int | None = None
    messagesUnread: int | None = None
    threadsTotal: int | None = None
    threadsUnread: int | None = None
    color: LabelColor | None = None


class LabelResult(ToolResult):
    data: LabelData | None = None


class LabelsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    labels: list[LabelData] | None = None


class LabelsResult(ToolResult):
    data: LabelsData | None = None


class DeleteLabelData(BaseModel):
    model_config = ConfigDict(extra="allow")


class DeleteLabelResult(ToolResult):
    data: DeleteLabelData | None = None


class UpdateLabelData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: LabelData
    after: LabelData


class UpdateLabelResult(ToolResult):
    data: UpdateLabelData | None = None
