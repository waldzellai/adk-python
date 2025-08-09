"""
Smithery MCP Agent Example Package

This package demonstrates integration between Google's ADK and Smithery CLI
for managing MCP (Model Context Protocol) servers.
"""

from .smithery_mcp_agent import SmitheryMCPAgent, create_agent
from .smithery_tools import (
    SmitherySearchTool,
    SmitheryInstallTool,
    SmitheryInspectTool,
    MCPServerManagerTool,
    create_smithery_tools,
)

__version__ = "1.0.0"
__all__ = [
    "SmitheryMCPAgent",
    "create_agent",
    "SmitherySearchTool",
    "SmitheryInstallTool",
    "SmitheryInspectTool",
    "MCPServerManagerTool",
    "create_smithery_tools",
]