"""Example client for interacting with the A2A agent system."""

import asyncio
import requests
from typing import Dict, Any
from config import Config


class A2AClient:
    """Client for interacting with A2A agents."""

    def __init__(self, base_url: str):
        """
        Initialize the A2A client.

        Args:
            base_url: Base URL of the agent service
        """
        self.base_url = base_url.rstrip("/")

    def get_agent_card(self) -> Dict[str, Any]:
        """Get the agent card."""
        response = requests.get(f"{self.base_url}/agent-card")
        response.raise_for_status()
        return response.json()

    def chat(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Send a chat message to the agent.

        Args:
            message: The message to send
            context: Optional context information

        Returns:
            Agent's response
        """
        payload = {"message": message}
        if context:
            payload["context"] = context

        response = requests.post(f"{self.base_url}/chat", json=payload)
        response.raise_for_status()
        return response.json()["response"]

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific tool on the agent.

        Args:
            tool_name: Name of the tool
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        payload = {"tool_name": tool_name, "parameters": parameters}

        response = requests.post(f"{self.base_url}/execute-tool", json=payload)
        response.raise_for_status()
        return response.json()["result"]

    def get_tools(self) -> Dict[str, Any]:
        """Get available tools."""
        response = requests.get(f"{self.base_url}/tools")
        response.raise_for_status()
        return response.json()


def main():
    """Example usage of the A2A client."""
    print("=== Google ADK A2A Multi-Agent System Client ===\n")

    # Create clients for each agent
    orchestrator = A2AClient(f"http://localhost:{Config.ORCHESTRATOR_PORT}")

    try:
        # Example 1: Chat with orchestrator
        print("1. Chatting with Orchestrator:")
        response = orchestrator.chat(
            "What agents are available and what can they do?"
        )
        print(f"Response: {response}\n")

        # Example 2: Get agent card
        print("2. Getting Orchestrator Agent Card:")
        card = orchestrator.get_agent_card()
        print(f"Name: {card['name']}")
        print(f"Description: {card['description']}\n")

        # Example 3: List available tools
        print("3. Available Tools:")
        tools = orchestrator.get_tools()
        for tool in tools.get("tools", []):
            print(f"  - {tool['name']}: {tool['description']}")
        print()

        # Example 4: Execute a tool
        print("4. Executing 'list_available_agents' tool:")
        result = orchestrator.execute_tool("list_available_agents", {})
        print(f"Available agents: {len(result['agents'])}")
        for agent in result["agents"]:
            print(f"  - {agent['name']}: {agent['description']}")
        print()

        # Example 5: Interact with BigQuery agent (if running)
        print("5. Interacting with BigQuery Agent:")
        bigquery_client = A2AClient(f"http://localhost:{Config.BIGQUERY_AGENT_PORT}")
        try:
            # List datasets
            datasets = bigquery_client.execute_tool("list_datasets", {})
            print(f"Datasets: {datasets}")
        except Exception as e:
            print(f"Note: BigQuery agent not running or error occurred: {e}")
        print()

        # Example 6: Interact with Ticket agent (if running)
        print("6. Creating a ticket:")
        ticket_client = A2AClient(f"http://localhost:{Config.TICKET_AGENT_PORT}")
        try:
            ticket = ticket_client.execute_tool(
                "create_ticket",
                {
                    "title": "Test ticket from client",
                    "description": "This is a test ticket created via the A2A API",
                    "category": "question",
                    "priority": "medium",
                },
            )
            print(f"Created ticket: {ticket['ticket_id']}")
            print(f"Status: {ticket['ticket']['status']}")
        except Exception as e:
            print(f"Note: Ticket agent not running or error occurred: {e}")
        print()

        # Example 7: Interact with Maps agent (if running)
        print("7. Geocoding an address:")
        maps_client = A2AClient(f"http://localhost:{Config.MAPS_AGENT_PORT}")
        try:
            location = maps_client.execute_tool(
                "geocode",
                {"address": "1600 Amphitheatre Parkway, Mountain View, CA"},
            )
            print(f"Location: {location}")
        except Exception as e:
            print(f"Note: Maps agent not running or error occurred: {e}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to agent. Make sure the agent is running.")
        print(f"Start the orchestrator with: python a2a_server.py --agent orchestrator")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

