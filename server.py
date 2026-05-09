#!/usr/bin/env python3
"""MCP Server for Gmail API."""

import logging

from fastmcp import FastMCP

from gmail_mcp.cli import parse_args
from gmail_mcp.config import configure_logging
from gmail_mcp.tools import register_tools
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend

configure_logging()
logger = logging.getLogger("gmail-mcp-server")

backend = HeaderCredentialBackend()
mcp = FastMCP(
    "CL Gmail MCP Server", middleware=[CredentialMiddleware(backend, "oauth")]
)
register_tools(mcp)

app = mcp.http_app(path="/mcp", transport="streamable-http")


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Gmail MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
