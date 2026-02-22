from typing import Any, TypedDict


class ToolError(TypedDict):
    error: str


class OAuthTokenData(TypedDict, total=False):
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]


class SendMessageResponse(TypedDict):
    message: str
    id: str
    threadId: str


class IdMessageResponse(TypedDict):
    message: str
    id: str


class ModifyLabelsResponse(TypedDict):
    message: str
    id: str
    labelIds: list[str]


class LabelsListResponse(TypedDict):
    count: int
    labels: list[dict[str, Any]]


class SearchMessagesResponse(TypedDict, total=False):
    count: int
    messages: list[dict[str, Any]]
    resultSizeEstimate: int


class CreateLabelResponse(TypedDict):
    message: str
    label: dict[str, Any]


class DraftsListResponse(TypedDict):
    count: int
    drafts: list[dict[str, Any]]


class CreateDraftResponse(TypedDict):
    message: str
    id: str


ApiObjectResponse = dict[str, Any] | ToolError
SendMessageToolResponse = SendMessageResponse | ToolError
IdMessageToolResponse = IdMessageResponse | ToolError
ModifyLabelsToolResponse = ModifyLabelsResponse | ToolError
LabelsListToolResponse = LabelsListResponse | ToolError
SearchMessagesToolResponse = SearchMessagesResponse | ToolError
CreateLabelToolResponse = CreateLabelResponse | ToolError
DraftsListToolResponse = DraftsListResponse | ToolError
CreateDraftToolResponse = CreateDraftResponse | ToolError
