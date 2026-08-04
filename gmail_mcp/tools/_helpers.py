"""Shared error and MIME-building helpers for all tool modules."""

import base64
from email.mime.text import MIMEText

from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError

from ..logging_utils import ToolLogger
from ..schemas import ToolError

USER_ID_DESC = (
    "The user's email address. Defaults to `me`, which refers to the authenticated user "
    "and is correct for almost every call — only override this if the token has delegated "
    "access to another mailbox."
)

LABEL_ID_GUIDANCE = (
    "System labels use fixed well-known strings (INBOX, UNREAD, SPAM, TRASH, IMPORTANT, "
    "STARRED, DRAFT, SENT, CATEGORY_PERSONAL, CATEGORY_SOCIAL, CATEGORY_PROMOTIONS, "
    "CATEGORY_UPDATES, CATEGORY_FORUMS). User-created labels use opaque IDs like "
    "`Label_8927364` — call list_labels first to resolve the correct ID; never guess or "
    "invent one."
)


def _err(result_class, tlog, code, message, status, retriable=False, retry_after=None):
    tlog.failure(code, message)
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code=code, message=message),
    )


def _handle_request_exc(result_class, tlog, exc):
    if isinstance(exc, HttpError):
        status = exc.resp.status if exc.resp is not None else 500
        retriable = status in (429, 500, 502, 503)
        tlog.failure("UPSTREAM_ERROR", f"HTTP {status}")
        return result_class(success=False, statusCode=status, retriable=retriable,
            error=ToolError(code="UPSTREAM_ERROR", message=f"HTTP {status}"))
    if isinstance(exc, RefreshError):
        tlog.failure("AUTH_ERROR", str(exc))
        return result_class(success=False, statusCode=401, retriable=False,
            error=ToolError(code="AUTH_ERROR", message=str(exc)))
    if isinstance(exc, ValueError):
        tlog.failure("AUTH_ERROR", str(exc))
        return result_class(success=False, statusCode=401, retriable=False,
            error=ToolError(code="AUTH_ERROR", message=str(exc)))
    tlog.failure("SERVER_ERROR", str(exc))  # log full detail internally
    return result_class(success=False, statusCode=500, retriable=False,
        error=ToolError(code="SERVER_ERROR", message="Unexpected server error"))


def _upstream_err(result_class, tlog, status, data, retry_after=None):
    retriable = status in (429, 500, 502, 503)
    tlog.failure("UPSTREAM_ERROR", f"HTTP {status}")
    msg = data.get("error") or data.get("message") or f"HTTP {status}"
    return result_class(
        success=False, statusCode=status, retriable=retriable,
        retry_after_seconds=retry_after,
        error=ToolError(code="UPSTREAM_ERROR", message=str(msg)),
    )


def _build_mime_message(
    *, to=None, subject=None, body="", cc=None, bcc=None, html=False,
    in_reply_to=None, references=None,
):
    """Builds an RFC 2822 message from plain fields, base64url-encoded for the `raw` field."""
    msg = MIMEText(body or "", "html" if html else "plain")
    if to:
        msg["To"] = to
    if subject:
        msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references
    return base64.urlsafe_b64encode(msg.as_bytes()).decode()
