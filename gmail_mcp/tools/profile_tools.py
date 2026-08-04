"""Profile group: get_profile."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.profile import ProfileData, ProfileResult
from ._helpers import USER_ID_DESC, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.profile")


def register_profile_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_profile",
        description=(
            "Gets the current user's Gmail profile, returning mailbox email address, "
            "message/thread totals, and current history ID."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_profile(
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> ProfileResult:
        tlog = ToolLogger(logger, "get_profile")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().getProfile(userId=userId).execute()
            tlog.success()
            return ProfileResult(success=True, statusCode=200, data=ProfileData(**data))
        except Exception as exc:
            return _handle_request_exc(ProfileResult, tlog, exc)
