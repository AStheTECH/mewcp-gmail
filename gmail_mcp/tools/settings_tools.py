"""Settings group: get_auto_forwarding_settings, get_vacation_settings, update_vacation_settings."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.settings import (
    AutoForwardingSettingsData,
    AutoForwardingSettingsResult,
    UpdateVacationSettingsData,
    UpdateVacationSettingsResult,
    VacationSettingsData,
    VacationSettingsResult,
)
from ._helpers import _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.settings")


def register_settings_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_auto_forwarding_settings",
        description="Gets the auto-forwarding setting for the account.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_auto_forwarding_settings(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
    ) -> AutoForwardingSettingsResult:
        tlog = ToolLogger(logger, "get_auto_forwarding_settings")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().settings().getAutoForwarding(userId=userId).execute()
            tlog.success()
            return AutoForwardingSettingsResult(
                success=True, statusCode=200, data=AutoForwardingSettingsData(**data)
            )
        except Exception as exc:
            return _handle_request_exc(AutoForwardingSettingsResult, tlog, exc)

    @mcp.tool(
        name="get_vacation_settings",
        description="Gets the vacation responder settings.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_vacation_settings(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
    ) -> VacationSettingsResult:
        tlog = ToolLogger(logger, "get_vacation_settings")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().settings().getVacation(userId=userId).execute()
            tlog.success()
            return VacationSettingsResult(success=True, statusCode=200, data=VacationSettingsData(**data))
        except Exception as exc:
            return _handle_request_exc(VacationSettingsResult, tlog, exc)

    @mcp.tool(
        name="update_vacation_settings",
        description=(
            "Updates the vacation responder settings. This first fetches the current settings "
            "so the response can report what changed. Only the fields you provide are changed — "
            "others keep their current value. NOTE: this overwrites the current field values — "
            "the original state is not stored after the call. The response includes both the "
            "before and after state (top-level fields are the post-update state, `data.before` "
            "holds the pre-update state) so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_vacation_settings(
        userId: str = Field(
            description=(
                "The user's email address. The special value `me` can be used to indicate "
                "the authenticated user."
            )
        ),
        enableAutoReply: bool | None = Field(
            default=None, description="Whether Gmail automatically replies to messages."
        ),
        responseSubject: str | None = Field(
            default=None,
            description=(
                "Text prepended to the subject line in vacation responses. Either this or the "
                "response body must be nonempty to enable auto-replies."
            ),
        ),
        responseBodyPlainText: str | None = Field(
            default=None,
            description=(
                "Response body in plain text. If both plain-text and HTML bodies are set, "
                "HTML is used."
            ),
        ),
        responseBodyHtml: str | None = Field(
            default=None,
            description=(
                "Response body in HTML (Gmail sanitizes it before storing). Used over plain "
                "text when both are set."
            ),
        ),
        restrictToContacts: bool | None = Field(
            default=None, description="Whether responses are limited to senders in the user's contacts."
        ),
        restrictToDomain: bool | None = Field(
            default=None,
            description=(
                "Whether responses are limited to senders in the user's domain. Google "
                "Workspace only."
            ),
        ),
        startTime: str | None = Field(
            default=None,
            description=(
                "Optional start time for auto-replies (epoch ms). Replies only to messages "
                "received after this time. Must precede endTime if both are set."
            ),
        ),
        endTime: str | None = Field(
            default=None,
            description=(
                "Optional end time for auto-replies (epoch ms). Replies only to messages "
                "received before this time. Must follow startTime if both are set."
            ),
        ),
    ) -> UpdateVacationSettingsResult:
        tlog = ToolLogger(logger, "update_vacation_settings")

        body = {
            k: v
            for k, v in {
                "enableAutoReply": enableAutoReply,
                "responseSubject": responseSubject,
                "responseBodyPlainText": responseBodyPlainText,
                "responseBodyHtml": responseBodyHtml,
                "restrictToContacts": restrictToContacts,
                "restrictToDomain": restrictToDomain,
                "startTime": startTime,
                "endTime": endTime,
            }.items()
            if v is not None
        }

        try:
            gmail_service = service.get_service()
            before_data = gmail_service.users().settings().getVacation(userId=userId).execute()
            after_data = (
                gmail_service.users()
                .settings()
                .updateVacation(userId=userId, body=body)
                .execute()
            )
            tlog.success()
            return UpdateVacationSettingsResult(
                success=True,
                statusCode=200,
                data=UpdateVacationSettingsData(
                    before=VacationSettingsData(**before_data),
                    after=VacationSettingsData(**after_data),
                ),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateVacationSettingsResult, tlog, exc)
