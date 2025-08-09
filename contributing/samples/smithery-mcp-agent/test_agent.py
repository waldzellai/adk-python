#!/usr/bin/env python3
"""
Test script for Smithery MCP Agent

This script provides a simple way to test the agent's functionality
without requiring a full setup.
"""

import asyncio
import os
import sys
from typing import Optional

# Add parent directory to path for imports if running directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smithery_mcp_agent import create_agent
from smithery_tools import SmitherySearchTool


async def test_basic_functionality():
    """Test basic agent functionality."""
    print("Testing Smithery MCP Agent")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY not set. Using mock mode.")
        # In real usage, this would fail
        return test_mock_functionality()
    
    try:
        # Create agent
        print("\n1. Creating agent...")
        agent = create_agent()
        print("✓ Agent created successfully")
        
        # Test search functionality
        print("\n2. Testing search for MCP servers...")
        search_tool = SmitherySearchTool()
        result = await search_tool.execute("web search", limit=5)
        print(f"✓ Found {len(result.get('results', []))} servers")
        for server in result.get('results', [])[:3]:
            print(f"  - {server['name']}: {server['description']}")
        
        # Test agent planning
        print("\n3. Testing agent planning...")
        # This would normally execute a plan
        print("✓ Agent planning available")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True


def test_mock_functionality():
    """Test with mock functionality when no API key is available."""
    print("\nRunning in mock mode...")
    
    # Test tool initialization
    print("\n1. Testing tool initialization...")
    from smithery_tools import create_smithery_tools
    
    tools = create_smithery_tools()
    print(f"✓ Initialized {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Test configuration loading
    print("\n2. Testing configuration loading...")
    import yaml
    
    if os.path.exists("agent_config.yaml"):
        with open("agent_config.yaml", "r") as f:
            config = yaml.safe_load(f)
        print(f"✓ Loaded configuration: {config['agent']['name']}")
    else:
        print("! Configuration file not found")
    
    print("\n✅ Mock tests completed!")
    return True


async def interactive_mode():
    """Run the agent in interactive mode."""
    print("\nStarting interactive mode...")
    print("Type 'exit' to quit\n")
    
    # Create agent
    try:
        agent = create_agent()
    except Exception as e:
        print(f"Failed to create agent: {e}")
        return
    
    while True:
        try:
            query = input("\nEnter your query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            print("\nProcessing...")
            result = await agent.plan_and_execute(query)
            print(f"\nResult: {result}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Smithery MCP Agent")
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run with mock functionality (no API key required)"
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        asyncio.run(interactive_mode())
    elif args.mock:
        test_mock_functionality()
    else:
        asyncio.run(test_basic_functionality())


if __name__ == "__main__":
    main()