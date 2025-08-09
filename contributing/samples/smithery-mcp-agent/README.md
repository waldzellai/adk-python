# Smithery MCP Agent Example

This example demonstrates how to build an AI agent using Google's Agent Development Kit (ADK) that integrates with the [Smithery CLI](https://github.com/smithery-ai/cli) to discover, install, and use MCP (Model Context Protocol) servers.

## Overview

The Smithery MCP Agent showcases:
- 🔍 **Discovery**: Search for MCP servers in the Smithery registry
- 📦 **Installation**: Install MCP servers using Smithery CLI
- 🔧 **Configuration**: Configure MCP servers with API keys and settings
- 🚀 **Execution**: Use tools provided by installed MCP servers
- 🤖 **Integration**: Seamless integration between ADK and MCP ecosystem

## Architecture

```
┌─────────────────────┐
│   User Interface    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Smithery MCP Agent │
│       (ADK)         │
├─────────────────────┤
│  - Search Tools     │
│  - Install Tools    │
│  - Manager Tools    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   Smithery CLI      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   MCP Servers       │
│  - Exa Search       │
│  - File System      │
│  - Custom Tools     │
└─────────────────────┘
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16+ (for Smithery CLI)
- Google API key (for Gemini model)
- API keys for MCP servers you want to use (e.g., Exa API key)

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to the sample directory
cd contributing/samples/smithery-mcp-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# GOOGLE_API_KEY=your-google-api-key
# EXA_API_KEY=your-exa-api-key (optional)
```

### 3. Run the Agent

```bash
# Run the example
python smithery_mcp_agent.py
```

## Usage Examples

### Basic Usage

```python
from smithery_mcp_agent import create_agent
import asyncio

async def main():
    # Create the agent
    agent = create_agent()
    
    # Search for MCP servers
    result = await agent.plan_and_execute(
        "Find MCP servers for web searching"
    )
    print(result)
    
    # Install a server
    result = await agent.plan_and_execute(
        "Install the exa web search server"
    )
    print(result)
    
    # Use the installed server
    result = await agent.plan_and_execute(
        "Search for information about Agent Development Kit using exa"
    )
    print(result)

asyncio.run(main())
```

### Advanced Configuration

```python
# Create agent with custom configuration
agent = create_agent(
    model_name="gemini-1.5-flash",  # Use a different model
    smithery_config={
        "default_client": "cursor",   # Default to Cursor instead of Claude
        "cache_dir": "./mcp_cache"    # Custom cache directory
    }
)
```

### Using Configuration File

```python
import yaml

# Load configuration from file
with open("agent_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Create agent with file-based config
agent = create_agent(
    model_name=config["model"]["name"],
    smithery_config=config["smithery"]
)
```

## Available Tools

The agent provides several tools for MCP server management:

### 1. **smithery_search**
Search for MCP servers in the Smithery registry.

```python
await agent.execute_tool("smithery_search", {
    "query": "file system",
    "limit": 10
})
```

### 2. **smithery_install**
Install an MCP server using Smithery CLI.

```python
await agent.execute_tool("smithery_install", {
    "server_name": "@smithery/files",
    "client": "claude"
})
```

### 3. **smithery_inspect**
Inspect an MCP server to see available tools.

```python
await agent.execute_tool("smithery_inspect", {
    "server_name": "exa"
})
```

### 4. **mcp_server_manager**
Manage installed MCP servers (start, stop, configure).

```python
await agent.execute_tool("mcp_server_manager", {
    "action": "start",
    "server_name": "exa",
    "config": {"api_key": "your-key"}
})
```

## Configuration

### Agent Configuration (agent_config.yaml)

The agent can be configured using a YAML file with the following sections:

- **agent**: Basic agent metadata
- **model**: LLM configuration (provider, parameters)
- **smithery**: Smithery CLI settings
- **mcp_servers**: Default MCP server configurations
- **tools**: Tool execution settings
- **logging**: Logging configuration
- **security**: Security and sandboxing settings

See `agent_config.yaml` for a complete example.

### Environment Variables

Key environment variables:

- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `EXA_API_KEY`: API key for Exa search (if using)
- `SMITHERY_DEFAULT_CLIENT`: Default client for installations
- `AGENT_DEBUG`: Enable debug mode
- `AGENT_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Docker Support

Run the agent in a container:

```bash
# Build and run with docker-compose
docker-compose up

# Or build manually
docker build -t smithery-mcp-agent .
docker run -it --env-file .env smithery-mcp-agent
```

## Extending the Agent

### Adding Custom Tools

```python
from google.adk.tools import Tool

class CustomMCPTool(Tool):
    def __init__(self):
        super().__init__(
            name="custom_tool",
            description="My custom MCP tool"
        )
    
    async def execute(self, **kwargs):
        # Your tool logic here
        return {"result": "success"}

# Add to agent
agent.add_tool(CustomMCPTool())
```

### Custom MCP Server Integration

```python
# Implement a custom MCP client
class CustomMCPClient:
    async def connect(self, server_info):
        # Connect to MCP server
        pass
    
    async def execute_tool(self, tool_name, args):
        # Execute MCP tool
        pass

# Integrate with agent
agent.mcp_client = CustomMCPClient()
```

## Troubleshooting

### Common Issues

1. **Smithery CLI not found**
   - Ensure Node.js is installed
   - Run `npm install -g @smithery/cli`

2. **MCP server installation fails**
   - Check network connectivity
   - Verify client compatibility
   - Check Smithery CLI logs

3. **Tool execution timeout**
   - Increase timeout in configuration
   - Check MCP server status
   - Verify API keys are correct

### Debug Mode

Enable debug mode for detailed logging:

```bash
export AGENT_DEBUG=true
export AGENT_LOG_LEVEL=DEBUG
python smithery_mcp_agent.py
```

## Security Considerations

- **API Keys**: Store sensitive keys in environment variables
- **Sandboxing**: Enable sandbox mode in production
- **Domain Restrictions**: Configure allowed domains for web-based servers
- **Command Restrictions**: Limit allowed commands in sandbox mode

## Contributing

To contribute to this example:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Smithery CLI](https://github.com/smithery-ai/cli)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Smithery Registry](https://smithery.ai/)

## License

This example is provided under the same license as the ADK project.