"""Configuration for MewCP Gmail MCP Server."""

import logging
import os

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

# OAuth servers only. One entry per scope a tool in tools/ actually calls.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",         # profile, history: read mailbox metadata and content
    "https://www.googleapis.com/auth/gmail.modify",            # messages, threads, labels: read + non-destructive mailbox writes
    "https://www.googleapis.com/auth/gmail.compose",           # drafts: create, read, update, delete, and send drafts
    "https://www.googleapis.com/auth/gmail.labels",             # labels: create, read, update, and delete labels
    "https://www.googleapis.com/auth/gmail.settings.basic",     # settings, filters, send_as: read/write mailbox settings
    "https://www.googleapis.com/auth/gmail.settings.sharing",   # forwarding_addresses, send_as: manage forwarding addresses + send-as aliases
]

# No {NAME}_API_BASE and no CONNECT_TIMEOUT/READ_TIMEOUT — the Google API Python Client
# SDK manages request construction, retries, and endpoint URLs internally.


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
