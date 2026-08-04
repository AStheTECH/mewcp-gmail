"""Forwarding addresses group: get_forwarding_address, list_forwarding_addresses."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.forwarding_addresses import (
    ForwardingAddressData,
    ForwardingAddressesData,
    ForwardingAddressesResult,
    ForwardingAddressResult,
)
from ._helpers import USER_ID_DESC, _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.forwarding_addresses")


def register_forwarding_addresses_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_forwarding_address",
        description="Gets the specified forwarding address.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_forwarding_address(
        forwardingEmail: str = Field(description="The forwarding address to retrieve."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> ForwardingAddressResult:
        tlog = ToolLogger(logger, "get_forwarding_address")

        if not forwardingEmail:
            return _err(
                ForwardingAddressResult, tlog, "VALIDATION_ERROR", "forwardingEmail is required", 400
            )

        try:
            gmail_service = service.get_service()
            data = (
                gmail_service.users()
                .settings()
                .forwardingAddresses()
                .get(userId=userId, forwardingEmail=forwardingEmail)
                .execute()
            )
            tlog.success()
            return ForwardingAddressResult(success=True, statusCode=200, data=ForwardingAddressData(**data))
        except Exception as exc:
            return _handle_request_exc(ForwardingAddressResult, tlog, exc)

    @mcp.tool(
        name="list_forwarding_addresses",
        description="Lists the forwarding addresses for the specified account.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_forwarding_addresses(
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> ForwardingAddressesResult:
        tlog = ToolLogger(logger, "list_forwarding_addresses")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().settings().forwardingAddresses().list(userId=userId).execute()
            tlog.success()
            return ForwardingAddressesResult(
                success=True, statusCode=200, data=ForwardingAddressesData(**data)
            )
        except Exception as exc:
            return _handle_request_exc(ForwardingAddressesResult, tlog, exc)
