from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ProfileData(BaseModel):
    model_config = ConfigDict(extra="allow")

    emailAddress: str | None = None
    messagesTotal: int | None = None
    threadsTotal: int | None = None
    historyId: str | None = None


class ProfileResult(ToolResult):
    data: ProfileData | None = None
