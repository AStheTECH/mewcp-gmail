"""Messages group: batch_delete_messages, batch_modify_messages, delete_message,
get_message_attachment, get_message, list_messages, modify_message, send_message,
trash_message, untrash_message."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.messages import (
    BatchDeleteMessagesData,
    BatchDeleteMessagesResult,
    BatchModifyMessagesData,
    BatchModifyMessagesResult,
    DeleteMessageData,
    DeleteMessageResult,
    GetMessageAttachmentData,
    GetMessageAttachmentResult,
    GetMessageData,
    GetMessageResult,
    ListMessagesData,
    ListMessagesResult,
    ModifyMessageData,
    ModifyMessageResult,
    SendMessageData,
    SendMessageResult,
    TrashMessageData,
    TrashMessageResult,
    UntrashMessageData,
    UntrashMessageResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.messages")


def register_messages_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="batch_delete_messages",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Permanently deletes many messages by message ID in one call; provides no guarantee "
            "that a message was not already deleted or ever existed. "
            "This action is irreversible — deleted messages cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly how many messages (and their IDs, if the list "
            "is short) will be deleted and that it is permanent, and wait for their explicit "
            "written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def batch_delete_messages(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        ids: list[str] = Field(
            description=(
                "The IDs of the messages to delete. No guarantee is given that a message wasn't "
                "already deleted or ever existed — this is a fire-and-forget bulk permanent "
                "delete, irreversible."
            )
        ),
    ) -> BatchDeleteMessagesResult:
        tlog = ToolLogger(logger, "batch_delete_messages")

        if not ids:
            return _err(BatchDeleteMessagesResult, tlog, "VALIDATION_ERROR", "ids must be a non-empty list", 400)

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().messages().batchDelete(userId=userId, body={"ids": ids}).execute()
            tlog.success()
            return BatchDeleteMessagesResult(success=True, statusCode=200, data=BatchDeleteMessagesData(**(data or {})))
        except Exception as exc:
            return _handle_request_exc(BatchDeleteMessagesResult, tlog, exc)

    @mcp.tool(
        name="batch_modify_messages",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Adds or removes labels on the specified messages in a single bulk call. "
            "This action affects many messages at once and can change their visibility "
            "(e.g. removing INBOX or adding TRASH/SPAM) or accessibility. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly which messages and labels will be affected, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def batch_modify_messages(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        ids: list[str] = Field(
            description="The IDs of the messages to modify. Limit of 1000 IDs per request."
        ),
        addLabelIds: list[str] | None = Field(
            default=None, description="Label IDs to add to all specified messages."
        ),
        removeLabelIds: list[str] | None = Field(
            default=None, description="Label IDs to remove from all specified messages."
        ),
        addClassificationLabels: list[dict] | None = Field(
            default=None,
            description=(
                "Classification Label values to add (Google Workspace only). "
                "Limit of 20 per message."
            ),
        ),
        removeClassificationLabelIds: list[str] | None = Field(
            default=None, description="Classification Label values to remove from the messages."
        ),
    ) -> BatchModifyMessagesResult:
        tlog = ToolLogger(logger, "batch_modify_messages")

        if not ids:
            return _err(BatchModifyMessagesResult, tlog, "VALIDATION_ERROR", "ids must be a non-empty list", 400)

        body: dict = {"ids": ids}
        if addLabelIds is not None:
            body["addLabelIds"] = addLabelIds
        if removeLabelIds is not None:
            body["removeLabelIds"] = removeLabelIds
        if addClassificationLabels is not None:
            body["addClassificationLabels"] = addClassificationLabels
        if removeClassificationLabelIds is not None:
            body["removeClassificationLabelIds"] = removeClassificationLabelIds

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().messages().batchModify(userId=userId, body=body).execute()
            tlog.success()
            return BatchModifyMessagesResult(success=True, statusCode=200, data=BatchModifyMessagesData(**(data or {})))
        except Exception as exc:
            return _handle_request_exc(BatchModifyMessagesResult, tlog, exc)

    @mcp.tool(
        name="delete_message",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Immediately and permanently deletes the specified message; this cannot be undone "
            "(prefer trashing instead). "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_message(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the message to delete."),
    ) -> DeleteMessageResult:
        tlog = ToolLogger(logger, "delete_message")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().messages().delete(userId=userId, id=id).execute()
            tlog.success()
            return DeleteMessageResult(success=True, statusCode=200, data=DeleteMessageData(**(data or {})))
        except Exception as exc:
            return _handle_request_exc(DeleteMessageResult, tlog, exc)

    @mcp.tool(
        name="get_message_attachment",
        description="Gets the specified message attachment.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_message_attachment(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        messageId: str = Field(description="The ID of the message containing the attachment."),
        id: str = Field(
            description="The ID of the attachment (from the message's `payload` — see get_message)."
        ),
    ) -> GetMessageAttachmentResult:
        tlog = ToolLogger(logger, "get_message_attachment")

        try:
            gmail_service = service.get_service()
            data = (
                gmail_service.users()
                .messages()
                .attachments()
                .get(userId=userId, messageId=messageId, id=id)
                .execute()
            )
            tlog.success()
            return GetMessageAttachmentResult(success=True, statusCode=200, data=GetMessageAttachmentData(**data))
        except Exception as exc:
            return _handle_request_exc(GetMessageAttachmentResult, tlog, exc)

    @mcp.tool(
        name="get_message",
        description="Gets the specified message.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_message(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(
            description="The ID of the message to retrieve. Usually obtained from list_messages."
        ),
        format: str | None = Field(
            default=None,
            description=(
                "`minimal` (ID and labels only), `full` (default; full data parsed into "
                "`payload`, `raw` unused), `raw` (full data as base64url in `raw`, `payload` "
                "unused), `metadata` (ID, labels, and headers only). `full`/`raw` are "
                "unavailable when using the `gmail.metadata` scope."
            ),
        ),
        metadataHeaders: list[str] | None = Field(
            default=None,
            description=(
                "When `format=METADATA`, restricts the returned headers to only those named here."
            ),
        ),
    ) -> GetMessageResult:
        tlog = ToolLogger(logger, "get_message")

        kwargs: dict = {"userId": userId, "id": id}
        if format is not None:
            kwargs["format"] = format
        if metadataHeaders is not None:
            kwargs["metadataHeaders"] = metadataHeaders

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().messages().get(**kwargs).execute()
            tlog.success()
            return GetMessageResult(success=True, statusCode=200, data=GetMessageData(**data))
        except Exception as exc:
            return _handle_request_exc(GetMessageResult, tlog, exc)

    @mcp.tool(
        name="list_messages",
        description="Lists the messages in the user's mailbox.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_messages(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        maxResults: int | None = Field(
            default=None,
            description="Maximum number of messages to return. Defaults to 100, maximum allowed is 500.",
        ),
        pageToken: str | None = Field(
            default=None, description="Page token to retrieve a specific page of results."
        ),
        q: str | None = Field(
            default=None,
            description=(
                "Only return messages matching this query, in Gmail search-box syntax. "
                "Cannot be used with the `gmail.metadata` scope."
            ),
        ),
        labelIds: list[str] | None = Field(
            default=None,
            description="Only return messages with labels matching all of the given label IDs.",
        ),
        includeSpamTrash: bool | None = Field(
            default=None, description="Include messages from `SPAM` and `TRASH` in the results."
        ),
    ) -> ListMessagesResult:
        tlog = ToolLogger(logger, "list_messages")

        if maxResults is not None and not (1 <= maxResults <= 500):
            return _err(ListMessagesResult, tlog, "VALIDATION_ERROR", "maxResults must be between 1 and 500", 400)

        kwargs: dict = {"userId": userId}
        if maxResults is not None:
            kwargs["maxResults"] = maxResults
        if pageToken is not None:
            kwargs["pageToken"] = pageToken
        if q is not None:
            kwargs["q"] = q
        if labelIds is not None:
            kwargs["labelIds"] = labelIds
        if includeSpamTrash is not None:
            kwargs["includeSpamTrash"] = includeSpamTrash

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().messages().list(**kwargs).execute()
            tlog.success()
            return ListMessagesResult(success=True, statusCode=200, data=ListMessagesData(**data))
        except Exception as exc:
            return _handle_request_exc(ListMessagesResult, tlog, exc)

    @mcp.tool(
        name="modify_message",
        description=(
            "Updates the specified message's labels. Only the label additions/removals you "
            "provide are applied — everything else about the message keeps its current value. "
            "NOTE: this overwrites the current label state — the original state is not stored "
            "after the call. The response includes both the before and after state of the "
            "message so you have a full record of what changed. "
            "Adds or removes labels on the specified message."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def modify_message(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the message to modify."),
        addLabelIds: list[str] | None = Field(
            default=None, description="Label IDs to add to this message. Up to 100 per update."
        ),
        removeLabelIds: list[str] | None = Field(
            default=None, description="Label IDs to remove from this message. Up to 100 per update."
        ),
        addClassificationLabels: list[dict] | None = Field(
            default=None,
            description="Classification Label values to add (Google Workspace only).",
        ),
        removeClassificationLabelIds: list[str] | None = Field(
            default=None, description="Classification Label values to remove from the message."
        ),
    ) -> ModifyMessageResult:
        tlog = ToolLogger(logger, "modify_message")

        body: dict = {}
        if addLabelIds is not None:
            body["addLabelIds"] = addLabelIds
        if removeLabelIds is not None:
            body["removeLabelIds"] = removeLabelIds
        if addClassificationLabels is not None:
            body["addClassificationLabels"] = addClassificationLabels
        if removeClassificationLabelIds is not None:
            body["removeClassificationLabelIds"] = removeClassificationLabelIds

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().messages().get(userId=userId, id=id).execute()
            after = gmail_service.users().messages().modify(userId=userId, id=id, body=body).execute()
            tlog.success()
            return ModifyMessageResult(
                success=True,
                statusCode=200,
                data=ModifyMessageData(before=GetMessageData(**before), after=GetMessageData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(ModifyMessageResult, tlog, exc)

    @mcp.tool(
        name="send_message",
        description="Sends the specified message to the recipients in the To, Cc, and Bcc headers.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def send_message(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        raw: str | None = Field(
            default=None,
            description=(
                "The entire RFC 2822 message (headers + body, with `To`/`Cc`/`Bcc`/`Subject` "
                "etc. as headers), base64url-encoded. Not explicitly marked required by the "
                "provider docs but practically necessary to send anything."
            ),
        ),
    ) -> SendMessageResult:
        tlog = ToolLogger(logger, "send_message")

        if not raw:
            return _err(SendMessageResult, tlog, "VALIDATION_ERROR", "raw is required to send a message", 400)

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().messages().send(userId=userId, body={"raw": raw}).execute()
            tlog.success()
            return SendMessageResult(success=True, statusCode=200, data=SendMessageData(**data))
        except Exception as exc:
            return _handle_request_exc(SendMessageResult, tlog, exc)

    @mcp.tool(
        name="trash_message",
        description=(
            "Moves the specified message to the trash. This changes the message's labels "
            "(typically adding TRASH and removing INBOX) — everything else about the message "
            "keeps its current value. NOTE: this overwrites the current label state — the "
            "original state is not stored after the call. The response includes both the "
            "before and after state of the message so you have a full record of what changed. "
            "Moves the specified message to the trash."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def trash_message(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the message to trash."),
    ) -> TrashMessageResult:
        tlog = ToolLogger(logger, "trash_message")

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().messages().get(userId=userId, id=id).execute()
            after = gmail_service.users().messages().trash(userId=userId, id=id).execute()
            tlog.success()
            return TrashMessageResult(
                success=True,
                statusCode=200,
                data=TrashMessageData(before=GetMessageData(**before), after=GetMessageData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(TrashMessageResult, tlog, exc)

    @mcp.tool(
        name="untrash_message",
        description=(
            "Removes the specified message from the trash. This changes the message's labels "
            "(typically removing TRASH) — everything else about the message keeps its current "
            "value. NOTE: this overwrites the current label state — the original state is not "
            "stored after the call. The response includes both the before and after state of "
            "the message so you have a full record of what changed. "
            "Removes the specified message from the trash."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def untrash_message(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the message to remove from trash."),
    ) -> UntrashMessageResult:
        tlog = ToolLogger(logger, "untrash_message")

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().messages().get(userId=userId, id=id).execute()
            after = gmail_service.users().messages().untrash(userId=userId, id=id).execute()
            tlog.success()
            return UntrashMessageResult(
                success=True,
                statusCode=200,
                data=UntrashMessageData(before=GetMessageData(**before), after=GetMessageData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(UntrashMessageResult, tlog, exc)
