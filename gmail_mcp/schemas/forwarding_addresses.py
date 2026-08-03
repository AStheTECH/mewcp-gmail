from pydantic import BaseModel, ConfigDict

from ._base import ToolResult


class ForwardingAddressData(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardingEmail: str | None = None
    verificationStatus: str | None = None


class ForwardingAddressResult(ToolResult):
    data: ForwardingAddressData | None = None


class ForwardingAddressesData(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardingAddresses: list[ForwardingAddressData] | None = None


class ForwardingAddressesResult(ToolResult):
    data: ForwardingAddressesData | None = None
