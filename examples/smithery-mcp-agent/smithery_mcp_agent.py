#!/usr/bin/env python3
"""
Smithery MCP Agent Example

This example demonstrates how to build an agent using Google's Agent Development Kit (ADK)
that integrates with the Smithery CLI to discover, install, and use MCP (Model Context Protocol) servers.

The agent can:
- Search for MCP servers using Smithery's registry
- Install MCP servers locally
- Configure and use installed MCP servers
- Execute tools provided by MCP servers
"""

import asyncio
import json
import os
import subprocess
from typing import Any, Dict, List, Optional

from google.adk import agents, models, planner_base, tools
from google.adk.events import EventListener
from google.adk.models import google_genai
from google.adk.planners import default_planner
from google.adk.runners import AIRunner
from google.adk.sessions import InMemorySession
from google.adk.tools.function_tool import FunctionTool

# Import custom tools for Smithery integration
from smithery_tools import (
    SmitherySearchTool,
    SmitheryInstallTool,
    SmitheryInspectTool,
    MCPServerManagerTool,
)


class SmitheryMCPAgent(agents.Agent):
    """An agent that can discover, install, and use MCP servers via Smithery CLI."""
    
    def __init__(
        self,
        model: models.Model,
        smithery_config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize the Smithery MCP Agent.
        
        Args:
            model: The language model to use
            smithery_config: Optional configuration for Smithery CLI
            **kwargs: Additional arguments passed to parent Agent
        """
        super().__init__(model=model, **kwargs)
        
        self.smithery_config = smithery_config or {}
        self.installed_servers: Dict[str, Dict[str, Any]] = {}
        
        # Initialize tools
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all tools available to the agent."""
        # Smithery CLI tools
        self.add_tool(SmitherySearchTool())
        self.add_tool(SmitheryInstallTool(config=self.smithery_config))
        self.add_tool(SmitheryInspectTool())
        self.add_tool(MCPServerManagerTool(self.installed_servers))
        
        # Additional utility tools
        self.add_tool(FunctionTool(
            name="list_installed_servers",
            description="List all currently installed MCP servers",
            function=self._list_installed_servers
        ))
        
        self.add_tool(FunctionTool(
            name="execute_mcp_tool",
            description="Execute a tool from an installed MCP server",
            function=self._execute_mcp_tool
        ))
    
    def _list_installed_servers(self) -> Dict[str, Any]:
        """List all installed MCP servers and their available tools."""
        return {
            "installed_servers": self.installed_servers,
            "count": len(self.installed_servers)
        }
    
    async def _execute_mcp_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool from an installed MCP server.
        
        Args:
            server_name: Name of the MCP server
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            Result from the MCP tool execution
        """
        if server_name not in self.installed_servers:
            return {
                "error": f"Server '{server_name}' not installed. Available servers: {list(self.installed_servers.keys())}"
            }
        
        server_info = self.installed_servers[server_name]
        
        # Here you would implement the actual MCP client connection
        # For this example, we'll show the structure
        return {
            "server": server_name,
            "tool": tool_name,
            "arguments": arguments,
            "status": "executed",
            "note": "In a real implementation, this would connect to the MCP server and execute the tool"
        }
    
    async def plan_and_execute(self, query: str) -> str:
        """
        Plan and execute actions based on the user query.
        
        Args:
            query: The user's request
            
        Returns:
            The result of executing the plan
        """
        # Create a planner with our tools
        planner = default_planner.DefaultPlanner(
            model=self.model,
            tools=self.tools
        )
        
        # Generate a plan
        plan = await planner.plan(query)
        
        # Execute the plan
        result = await self.execute_plan(plan)
        
        return result


def create_agent(
    api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-pro",
    smithery_config: Optional[Dict[str, Any]] = None
) -> SmitheryMCPAgent:
    """
    Create and configure a Smithery MCP Agent.
    
    Args:
        api_key: API key for the model (uses environment variable if not provided)
        model_name: Name of the model to use
        smithery_config: Configuration for Smithery CLI
        
    Returns:
        Configured SmitheryMCPAgent instance
    """
    # Initialize the model
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("API key must be provided or set in GOOGLE_API_KEY environment variable")
    
    model = google_genai.Gemini(
        model_name=model_name,
        api_key=api_key
    )
    
    # Create the agent
    agent = SmitheryMCPAgent(
        model=model,
        smithery_config=smithery_config
    )
    
    return agent


async def main():
    """Main function demonstrating the Smithery MCP Agent."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Create the agent
    agent = create_agent()
    
    # Example interactions
    print("Smithery MCP Agent Example")
    print("=" * 50)
    
    # Example 1: Search for MCP servers
    print("\n1. Searching for web search MCP servers...")
    result = await agent.plan_and_execute(
        "Search for MCP servers that provide web search capabilities"
    )
    print(f"Result: {result}")
    
    # Example 2: Install an MCP server
    print("\n2. Installing a web search MCP server...")
    result = await agent.plan_and_execute(
        "Install the exa web search MCP server"
    )
    print(f"Result: {result}")
    
    # Example 3: Use an installed MCP server
    print("\n3. Using the installed MCP server...")
    result = await agent.plan_and_execute(
        "Use the exa server to search for information about Agent Development Kit"
    )
    print(f"Result: {result}")
    
    # Example 4: List all installed servers
    print("\n4. Listing installed servers...")
    result = await agent.plan_and_execute(
        "Show me all the MCP servers I have installed"
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())