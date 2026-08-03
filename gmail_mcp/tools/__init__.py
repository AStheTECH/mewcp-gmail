"""MewCP Gmail tool registration."""

from fastmcp import FastMCP

from .profile_tools import register_profile_tools
from .drafts_tools import register_drafts_tools
from .labels_tools import register_labels_tools
from .messages_tools import register_messages_tools
from .threads_tools import register_threads_tools
from .history_tools import register_history_tools
from .settings_tools import register_settings_tools
from .filters_tools import register_filters_tools
from .forwarding_addresses_tools import register_forwarding_addresses_tools
from .send_as_tools import register_send_as_tools


def register_tools(mcp: FastMCP) -> None:
    register_profile_tools(mcp)
    register_drafts_tools(mcp)
    register_labels_tools(mcp)
    register_messages_tools(mcp)
    register_threads_tools(mcp)
    register_history_tools(mcp)
    register_settings_tools(mcp)
    register_filters_tools(mcp)
    register_forwarding_addresses_tools(mcp)
    register_send_as_tools(mcp)
