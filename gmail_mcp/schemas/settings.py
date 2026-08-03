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


class VacationSettingsResult(ToolResult):
    data: VacationSettingsData | None = None


class UpdateVacationSettingsData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: VacationSettingsData
    after: VacationSettingsData


class UpdateVacationSettingsResult(ToolResult):
    data: UpdateVacationSettingsData | None = None
