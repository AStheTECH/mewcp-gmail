from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class SmtpMsaData(BaseModel):
    model_config = ConfigDict(extra="allow")

    host: str | None = None
    port: int | None = None
    username: str | None = None
    password: str | None = None
    securityMode: str | None = None


class SendAsAliasData(BaseModel):
    model_config = ConfigDict(extra="allow")

    sendAsEmail: str | None = None
    displayName: str | None = None
    replyToAddress: str | None = None
    signature: str | None = None
    isPrimary: bool | None = None
    isDefault: bool | None = None
    treatAsAlias: bool | None = None
    smtpMsa: SmtpMsaData | None = None
    verificationStatus: str | None = None


class SendAsAliasResult(ToolResult):
    data: SendAsAliasData | None = None


class SendAsAliasesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    sendAs: list[SendAsAliasData] | None = None


class SendAsAliasesResult(ToolResult):
    data: SendAsAliasesData | None = None


class UpdateSendAsAliasData(BaseModel):
    model_config = ConfigDict(extra="allow")

    before: SendAsAliasData
    after: SendAsAliasData


class UpdateSendAsAliasResult(ToolResult):
    data: UpdateSendAsAliasData | None = None
