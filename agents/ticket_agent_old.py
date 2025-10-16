"""Ticket sales agent for events and venues with HTTP 402 payment support."""

from typing import Any, Dict, List
import os
import requests
from .base_agent import BaseAgent
from config import Config


class TicketAgent(BaseAgent):
    """Agent for selling tickets to events and venues with payment processing."""

    def __init__(self):
        """Initialize the ticket agent."""
        super().__init__(
            name="Ticket Agent",
            description="Specialized agent for selling tickets to events and venues in the city",
            instructions="""You are a ticket sales expert agent. Your role is to:
1. Help customers find and browse events and venues
2. Provide detailed information about events, dates, and pricing
3. Process ticket purchases with secure payment handling
4. Support HTTP 402 payment flow with Coinbase Commerce
5. Track payment status and confirm ticket purchases
6. Provide tickets with QR codes after successful payment

You work with a FastMCP server that handles the actual ticket inventory and payments.
Always provide clear pricing information and guide users through the payment process.
Support cryptocurrency payments through Coinbase Commerce.""",
        )

        # MCP Server configuration
        self.mcp_server_url = os.getenv("MCP_TICKET_SERVER_URL", "http://localhost:3000")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get ticket management tools."""
        return [
            {
                "name": "create_ticket",
                "description": "Create a new support ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Ticket title/summary",
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed ticket description",
                        },
                        "category": {
                            "type": "string",
                            "enum": ["bug", "feature_request", "question", "incident"],
                            "description": "Ticket category",
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Ticket priority",
                        },
                        "assignee": {
                            "type": "string",
                            "description": "Person or team to assign the ticket to",
                        },
                    },
                    "required": ["title", "description", "category", "priority"],
                },
            },
            {
                "name": "update_ticket",
                "description": "Update an existing ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ticket ID",
                        },
                        "status": {
                            "type": "string",
                            "enum": ["open", "in_progress", "waiting", "resolved", "closed"],
                            "description": "New ticket status",
                        },
                        "note": {
                            "type": "string",
                            "description": "Update note or comment",
                        },
                    },
                    "required": ["ticket_id"],
                },
            },
            {
                "name": "get_ticket",
                "description": "Retrieve ticket information by ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "The ticket ID",
                        }
                    },
                    "required": ["ticket_id"],
                },
            },
            {
                "name": "search_tickets",
                "description": "Search tickets by various criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by status",
                        },
                        "category": {
                            "type": "string",
                            "description": "Filter by category",
                        },
                        "priority": {
                            "type": "string",
                            "description": "Filter by priority",
                        },
                        "assignee": {
                            "type": "string",
                            "description": "Filter by assignee",
                        },
                    },
                },
            },
            {
                "name": "list_all_tickets",
                "description": "List all tickets in the system",
                "parameters": {"type": "object", "properties": {}},
            },
        ]

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute ticket management tools."""
        try:
            if tool_name == "create_ticket":
                return self._create_ticket(parameters)

            elif tool_name == "update_ticket":
                return self._update_ticket(parameters)

            elif tool_name == "get_ticket":
                return self._get_ticket(parameters["ticket_id"])

            elif tool_name == "search_tickets":
                return self._search_tickets(parameters)

            elif tool_name == "list_all_tickets":
                return self._list_all_tickets()

            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

    def _create_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new ticket."""
        ticket_id = f"TICKET-{str(uuid.uuid4())[:8].upper()}"
        timestamp = datetime.now().isoformat()

        ticket = {
            "ticket_id": ticket_id,
            "title": params["title"],
            "description": params["description"],
            "category": params["category"],
            "priority": params["priority"],
            "assignee": params.get("assignee", "unassigned"),
            "status": "open",
            "created_at": timestamp,
            "updated_at": timestamp,
            "notes": [],
        }

        self.tickets[ticket_id] = ticket

        return {
            "success": True,
            "ticket_id": ticket_id,
            "message": f"Ticket {ticket_id} created successfully",
            "ticket": ticket,
        }

    def _update_ticket(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing ticket."""
        ticket_id = params["ticket_id"]

        if ticket_id not in self.tickets:
            return {"success": False, "error": f"Ticket {ticket_id} not found"}

        ticket = self.tickets[ticket_id]

        if "status" in params:
            ticket["status"] = params["status"]

        if "note" in params:
            ticket["notes"].append(
                {"timestamp": datetime.now().isoformat(), "note": params["note"]}
            )

        ticket["updated_at"] = datetime.now().isoformat()

        return {
            "success": True,
            "ticket_id": ticket_id,
            "message": f"Ticket {ticket_id} updated successfully",
            "ticket": ticket,
        }

    def _get_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """Get a specific ticket."""
        if ticket_id not in self.tickets:
            return {"success": False, "error": f"Ticket {ticket_id} not found"}

        return {"success": True, "ticket": self.tickets[ticket_id]}

    def _search_tickets(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Search tickets based on filters."""
        results = []

        for ticket in self.tickets.values():
            match = True

            for key, value in filters.items():
                if key in ticket and ticket[key] != value:
                    match = False
                    break

            if match:
                results.append(ticket)

        return {"success": True, "count": len(results), "tickets": results}

    def _list_all_tickets(self) -> Dict[str, Any]:
        """List all tickets."""
        return {
            "success": True,
            "count": len(self.tickets),
            "tickets": list(self.tickets.values()),
        }

