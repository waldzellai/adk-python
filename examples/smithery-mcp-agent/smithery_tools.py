"""
Smithery CLI Integration Tools

This module provides tools for interacting with the Smithery CLI to discover,
install, and manage MCP (Model Context Protocol) servers.
"""

import asyncio
import json
import subprocess
import shlex
from typing import Any, Dict, List, Optional, Tuple

from google.adk.tools import Tool
from google.adk.tools.function_tool import FunctionTool


class SmitherySearchTool(Tool):
    """Tool for searching MCP servers in the Smithery registry."""
    
    def __init__(self):
        super().__init__(
            name="smithery_search",
            description="Search for MCP servers in the Smithery registry by keyword or functionality"
        )
    
    async def execute(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for MCP servers.
        
        Args:
            query: Search query (e.g., "web search", "file system", etc.)
            limit: Maximum number of results to return
            
        Returns:
            Dictionary containing search results
        """
        # Note: Since Smithery doesn't have a direct search CLI command,
        # we'll simulate this by fetching from their registry API
        # In a real implementation, you might use their web API
        
        return {
            "query": query,
            "results": [
                {
                    "name": "exa",
                    "description": "Fast, intelligent web search and crawling",
                    "package": "exa",
                    "remote": True,
                    "tools_count": 6
                },
                {
                    "name": "@mnhlt/WebSearch-MCP",
                    "description": "Self-hosted web search API",
                    "package": "@mnhlt/WebSearch-MCP",
                    "remote": False,
                    "tools_count": 1
                }
            ],
            "note": "This is a simulated search. In production, use Smithery's API"
        }


class SmitheryInstallTool(Tool):
    """Tool for installing MCP servers using Smithery CLI."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            name="smithery_install",
            description="Install an MCP server using Smithery CLI"
        )
        self.config = config or {}
        self.default_client = self.config.get("default_client", "claude")
    
    async def execute(
        self,
        server_name: str,
        client: Optional[str] = None,
        config_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Install an MCP server.
        
        Args:
            server_name: Name of the server to install (e.g., "exa", "@org/server-name")
            client: Target client (e.g., "claude", "cursor", "cline")
            config_file: Optional path to configuration file
            
        Returns:
            Installation result
        """
        client = client or self.default_client
        
        # Construct the command
        cmd_parts = [
            "npx", "-y", "@smithery/cli", "install",
            server_name,
            "--client", client
        ]
        
        if config_file:
            cmd_parts.extend(["--config", config_file])
        
        try:
            # Run the installation command
            result = await self._run_command(cmd_parts)
            
            return {
                "server": server_name,
                "client": client,
                "status": "installed",
                "output": result[0],
                "command": " ".join(cmd_parts)
            }
        except Exception as e:
            return {
                "server": server_name,
                "client": client,
                "status": "failed",
                "error": str(e),
                "command": " ".join(cmd_parts)
            }
    
    async def _run_command(self, cmd_parts: List[str]) -> Tuple[str, str]:
        """Run a command asynchronously and return stdout, stderr."""
        process = await asyncio.create_subprocess_exec(
            *cmd_parts,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError(f"Command failed: {stderr.decode()}")
        
        return stdout.decode(), stderr.decode()


class SmitheryInspectTool(Tool):
    """Tool for inspecting MCP servers to see available tools."""
    
    def __init__(self):
        super().__init__(
            name="smithery_inspect",
            description="Inspect an MCP server to see its available tools and capabilities"
        )
    
    async def execute(self, server_name: str) -> Dict[str, Any]:
        """
        Inspect an MCP server.
        
        Args:
            server_name: Name of the server to inspect
            
        Returns:
            Server information including available tools
        """
        cmd_parts = [
            "npx", "-y", "@smithery/cli@latest", "inspect", server_name
        ]
        
        try:
            result = await self._run_command(cmd_parts)
            
            # Parse the output (this would need real parsing in production)
            return {
                "server": server_name,
                "status": "success",
                "output": result[0],
                "tools": self._parse_tools_from_output(result[0])
            }
        except Exception as e:
            return {
                "server": server_name,
                "status": "failed",
                "error": str(e)
            }
    
    async def _run_command(self, cmd_parts: List[str]) -> Tuple[str, str]:
        """Run a command asynchronously and return stdout, stderr."""
        process = await asyncio.create_subprocess_exec(
            *cmd_parts,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError(f"Command failed: {stderr.decode()}")
        
        return stdout.decode(), stderr.decode()
    
    def _parse_tools_from_output(self, output: str) -> List[Dict[str, str]]:
        """Parse tools from inspection output."""
        # This is a simplified parser - in production, you'd parse the actual output format
        tools = []
        lines = output.strip().split('\n')
        
        for line in lines:
            if "tool:" in line.lower() or "function:" in line.lower():
                # Extract tool information
                tools.append({
                    "name": "extracted_tool_name",
                    "description": "Tool description from output"
                })
        
        return tools


class MCPServerManagerTool(Tool):
    """Tool for managing installed MCP servers and their connections."""
    
    def __init__(self, installed_servers: Dict[str, Dict[str, Any]]):
        super().__init__(
            name="mcp_server_manager",
            description="Manage installed MCP servers - start, stop, configure"
        )
        self.installed_servers = installed_servers
    
    async def execute(
        self,
        action: str,
        server_name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Manage MCP servers.
        
        Args:
            action: Action to perform ("start", "stop", "configure", "status")
            server_name: Name of the server
            config: Optional configuration for the server
            
        Returns:
            Result of the action
        """
        if action == "start":
            return await self._start_server(server_name, config)
        elif action == "stop":
            return await self._stop_server(server_name)
        elif action == "configure":
            return await self._configure_server(server_name, config)
        elif action == "status":
            return await self._get_status(server_name)
        else:
            return {
                "error": f"Unknown action: {action}",
                "valid_actions": ["start", "stop", "configure", "status"]
            }
    
    async def _start_server(
        self,
        server_name: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Start an MCP server."""
        # In a real implementation, this would start the MCP server process
        self.installed_servers[server_name] = {
            "status": "running",
            "config": config or {},
            "pid": 12345  # Simulated PID
        }
        
        return {
            "server": server_name,
            "action": "start",
            "status": "success",
            "message": f"Server {server_name} started successfully"
        }
    
    async def _stop_server(self, server_name: str) -> Dict[str, Any]:
        """Stop an MCP server."""
        if server_name in self.installed_servers:
            self.installed_servers[server_name]["status"] = "stopped"
            return {
                "server": server_name,
                "action": "stop",
                "status": "success",
                "message": f"Server {server_name} stopped successfully"
            }
        else:
            return {
                "server": server_name,
                "action": "stop",
                "status": "error",
                "message": f"Server {server_name} not found"
            }
    
    async def _configure_server(
        self,
        server_name: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Configure an MCP server."""
        if server_name in self.installed_servers:
            self.installed_servers[server_name]["config"] = config
            return {
                "server": server_name,
                "action": "configure",
                "status": "success",
                "config": config
            }
        else:
            return {
                "server": server_name,
                "action": "configure",
                "status": "error",
                "message": f"Server {server_name} not found"
            }
    
    async def _get_status(self, server_name: str) -> Dict[str, Any]:
        """Get status of an MCP server."""
        if server_name in self.installed_servers:
            return {
                "server": server_name,
                "info": self.installed_servers[server_name]
            }
        else:
            return {
                "server": server_name,
                "status": "not_installed"
            }


# Utility function to create all Smithery tools
def create_smithery_tools(config: Optional[Dict[str, Any]] = None) -> List[Tool]:
    """
    Create all Smithery-related tools.
    
    Args:
        config: Optional configuration for tools
        
    Returns:
        List of initialized tools
    """
    installed_servers = {}
    
    return [
        SmitherySearchTool(),
        SmitheryInstallTool(config=config),
        SmitheryInspectTool(),
        MCPServerManagerTool(installed_servers)
    ]