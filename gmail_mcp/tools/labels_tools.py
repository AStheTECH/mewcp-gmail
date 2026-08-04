"""Labels group: create_label, delete_label, get_label, list_labels, update_label."""

import logging
from typing import Literal

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.labels import (
    DeleteLabelData,
    DeleteLabelResult,
    LabelData,
    LabelResult,
    LabelsData,
    LabelsResult,
    UpdateLabelData,
    UpdateLabelResult,
)
from ._helpers import USER_ID_DESC, _err, _handle_request_exc

logger = logging.getLogger("gmail-mcp.tools.labels")


def register_labels_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_label",
        description="Creates a label.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_label(
        name: str = Field(description="The display name of the label."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
        messageListVisibility: Literal["show", "hide"] | None = Field(
            default=None,
            description="Visibility of messages with this label in the Gmail web message list.",
        ),
        labelListVisibility: Literal["labelShow", "labelShowIfUnread", "labelHide"] | None = Field(
            default=None,
            description="Visibility of the label itself in the Gmail web label list.",
        ),
        type: Literal["system", "user"] | None = Field(
            default=None,
            description=(
                "Owner type. `system` labels are internally created by Gmail and cannot be "
                "added/modified/deleted. `user` labels are created by the user/app."
            ),
        ),
        color_text_color: str | None = Field(
            default=None,
            description=(
                "Text color hex string for the label, chosen from Gmail's fixed color palette. "
                "Only available for `type: user` labels; must be set together with "
                "`color_background_color`."
            ),
        ),
        color_background_color: str | None = Field(
            default=None,
            description=(
                "Background color hex string for the label, chosen from Gmail's fixed color "
                "palette. Only available for `type: user` labels; must be set together with "
                "`color_text_color`."
            ),
        ),
    ) -> LabelResult:
        tlog = ToolLogger(logger, "create_label")

        if not name:
            return _err(LabelResult, tlog, "VALIDATION_ERROR", "name is required", 400)
        if (color_text_color is None) != (color_background_color is None):
            return _err(
                LabelResult, tlog, "VALIDATION_ERROR",
                "color_text_color and color_background_color must both be set together", 400,
            )

        body: dict = {"name": name}
        if messageListVisibility is not None:
            body["messageListVisibility"] = messageListVisibility
        if labelListVisibility is not None:
            body["labelListVisibility"] = labelListVisibility
        if type is not None:
            body["type"] = type
        if color_text_color is not None and color_background_color is not None:
            body["color"] = {"textColor": color_text_color, "backgroundColor": color_background_color}

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().labels().create(userId=userId, body=body).execute()
            tlog.success()
            return LabelResult(success=True, statusCode=200, data=LabelData(**data))
        except Exception as exc:
            return _handle_request_exc(LabelResult, tlog, exc)

    @mcp.tool(
        name="delete_label",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. "
            "Immediately and permanently deletes the specified label and removes it from any "
            "messages and threads it's applied to. "
            "This action is irreversible — the label and its associations with messages and "
            "threads cannot be recovered. "
            "NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_label(
        id: str = Field(description="The ID of the label to delete."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> DeleteLabelResult:
        tlog = ToolLogger(logger, "delete_label")

        if not id:
            return _err(DeleteLabelResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            gmail_service.users().labels().delete(userId=userId, id=id).execute()
            tlog.success()
            return DeleteLabelResult(success=True, statusCode=200, data=DeleteLabelData())
        except Exception as exc:
            return _handle_request_exc(DeleteLabelResult, tlog, exc)

    @mcp.tool(
        name="get_label",
        description="Gets the specified label.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_label(
        id: str = Field(description="The ID of the label to retrieve."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> LabelResult:
        tlog = ToolLogger(logger, "get_label")

        if not id:
            return _err(LabelResult, tlog, "VALIDATION_ERROR", "id is required", 400)

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().labels().get(userId=userId, id=id).execute()
            tlog.success()
            return LabelResult(success=True, statusCode=200, data=LabelData(**data))
        except Exception as exc:
            return _handle_request_exc(LabelResult, tlog, exc)

    @mcp.tool(
        name="list_labels",
        description="Lists all labels in the user's mailbox.",
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def list_labels(
        userId: str | None = Field(default="me", description=USER_ID_DESC),
    ) -> LabelsResult:
        tlog = ToolLogger(logger, "list_labels")

        try:
            gmail_service = service.get_service()
            data = gmail_service.users().labels().list(userId=userId).execute()
            tlog.success()
            return LabelsResult(success=True, statusCode=200, data=LabelsData(**data))
        except Exception as exc:
            return _handle_request_exc(LabelsResult, tlog, exc)

    @mcp.tool(
        name="update_label",
        description=(
            "NOTE: this overwrites the current field values — the original state is not stored "
            "after the call. The response includes both the before and after state so you have "
            "a full record of what changed. "
            "Partially updates the specified label (only the fields provided are changed)."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_label(
        id: str = Field(description="The ID of the label to update."),
        userId: str | None = Field(default="me", description=USER_ID_DESC),
        name: str | None = Field(default=None, description="The display name of the label."),
        messageListVisibility: Literal["show", "hide"] | None = Field(
            default=None,
            description="Visibility of messages with this label in the Gmail web message list.",
        ),
        labelListVisibility: Literal["labelShow", "labelShowIfUnread", "labelHide"] | None = Field(
            default=None,
            description="Visibility of the label itself in the Gmail web label list.",
        ),
        type: Literal["system", "user"] | None = Field(
            default=None,
            description=(
                "System labels cannot actually be renamed/recolored even though the field is "
                "present."
            ),
        ),
        color_text_color: str | None = Field(
            default=None,
            description=(
                "Text color hex string, chosen from Gmail's fixed color palette; must be set "
                "together with `color_background_color`. Only applies to `type: user` labels."
            ),
        ),
        color_background_color: str | None = Field(
            default=None,
            description=(
                "Background color hex string, chosen from Gmail's fixed color palette; must be "
                "set together with `color_text_color`. Only applies to `type: user` labels."
            ),
        ),
    ) -> UpdateLabelResult:
        tlog = ToolLogger(logger, "update_label")

        if not id:
            return _err(UpdateLabelResult, tlog, "VALIDATION_ERROR", "id is required", 400)
        if (color_text_color is None) != (color_background_color is None):
            return _err(
                UpdateLabelResult, tlog, "VALIDATION_ERROR",
                "color_text_color and color_background_color must both be set together", 400,
            )

        body: dict = {}
        if name is not None:
            body["name"] = name
        if messageListVisibility is not None:
            body["messageListVisibility"] = messageListVisibility
        if labelListVisibility is not None:
            body["labelListVisibility"] = labelListVisibility
        if type is not None:
            body["type"] = type
        if color_text_color is not None and color_background_color is not None:
            body["color"] = {"textColor": color_text_color, "backgroundColor": color_background_color}

        try:
            gmail_service = service.get_service()
            before = gmail_service.users().labels().get(userId=userId, id=id).execute()
            after = gmail_service.users().labels().patch(userId=userId, id=id, body=body).execute()
            tlog.success()
            return UpdateLabelResult(
                success=True,
                statusCode=200,
                data=UpdateLabelData(before=LabelData(**before), after=LabelData(**after)),
            )
        except Exception as exc:
            return _handle_request_exc(UpdateLabelResult, tlog, exc)
