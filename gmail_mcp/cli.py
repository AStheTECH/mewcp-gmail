"""CLI argument parsing for MewCP MCP Server."""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MewCP MCP Server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="streamable-http")
    parser.add_argument("--host", default=None)
    parser.add_argument("--port", type=int, default=None)
    return parser.parse_args()
