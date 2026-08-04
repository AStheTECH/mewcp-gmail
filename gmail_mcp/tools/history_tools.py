"""History group: list_history."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.history import HistoryData, HistoryResult
from ._helpers import USER_ID_DESC, _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.history")


def register_history_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="list_history",
        description=(
            "Lists the history of all changes to the mailbox in chronological order "
            "(increasing historyId), for syncing local client state with the server."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_history(
        startHistoryId: str = Field(
            description=(
                "Return history records after this `historyId` (obtained from a "
                "message's/thread's `historyId`, or a previous `list` response). History IDs "
                "increase chronologically but are not contiguous. An invalid or stale "
                "`startHistoryId` typically returns `HTTP 404` — perform a full sync if that "
                "happens. A `historyId` is usually valid for at least a week (sometimes only a "
                "few hours). No `nextPageToken` in the response means there are no updates; "
                "store the returned `historyId` for the next request."
            )
        ),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
        maxResults: int | None = Field(
            default=None,
            description="Maximum number of history records to return. Defaults to 100, maximum allowed is 500.",
        ),
        pageToken: str | None = Field(
            default=None, description="Page token to retrieve a specific page of results."
        ),
        labelId: str | None = Field(
            default=None, description="Only return messages with a label matching this ID."
        ),
        historyTypes: list[str] | None = Field(
            default=None,
            description=(
                "Restrict to these history record types. Enum values (`HistoryType`): "
                "`messageAdded`, `messageDeleted`, `labelAdded`, `labelRemoved`."
            ),
        ),
    ) -> HistoryResult:
        tlog = ToolLogger(logger, "list_history")

        if not startHistoryId:
            return _err(HistoryResult, tlog, "VALIDATION_ERROR", "startHistoryId is required", 400)
        if maxResults is not None and (maxResults < 1 or maxResults > 500):
            return _err(HistoryResult, tlog, "VALIDATION_ERROR", "maxResults must be 1-500", 400)

        try:
            gmail_service = service.get_service()
            params = {"userId": userId, "startHistoryId": startHistoryId}
            if maxResults is not None:
                params["maxResults"] = maxResults
            if pageToken is not None:
                params["pageToken"] = pageToken
            if labelId is not None:
                params["labelId"] = labelId
            if historyTypes is not None:
                params["historyTypes"] = historyTypes

            data = gmail_service.users().history().list(**params).execute()
            tlog.success()
            return HistoryResult(success=True, statusCode=200, data=HistoryData(**data))
        except Exception as exc:
            return _handle_request_exc(HistoryResult, tlog, exc)
