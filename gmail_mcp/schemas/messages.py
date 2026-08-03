from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


# --- batch_delete_messages ---------------------------------------------------

class BatchDeleteMessagesData(BaseModel):
    model_config = ConfigDict(extra="allow")


class BatchDeleteMessagesResult(ToolResult):
    data: BatchDeleteMessagesData | None = None


# --- batch_modify_messages ---------------------------------------------------

class BatchModifyMessagesData(BaseModel):
    model_config = ConfigDict(extra="allow")


class BatchModifyMessagesResult(ToolResult):
    data: BatchModifyMessagesData | None = None


# --- delete_message -----------------------------------------------------------

class DeleteMessageData(BaseModel):
    model_config = ConfigDict(extra="allow")


class DeleteMessageResult(ToolResult):
    data: DeleteMessageData | None = None


# --- get_message_attachment ---------------------------------------------------

class GetMessageAttachmentData(BaseModel):
    model_config = ConfigDict(extra="allow")

    attachmentId: str | None = None
    size: int | None = None
    data: str | None = None


class GetMessageAttachmentResult(ToolResult):
    data: GetMessageAttachmentData | None = None


# --- get_message ---------------------------------------------------------------

class GetMessageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    threadId: str | None = None
    labelIds: list[str] | None = None
    snippet: str | None = None
    historyId: str | None = None
    internalDate: str | None = None
    payload: dict | None = None
    sizeEstimate: int | None = None
    raw: str | None = None
    classificationLabelValues: list[dict] | None = None


class GetMessageResult(ToolResult):
    data: GetMessageData | None = None


# --- list_messages ---------------------------------------------------------------

class ListMessagesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    messages: list[GetMessageData] | None = None
    nextPageToken: str | None = None
    resultSizeEstimate: int | None = None


class ListMessagesResult(ToolResult):
    data: ListMessagesData | None = None


# --- modify_message ---------------------------------------------------------------

class ModifyMessageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GetMessageData
    after: GetMessageData


class ModifyMessageResult(ToolResult):
    data: ModifyMessageData | None = None


# --- send_message ---------------------------------------------------------------

class SendMessageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | None = None
    threadId: str | None = None
    labelIds: list[str] | None = None
    snippet: str | None = None
    historyId: str | None = None
    internalDate: str | None = None
    payload: dict | None = None
    sizeEstimate: int | None = None
    raw: str | None = None
    classificationLabelValues: list[dict] | None = None


class SendMessageResult(ToolResult):
    data: SendMessageData | None = None


# --- trash_message ---------------------------------------------------------------

class TrashMessageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GetMessageData
    after: GetMessageData


class TrashMessageResult(ToolResult):
    data: TrashMessageData | None = None


# --- untrash_message ---------------------------------------------------------------

class UntrashMessageData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: GetMessageData
    after: GetMessageData


class UntrashMessageResult(ToolResult):
    data: UntrashMessageData | None = None
