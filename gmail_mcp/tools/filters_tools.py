"""Filters group: create_filter, delete_filter, get_filter, list_filters."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.filters import (
    DeleteFilterData,
    DeleteFilterResult,
    FilterData,
    FilterResult,
    FiltersData,
    FiltersResult,
)
from ._helpers import _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.filters")


def register_filters_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_filter",
        description=(
            "Creates a mail filter (an account can have a maximum of 1,000 filters)."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_filter(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        from_: str | None = Field(
            default=None,
            alias="from",
            description="Sender's display name or email address. Maps to the filter's `criteria.from`.",
        ),
        to: str | None = Field(
            default=None,
            description=(
                "Recipient's display name or email address (matches To/Cc/Bcc). "
                "Maps to the filter's `criteria.to`."
            ),
        ),
        subject: str | None = Field(
            default=None,
            description=(
                "Case-insensitive phrase in the subject; whitespace trimmed/collapsed. "
                "Maps to the filter's `criteria.subject`."
            ),
        ),
        query: str | None = Field(
            default=None,
            description=(
                "Only match messages matching this query, in Gmail search-box syntax. "
                "Maps to the filter's `criteria.query`."
            ),
        ),
        negatedQuery: str | None = Field(
            default=None,
            description=(
                "Only match messages NOT matching this query, same syntax. "
                "Maps to the filter's `criteria.negatedQuery`."
            ),
        ),
        hasAttachment: bool | None = Field(
            default=None,
            description="Whether the message has any attachment. Maps to the filter's `criteria.hasAttachment`.",
        ),
        excludeChats: bool | None = Field(
            default=None,
            description="Whether to exclude chats from the match. Maps to the filter's `criteria.excludeChats`.",
        ),
        size: int | None = Field(
            default=None,
            description=(
                "Size of the entire RFC822 message in bytes (headers + attachments), compared "
                "per `sizeComparison`. Maps to the filter's `criteria.size`."
            ),
        ),
        sizeComparison: str | None = Field(
            default=None,
            description=(
                "How `size` should relate to the actual message size. Enum values "
                "(`SizeComparison`): `unspecified`, `smaller`, `larger`. Maps to the filter's "
                "`criteria.sizeComparison`."
            ),
        ),
        addLabelIds: list[str] | None = Field(
            default=None,
            description="Labels to add to matching messages. Maps to the filter's `action.addLabelIds`.",
        ),
        removeLabelIds: list[str] | None = Field(
            default=None,
            description="Labels to remove from matching messages. Maps to the filter's `action.removeLabelIds`.",
        ),
        forward: str | None = Field(
            default=None,
            description=(
                "Email address to forward matching messages to, keeping the original sender "
                "in From. Maps to the filter's `action.forward`."
            ),
        ),
    ) -> FilterResult:
        tlog = ToolLogger(logger, "create_filter")

        criteria = {
            k: v
            for k, v in {
                "from": from_,
                "to": to,
                "subject": subject,
                "query": query,
                "negatedQuery": negatedQuery,
                "hasAttachment": hasAttachment,
                "excludeChats": excludeChats,
                "size": size,
                "sizeComparison": sizeComparison,
            }.items()
            if v is not None
        }
        if not criteria:
            return _err(
                FilterResult, tlog, "VALIDATION_ERROR",
                "criteria is required: provide at least one criteria field "
                "(from_, to, subject, query, negatedQuery, hasAttachment, excludeChats, size, sizeComparison)",
                400,
            )

        action = {
            k: v
            for k, v in {
                "addLabelIds": addLabelIds,
                "removeLabelIds": removeLabelIds,
                "forward": forward,
            }.items()
            if v is not None
        }
        if not action:
            return _err(
                FilterResult, tlog, "VALIDATION_ERROR",
                "action is required: provide at least one action field (addLabelIds, removeLabelIds, forward)",
                400,
            )

        try:
            gmail_service = service.get_service()
            body = {"criteria": criteria, "action": action}
            data = gmail_service.users().settings().filters().create(userId=userId, body=body).execute()
            tlog.success()
            return FilterResult(success=True, statusCode=200, data=FilterData(**data))
        except Exception as exc:
            return _handle_request_exc(FilterResult, tlog, exc)

    @mcp.tool(
        name="delete_filter",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Immediately and permanently deletes the specified filter. "
            "This action is irreversible — the filter's criteria and actions cannot be recovered once deleted. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_filter(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the filter to delete."),
    ) -> DeleteFilterResult:
        tlog = ToolLogger(logger, "delete_filter")

        if not id:
            return _err(DeleteFilterResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            gmail_service.users().settings().filters().delete(userId=userId, id=id).execute()
            tlog.success()
            return DeleteFilterResult(success=True, statusCode=200, data=DeleteFilterData())
        except Exception as exc:
            return _handle_request_exc(DeleteFilterResult, tlog, exc)

    @mcp.tool(
        name="get_filter",
        description="Gets the specified filter.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_filter(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        id: str = Field(description="The ID of the filter to fetch."),
    ) -> FilterResult:
        tlog = ToolLogger(logger, "get_filter")

        if not id:
            return _err(FilterResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().settings().filters().get(userId=userId, id=id).execute()
            tlog.success()
            return FilterResult(success=True, statusCode=200, data=FilterData(**data))
        except Exception as exc:
            return _handle_request_exc(FilterResult, tlog, exc)

    @mcp.tool(
        name="list_filters",
        description="Lists the message filters of the Gmail user.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_filters(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
    ) -> FiltersResult:
        tlog = ToolLogger(logger, "list_filters")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().settings().filters().list(userId=userId).execute()
            tlog.success()
            return FiltersResult(success=True, statusCode=200, data=FiltersData(**data))
        except Exception as exc:
            return _handle_request_exc(FiltersResult, tlog, exc)
