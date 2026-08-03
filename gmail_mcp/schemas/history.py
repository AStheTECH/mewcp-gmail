from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class HistoryRecordData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    messages: list[dict] | None = None
    messagesAdded: list[dict] | None = None
    messagesDeleted: list[dict] | None = None
    labelsAdded: list[dict] | None = None
    labelsRemoved: list[dict] | None = None


class HistoryData(BaseModel):
    model_config = ConfigDict(extra="allow")

    history: list[HistoryRecordData] | None = None
    nextPageToken: str | None = None
    historyId: str | None = None


class HistoryResult(ToolResult):
    data: HistoryData | None = None
