from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class AutoForwardingSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool | None = None
    emailAddress: str | None = None
    disposition: str | None = None


class AutoForwardingSettingsResult(ToolResult):
    data: AutoForwardingSettingsData | None = None


class VacationSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    enableAutoReply: bool | None = None
    responseSubject: str | None = None
    responseBodyPlainText: str | None = None
    responseBodyHtml: str | None = None
    restrictToContacts: bool | None = None
    restrictToDomain: bool | None = None
    startTime: str | None = None
    endTime: str | None = None
    # Populated only by update_vacation_settings, which reports the pre-update
    # state alongside the (top-level) post-update state. Left unset by
    # get_vacation_settings, which only ever reports the current state.
    before: "VacationSettingsData | None" = None


class VacationSettingsResult(ToolResult):
    data: VacationSettingsData | None = None
