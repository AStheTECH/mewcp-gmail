"""Send-as group: get_send_as_alias, list_send_as_aliases, update_send_as_alias."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.send_as import (
    SendAsAliasData,
    SendAsAliasesData,
    SendAsAliasesResult,
    SendAsAliasResult,
    UpdateSendAsAliasData,
    UpdateSendAsAliasResult,
)
from ._helpers import USER_ID_DESC, _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.send_as")


def register_send_as_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_send_as_alias",
        description="Gets the specified send-as alias.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_send_as_alias(
        sendAsEmail: str = Field(description="The send-as alias to retrieve."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> SendAsAliasResult:
        tlog = ToolLogger(logger, "get_send_as_alias")

        if not sendAsEmail:
            return _err(SendAsAliasResult, tlog, "VALIDATION_ERROR", "sendAsEmail is required", 400)

        try:
            gmail_service = service.get_service()
            data = (
                gmail_service.users()
                .settings()
                .sendAs()
                .get(userId=userId, sendAsEmail=sendAsEmail)
                .execute()
            )
            tlog.success()
            return SendAsAliasResult(success=True, statusCode=200, data=SendAsAliasData(**data))
        except Exception as exc:
            return _handle_request_exc(SendAsAliasResult, tlog, exc)

    @mcp.tool(
        name="list_send_as_aliases",
        description=(
            "Lists the send-as aliases for the account, including the primary address and "
            'any custom "from" aliases.'
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_send_as_aliases(
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> SendAsAliasesResult:
        tlog = ToolLogger(logger, "list_send_as_aliases")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().settings().sendAs().list(userId=userId).execute()
            tlog.success()
            return SendAsAliasesResult(
                success=True, statusCode=200, data=SendAsAliasesData(**data)
            )
        except Exception as exc:
            return _handle_request_exc(SendAsAliasesResult, tlog, exc)

    @mcp.tool(
        name="update_send_as_alias",
        description=(
            "NOTE: this tool first fetches the alias's current state, then applies your "
            "changes — the response includes both the `before` and `after` state so you have "
            "a full record of what changed. Only the fields you provide are changed — others "
            "keep their current value. Partially updates the specified send-as alias."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_send_as_alias(
        sendAsEmail: str = Field(description="The send-as alias to update."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
        displayName: str | None = Field(
            default=None, description="Name shown in the From: header."
        ),
        replyToAddress: str | None = Field(
            default=None,
            description=(
                "Optional Reply-To: address. Empty means no Reply-To: header is generated."
            ),
        ),
        signature: str | None = Field(
            default=None,
            description=(
                "Optional HTML signature added to new messages composed with this alias in "
                "the Gmail web UI."
            ),
        ),
        isDefault: bool | None = Field(
            default=None,
            description="Whether this is the default From: address for new messages/vacation replies.",
        ),
        treatAsAlias: bool | None = Field(
            default=None,
            description=(
                "Whether Gmail should treat this address as an alias of the primary address. "
                "Custom \"from\" aliases only."
            ),
        ),
        smtpMsa: dict | None = Field(
            default=None,
            description=(
                "Optional outbound SMTP relay for mail sent with this alias (object (SmtpMsa)); "
                "custom aliases only. Keys: `host` (string, SMTP service hostname), `port` "
                "(integer, SMTP service port), `username` (string, write-only), `password` "
                "(string, write-only), `securityMode` (enum: `securityModeUnspecified`, `none`, "
                "`ssl`, `starttls`)."
            ),
        ),
    ) -> UpdateSendAsAliasResult:
        tlog = ToolLogger(logger, "update_send_as_alias")

        if not sendAsEmail:
            return _err(UpdateSendAsAliasResult, tlog, "VALIDATION_ERROR", "sendAsEmail is required", 400)

        try:
            gmail_service = service.get_service()
            before_data = (
                gmail_service.users()
                .settings()
                .sendAs()
                .get(userId=userId, sendAsEmail=sendAsEmail)
                .execute()
            )

            body = {}
            if displayName is not None:
                body["displayName"] = displayName
            if replyToAddress is not None:
                body["replyToAddress"] = replyToAddress
            if signature is not None:
                body["signature"] = signature
            if isDefault is not None:
                body["isDefault"] = isDefault
            if treatAsAlias is not None:
                body["treatAsAlias"] = treatAsAlias
            if smtpMsa is not None:
                body["smtpMsa"] = smtpMsa

            after_data = (
                gmail_service.users()
                .settings()
                .sendAs()
                .patch(userId=userId, sendAsEmail=sendAsEmail, body=body)
                .execute()
            )
            tlog.success()
            return UpdateSendAsAliasResult(
                success=True,
                statusCode=200,
                data=UpdateSendAsAliasData(
                    before=SendAsAliasData(**before_data),
                    after=SendAsAliasData(**after_data),
                ),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateSendAsAliasResult, tlog, exc)
