"""Tests for agent functionality."""

import pytest
from agents import BigQueryAgent, TicketAgent, MapsAgent, OrchestratorAgent


class TestBaseAgent:
    """Test base agent functionality."""

    def test_bigquery_agent_initialization(self):
        """Test BigQuery agent initializes correctly."""
        agent = BigQueryAgent()
        assert agent.name == "BigQuery Agent"
        assert "BigQuery" in agent.description

    def test_ticket_agent_initialization(self):
        """Test Ticket agent initializes correctly."""
        agent = TicketAgent()
        assert agent.name == "Ticket Agent"
        assert "ticket" in agent.description.lower()

    def test_maps_agent_initialization(self):
        """Test Maps agent initializes correctly."""
        agent = MapsAgent()
        assert agent.name == "Maps Agent"
        assert "map" in agent.description.lower()

    def test_orchestrator_agent_initialization(self):
        """Test Orchestrator agent initializes correctly."""
        agent = OrchestratorAgent()
        assert agent.name == "Orchestrator Agent"
        assert len(agent.remote_agents) == 3


class TestAgentTools:
    """Test agent tool definitions."""

    def test_bigquery_tools(self):
        """Test BigQuery agent tools."""
        agent = BigQueryAgent()
        tools = agent.get_tools()
        assert len(tools) > 0
        tool_names = [tool["name"] for tool in tools]
        assert "execute_query" in tool_names
        assert "list_datasets" in tool_names

    def test_ticket_tools(self):
        """Test Ticket agent tools."""
        agent = TicketAgent()
        tools = agent.get_tools()
        assert len(tools) > 0
        tool_names = [tool["name"] for tool in tools]
        assert "create_ticket" in tool_names
        assert "update_ticket" in tool_names

    def test_maps_tools(self):
        """Test Maps agent tools."""
        agent = MapsAgent()
        tools = agent.get_tools()
        assert len(tools) > 0
        tool_names = [tool["name"] for tool in tools]
        assert "geocode" in tool_names
        assert "get_directions" in tool_names

    def test_orchestrator_tools(self):
        """Test Orchestrator agent tools."""
        agent = OrchestratorAgent()
        tools = agent.get_tools()
        assert len(tools) > 0
        tool_names = [tool["name"] for tool in tools]
        assert "list_available_agents" in tool_names


class TestAgentCards:
    """Test A2A agent cards."""

    def test_agent_card_structure(self):
        """Test agent card has correct structure."""
        agent = BigQueryAgent()
        card = agent.get_agent_card()
        
        assert "name" in card
        assert "description" in card
        assert "capabilities" in card
        assert "metadata" in card
        assert "tools" in card["capabilities"]


@pytest.mark.asyncio
class TestTicketAgent:
    """Test ticket agent operations."""

    async def test_create_ticket(self):
        """Test creating a ticket."""
        agent = TicketAgent()
        result = await agent.execute_tool(
            "create_ticket",
            {
                "title": "Test Ticket",
                "description": "Test description",
                "category": "bug",
                "priority": "high",
            },
        )
        
        assert result["success"] is True
        assert "ticket_id" in result
        assert result["ticket"]["title"] == "Test Ticket"
        assert result["ticket"]["status"] == "open"

    async def test_update_ticket(self):
        """Test updating a ticket."""
        agent = TicketAgent()
        
        # Create a ticket first
        create_result = await agent.execute_tool(
            "create_ticket",
            {
                "title": "Test Ticket",
                "description": "Test description",
                "category": "bug",
                "priority": "high",
            },
        )
        
        ticket_id = create_result["ticket_id"]
        
        # Update the ticket
        update_result = await agent.execute_tool(
            "update_ticket",
            {
                "ticket_id": ticket_id,
                "status": "in_progress",
                "note": "Working on it",
            },
        )
        
        assert update_result["success"] is True
        assert update_result["ticket"]["status"] == "in_progress"
        assert len(update_result["ticket"]["notes"]) == 1

    async def test_list_tickets(self):
        """Test listing all tickets."""
        agent = TicketAgent()
        
        # Create some tickets
        for i in range(3):
            await agent.execute_tool(
                "create_ticket",
                {
                    "title": f"Test Ticket {i}",
                    "description": f"Test description {i}",
                    "category": "bug",
                    "priority": "medium",
                },
            )
        
        # List all tickets
        result = await agent.execute_tool("list_all_tickets", {})
        
        assert result["success"] is True
        assert result["count"] >= 3


@pytest.mark.asyncio
class TestMapsAgent:
    """Test maps agent operations."""

    async def test_geocode(self):
        """Test geocoding an address."""
        agent = MapsAgent()
        result = await agent.execute_tool(
            "geocode",
            {"address": "1600 Amphitheatre Parkway, Mountain View, CA"},
        )
        
        assert result["success"] is True
        assert "location" in result
        assert "latitude" in result["location"]
        assert "longitude" in result["location"]

    async def test_generate_static_map(self):
        """Test generating a static map URL."""
        agent = MapsAgent()
        result = await agent.execute_tool(
            "generate_static_map",
            {
                "center": "San Francisco, CA",
                "zoom": 12,
                "size": "800x600",
            },
        )
        
        assert result["success"] is True
        assert "url" in result
        assert "maps.googleapis.com" in result["url"]


@pytest.mark.asyncio
class TestOrchestratorAgent:
    """Test orchestrator agent operations."""

    async def test_list_available_agents(self):
        """Test listing available agents."""
        agent = OrchestratorAgent()
        result = await agent.execute_tool("list_available_agents", {})
        
        assert result["success"] is True
        assert "agents" in result
        assert len(result["agents"]) == 3

