from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ThreadData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    snippet: str | None = None
    historyId: str | None = None
    messages: list[dict] | None = None


class ThreadResult(ToolResult):
    data: ThreadData | None = None


class ThreadsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    threads: list[ThreadData] | None = None
    nextPageToken: str | None = None
    resultSizeEstimate: int | None = None


class ThreadsResult(ToolResult):
    data: ThreadsData | None = None


class DeleteThreadData(BaseModel):
    model_config = ConfigDict(extra="allow")


class DeleteThreadResult(ToolResult):
    data: DeleteThreadData | None = None


class ModifyThreadData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: ThreadData
    after: ThreadData


class ModifyThreadResult(ToolResult):
    data: ModifyThreadData | None = None


class TrashThreadData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: ThreadData
    after: ThreadData


class TrashThreadResult(ToolResult):
    data: TrashThreadData | None = None


class UntrashThreadData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: ThreadData
    after: ThreadData


class UntrashThreadResult(ToolResult):
    data: UntrashThreadData | None = None
