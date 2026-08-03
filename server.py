#!/usr/bin/env python3
"""MewCP Gmail MCP Server."""

import logging

from fastmcp import FastMCP
from starlette.responses import JSONResponse

from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend

from gmail_mcp.cli import parse_args
from gmail_mcp.config import BREAKING_CHANGES, SERVER_VERSION, configure_logging
from gmail_mcp.tools import register_tools

configure_logging()
logger = logging.getLogger("gmail-mcp")

backend = HeaderCredentialBackend()
mcp = FastMCP("MewCP Gmail MCP Server", version=SERVER_VERSION,
              middleware=[CredentialMiddleware(backend, "oauth")])

register_tools(mcp)


# /health MUST come before mcp.http_app() — routes are baked at http_app() time
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({
        "status": "healthy",
        "service": mcp.name,
        "version": SERVER_VERSION,
        "breaking_changes": BREAKING_CHANGES,
    })


app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)


if __name__ == "__main__":
    args = parse_args()
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
    if args.host:
        run_kwargs["host"] = args.host
    if args.port:
        run_kwargs["port"] = args.port
    try:
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server crashed: %s", e, exc_info=True)
        raise
