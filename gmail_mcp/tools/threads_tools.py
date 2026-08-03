"""Threads group: delete_thread, get_thread, list_threads, modify_thread, trash_thread, untrash_thread."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.threads import (
    DeleteThreadData,
    DeleteThreadResult,
    ModifyThreadData,
    ModifyThreadResult,
    ThreadData,
    ThreadResult,
    ThreadsData,
    ThreadsResult,
    TrashThreadData,
    TrashThreadResult,
    UntrashThreadData,
    UntrashThreadResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.threads")

_VALID_FORMATS = {"full", "metadata", "minimal"}


def register_threads_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="delete_thread",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Immediately and permanently deletes the specified thread and all its messages; cannot be undone "
            "(prefer trashing instead). "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_thread(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the thread to delete."),
    ) -> DeleteThreadResult:
        tlog = ToolLogger(logger, "delete_thread")

        if not userId:
            return _err(DeleteThreadResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(DeleteThreadResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            gmail_service.users().threads().delete(userId=userId, id=id).execute()
            tlog.success()
            return DeleteThreadResult(success=True, statusCode=200, data=DeleteThreadData())
        except Exception as exc:
            return _handle_request_exc(DeleteThreadResult, tlog, exc)

    @mcp.tool(
        name="get_thread",
        description="Gets the specified thread.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_thread(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the thread to retrieve."),
        format: str | None = Field(
            default=None,
            description=(
                "The format to return the thread's messages in: `full` (full email data, `payload` parsed; "
                "unavailable with the `gmail.metadata` scope), `metadata` (IDs, labels, and headers only), "
                "`minimal` (IDs and labels only)."
            ),
        ),
        metadataHeaders: list[str] | None = Field(
            default=None,
            description="When `format=METADATA`, restricts the returned headers to only those named here.",
        ),
    ) -> ThreadResult:
        tlog = ToolLogger(logger, "get_thread")

        if not userId:
            return _err(ThreadResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(ThreadResult, tlog, "VALIDATION_ERROR", "id is required", 400)
        if format is not None and format not in _VALID_FORMATS:
            return _err(
                ThreadResult, tlog, "VALIDATION_ERROR",
                f"format must be one of {sorted(_VALID_FORMATS)}", 400,
            )

        try:
            gmail_service = service.get_service()
            params: dict = {"userId": userId, "id": id}
            if format is not None:
                params["format"] = format
            if metadataHeaders:
                params["metadataHeaders"] = metadataHeaders
            data = gmail_service.users().threads().get(**params).execute()
            tlog.success()
            return ThreadResult(success=True, statusCode=200, data=ThreadData(**data))
        except Exception as exc:
            return _handle_request_exc(ThreadResult, tlog, exc)

    @mcp.tool(
        name="list_threads",
        description="Lists the threads in the user's mailbox.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_threads(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        maxResults: int | None = Field(
            default=None,
            description="Maximum number of threads to return. Defaults to 100, maximum allowed is 500.",
        ),
        pageToken: str | None = Field(
            default=None, description="Page token to retrieve a specific page of results."
        ),
        q: str | None = Field(
            default=None,
            description=(
                "Only return threads matching this query, in Gmail search-box syntax. "
                "Cannot be used with the `gmail.metadata` scope."
            ),
        ),
        labelIds: list[str] | None = Field(
            default=None,
            description="Only return threads with labels matching all of the given label IDs.",
        ),
        includeSpamTrash: bool | None = Field(
            default=None, description="Include threads from `SPAM` and `TRASH` in the results."
        ),
    ) -> ThreadsResult:
        tlog = ToolLogger(logger, "list_threads")

        if not userId:
            return _err(ThreadsResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if maxResults is not None and (maxResults < 1 or maxResults > 500):
            return _err(
                ThreadsResult, tlog, "VALIDATION_ERROR", "maxResults must be between 1 and 500", 400
            )

        try:
            gmail_service = service.get_service()
            params: dict = {"userId": userId}
            if maxResults is not None:
                params["maxResults"] = maxResults
            if pageToken is not None:
                params["pageToken"] = pageToken
            if q is not None:
                params["q"] = q
            if labelIds:
                params["labelIds"] = labelIds
            if includeSpamTrash is not None:
                params["includeSpamTrash"] = includeSpamTrash
            data = gmail_service.users().threads().list(**params).execute()
            tlog.success()
            return ThreadsResult(success=True, statusCode=200, data=ThreadsData(**data))
        except Exception as exc:
            return _handle_request_exc(ThreadsResult, tlog, exc)

    @mcp.tool(
        name="modify_thread",
        description=(
            "NOTE: this changes label state on the thread (all its messages) immediately — the original "
            "label state is not stored after the call, so the response includes both the `before` and "
            "`after` thread state for a full record of what changed. "
            "Adds or removes labels applied to the thread; this affects all messages in the thread."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def modify_thread(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the thread to modify."),
        addLabelIds: list[str] | None = Field(
            default=None,
            description="Label IDs to add to this thread (all its messages). Up to 100 per update.",
        ),
        removeLabelIds: list[str] | None = Field(
            default=None,
            description="Label IDs to remove from this thread (all its messages). Up to 100 per update.",
        ),
    ) -> ModifyThreadResult:
        tlog = ToolLogger(logger, "modify_thread")

        if not userId:
            return _err(ModifyThreadResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(ModifyThreadResult, tlog, "VALIDATION_ERROR", "id is required", 400)
        if addLabelIds and len(addLabelIds) > 100:
            return _err(
                ModifyThreadResult, tlog, "VALIDATION_ERROR",
                "addLabelIds accepts up to 100 label IDs per update", 400,
            )
        if removeLabelIds and len(removeLabelIds) > 100:
            return _err(
                ModifyThreadResult, tlog, "VALIDATION_ERROR",
                "removeLabelIds accepts up to 100 label IDs per update", 400,
            )

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().threads().get(userId=userId, id=id).execute()

            body: dict = {}
            if addLabelIds:
                body["addLabelIds"] = addLabelIds
            if removeLabelIds:
                body["removeLabelIds"] = removeLabelIds

            after = gmail_service.users().threads().modify(userId=userId, id=id, body=body).execute()
            tlog.success()
            return ModifyThreadResult(
                success=True,
                statusCode=200,
                data=ModifyThreadData(before=ThreadData(**before), after=ThreadData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(ModifyThreadResult, tlog, exc)

    @mcp.tool(
        name="trash_thread",
        description=(
            "NOTE: this moves the thread (all its messages) to trash immediately — the original, "
            "non-trashed state is not stored after the call, so the response includes both the `before` "
            "and `after` thread state for a full record of what changed. "
            "Moves the specified thread, and all its messages, to the trash."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def trash_thread(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the thread to trash."),
    ) -> TrashThreadResult:
        tlog = ToolLogger(logger, "trash_thread")

        if not userId:
            return _err(TrashThreadResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(TrashThreadResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().threads().get(userId=userId, id=id).execute()
            after = gmail_service.users().threads().trash(userId=userId, id=id).execute()
            tlog.success()
            return TrashThreadResult(
                success=True,
                statusCode=200,
                data=TrashThreadData(before=ThreadData(**before), after=ThreadData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(TrashThreadResult, tlog, exc)

    @mcp.tool(
        name="untrash_thread",
        description=(
            "NOTE: this removes the thread (all its messages) from trash immediately — the prior, "
            "trashed state is not stored after the call, so the response includes both the `before` "
            "and `after` thread state for a full record of what changed. "
            "Removes the specified thread, and all its messages, from the trash."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def untrash_thread(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the thread to remove from trash."),
    ) -> UntrashThreadResult:
        tlog = ToolLogger(logger, "untrash_thread")

        if not userId:
            return _err(UntrashThreadResult, tlog, "VALIDATION_ERROR", "userId is required", 400)
        if not id:
            return _err(UntrashThreadResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().threads().get(userId=userId, id=id).execute()
            after = gmail_service.users().threads().untrash(userId=userId, id=id).execute()
            tlog.success()
            return UntrashThreadResult(
                success=True,
                statusCode=200,
                data=UntrashThreadData(before=ThreadData(**before), after=ThreadData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(UntrashThreadResult, tlog, exc)
