from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class DraftData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    message: dict | None = None


class DraftResult(ToolResult):
    data: DraftData | None = None


class DraftsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    drafts: list[DraftData] | None = None
    nextPageToken: str | None = None
    resultSizeEstimate: int | None = None


class DraftsResult(ToolResult):
    data: DraftsData | None = None


class DeleteDraftData(BaseModel):
    model_config = ConfigDict(extra="allow")


class DeleteDraftResult(ToolResult):
    data: DeleteDraftData | None = None


class SendDraftData(BaseModel):
    model_config = ConfigDict(extra="allow")


class SendDraftResult(ToolResult):
    data: SendDraftData | None = None
