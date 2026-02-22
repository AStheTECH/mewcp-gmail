import logging
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .schemas import OAuthTokenData

logger = logging.getLogger("gmail-mcp-server")


def get_token_data(token_data: OAuthTokenData) -> dict[str, Any]:
    return {
        "token": token_data.get("token"),
        "refresh_token": token_data.get("refresh_token"),
        "token_uri": token_data.get("token_uri") or "https://oauth2.googleapis.com/token",
        "client_id": token_data.get("client_id"),
        "client_secret": token_data.get("client_secret"),
        "scopes": token_data.get("scopes"),
    }


def get_service(token_data: OAuthTokenData):
    auth_data = get_token_data(token_data)
    logger.info("Creating Gmail API service with provided access token")
    creds = Credentials(**auth_data)
    service = build("gmail", "v1", credentials=creds)
    logger.info("Gmail API service created successfully")
    return service
