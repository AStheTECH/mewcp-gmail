"""Upstream API client for MewCP Gmail MCP Server."""

import logging

from fastmcp_credentials import get_credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger("gmail-mcp.service")


def get_service():
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("No OAuth access token available in credentials")

    # Google's installed-app OAuth flow issues an access token plus (when the user
    # granted offline access) a refresh token, client_id, client_secret, and token
    # endpoint — the same fields a locally cached token.json/credentials.json pair
    # would hold. Building a full Credentials object (not just the bare access token)
    # lets the client library refresh transparently via creds.refresh(Request())
    # whenever the access token has expired and a refresh_token is present.
    creds = Credentials(
        token=cred.access_token,
        refresh_token=getattr(cred, "refresh_token", None),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=getattr(cred, "client_id", None),
        client_secret=getattr(cred, "client_secret", None),
        scopes=getattr(cred, "scopes", None),
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("gmail", "v1", credentials=creds, cache_discovery=False)
