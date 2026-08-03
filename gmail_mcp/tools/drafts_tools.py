"""Drafts group: create_draft, delete_draft, get_draft, list_drafts, send_draft, update_draft."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.drafts import (
    DeleteDraftData,
    DeleteDraftResult,
    DraftData,
    DraftResult,
    DraftsData,
    DraftsResult,
    SendDraftData,
    SendDraftResult,
    UpdateDraftData,
    UpdateDraftResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.drafts")


def register_drafts_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_draft",
        description="Creates a draft with the DRAFT label.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_draft(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        message: dict | None = Field(
            default=None,
            description=(
                "The message content of the draft (object (Message)); send this to give "
                "the draft its content."
            ),
        ),
    ) -> DraftResult:
        tlog = ToolLogger(logger, "create_draft")

        if not userId:
            return _err(DraftResult, tlog, "VALIDATION_ERROR", "userId is required", 400)

        try:
            gmail_service = service.get_service()
            body = {"message": message} if message else {}
            data = gmail_service.users().drafts().create(userId=userId, body=body).execute()
            tlog.success()
            return DraftResult(success=True, statusCode=200, data=DraftData(**data))
        except Exception as exc:
            return _handle_request_exc(DraftResult, tlog, exc)

    @mcp.tool(
        name="delete_draft",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Immediately and permanently deletes the specified draft (does not simply trash it). "
            "This action is irreversible — the draft and its message content cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_draft(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the draft to delete."),
    ) -> DeleteDraftResult:
        tlog = ToolLogger(logger, "delete_draft")

        if not userId:
            return _err(DeleteDraftResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(DeleteDraftResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            gmail_service.users().drafts().delete(userId=userId, id=id).execute()
            tlog.success()
            return DeleteDraftResult(success=True, statusCode=200, data=DeleteDraftData())
        except Exception as exc:
            return _handle_request_exc(DeleteDraftResult, tlog, exc)

    @mcp.tool(
        name="get_draft",
        description="Gets the specified draft.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_draft(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the draft to retrieve."),
        format: str | None = Field(
            default=None,
            description=(
                "The format to return the draft's message in: `minimal` (ID and labels only), "
                "`full` (full data, parsed into `payload`), `raw` (full data as a base64url "
                "string in `raw`; `payload` unused), `metadata` (ID, labels, and headers only). "
                "`full`/`raw` are unavailable when using the `gmail.metadata` scope."
            ),
        ),
    ) -> DraftResult:
        tlog = ToolLogger(logger, "get_draft")

        if not userId:
            return _err(DraftResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(DraftResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().drafts().get(userId=userId, id=id, format=format).execute()
            tlog.success()
            return DraftResult(success=True, statusCode=200, data=DraftData(**data))
        except Exception as exc:
            return _handle_request_exc(DraftResult, tlog, exc)

    @mcp.tool(
        name="list_drafts",
        description="Lists the drafts in the user's mailbox.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_drafts(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        maxResults: int | None = Field(
            default=None,
            description="Maximum number of drafts to return. Defaults to 100, maximum allowed is 500.",
        ),
        pageToken: str | None = Field(
            default=None, description="Page token to retrieve a specific page of results."
        ),
        q: str | None = Field(
            default=None,
            description=(
                "Only return drafts matching this query, in Gmail search-box syntax, e.g. "
                '`"from:someuser@example.com rfc822msgid:<somemsgid@example.com> is:unread"`.'
            ),
        ),
        includeSpamTrash: bool | None = Field(
            default=None, description="Include drafts from `SPAM` and `TRASH` in the results."
        ),
    ) -> DraftsResult:
        tlog = ToolLogger(logger, "list_drafts")

        if not userId:
            return _err(DraftsResult, tlog, "VALIDATION_ERROR", "userId is required", 400)

        try:
            gmail_service = service.get_service()
            data = (
                gmail_service.users()
                .drafts()
                .list(
                    userId=userId,
                    maxResults=maxResults,
                    pageToken=pageToken,
                    q=q,
                    includeSpamTrash=includeSpamTrash,
                )
                .execute()
            )
            tlog.success()
            return DraftsResult(success=True, statusCode=200, data=DraftsData(**data))
        except Exception as exc:
            return _handle_request_exc(DraftsResult, tlog, exc)

    @mcp.tool(
        name="send_draft",
        description="Sends the specified, existing draft to the recipients in the To, Cc, and Bcc headers.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def send_draft(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the existing draft to send."),
        message: dict | None = Field(
            default=None,
            description="Optional — the draft's message content (object (Message)).",
        ),
    ) -> SendDraftResult:
        tlog = ToolLogger(logger, "send_draft")

        if not userId:
            return _err(SendDraftResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(SendDraftResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            body = {"id": id, **({"message": message} if message else {})}
            data = gmail_service.users().drafts().send(userId=userId, body=body).execute()
            tlog.success()
            return SendDraftResult(success=True, statusCode=200, data=SendDraftData(**data))
        except Exception as exc:
            return _handle_request_exc(SendDraftResult, tlog, exc)

    @mcp.tool(
        name="update_draft",
        description=(
            "NOTE: this tool first fetches the draft's current state, then replaces it — the "
            "response includes both the `before` and `after` state so you have a full record of "
            "what changed. Replaces a draft's content entirely; since this is a full overwrite, "
            "any fields not included in `message` are lost."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_draft(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the draft to update."),
        message: dict | None = Field(
            default=None,
            description=(
                "The replacement message content of the draft (object (Message)); since this is "
                "a full replace, send this to give the draft its new content."
            ),
        ),
    ) -> UpdateDraftResult:
        tlog = ToolLogger(logger, "update_draft")

        if not userId:
            return _err(UpdateDraftResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(UpdateDraftResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            before_data = gmail_service.users().drafts().get(userId=userId, id=id).execute()
            body = {"message": message} if message else {}
            after_data = gmail_service.users().drafts().update(userId=userId, id=id, body=body).execute()
            tlog.success()
            return UpdateDraftResult(
                success=True,
                statusCode=200,
                data=UpdateDraftData(before=DraftData(**before_data), after=DraftData(**after_data)),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateDraftResult, tlog, exc)
