"""Ticket sales agent for events and venues with HTTP 402 payment support."""

from typing import Any, Dict, List
import os
import requests
from .base_agent import BaseAgent


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
        print(f"Ticket Agent connected to MCP server at: {self.mcp_server_url}")

    def _call_mcp(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call the MCP server."""
        try:
            response = requests.post(
                f"{self.mcp_server_url}/mcp/tool/{tool_name}",
                json=parameters,
                timeout=10
            )
            
            # Handle HTTP 402 Payment Required
            if response.status_code == 402:
                return response.json()
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"Cannot connect to MCP server at {self.mcp_server_url}. Make sure it's running."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get ticket sales tools."""
        return [
            {
                "name": "list_events",
                "description": "List available events and shows in the city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["concert", "sports", "theater", "festival", "conference", "other"],
                            "description": "Filter by event category"
                        },
                        "city": {
                            "type": "string",
                            "description": "Filter by city name"
                        }
                    }
                }
            },
            {
                "name": "get_event_details",
                "description": "Get detailed information about a specific event",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "event_id": {
                            "type": "string",
                            "description": "The event ID"
                        }
                    },
                    "required": ["event_id"]
                }
            },
            {
                "name": "list_venues",
                "description": "List all venues in the city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Filter by city name"
                        }
                    }
                }
            },
            {
                "name": "purchase_tickets",
                "description": "Purchase tickets for an event (requires payment via HTTP 402)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "event_id": {
                            "type": "string",
                            "description": "The event ID"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Number of tickets (1-10)",
                            "minimum": 1,
                            "maximum": 10
                        },
                        "customer_email": {
                            "type": "string",
                            "description": "Customer email address"
                        },
                        "customer_name": {
                            "type": "string",
                            "description": "Customer name"
                        }
                    },
                    "required": ["event_id", "quantity", "customer_email", "customer_name"]
                }
            },
            {
                "name": "check_payment_status",
                "description": "Check the status of a payment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_intent_id": {
                            "type": "string",
                            "description": "The payment intent ID"
                        }
                    },
                    "required": ["payment_intent_id"]
                }
            },
            {
                "name": "get_my_tickets",
                "description": "Get purchased tickets",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending_payment", "paid", "cancelled", "used"],
                            "description": "Filter by ticket status"
                        }
                    }
                }
            }
        ]

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute ticket sales tools."""
        try:
            if tool_name == "list_events":
                return self._call_mcp("list_events", parameters)
            
            elif tool_name == "get_event_details":
                return self._call_mcp("get_event", {"eventId": parameters.get("event_id")})
            
            elif tool_name == "list_venues":
                return self._call_mcp("list_venues", parameters)
            
            elif tool_name == "purchase_tickets":
                # This will trigger HTTP 402 payment flow
                result = self._call_mcp("purchase_tickets", {
                    "eventId": parameters.get("event_id"),
                    "quantity": parameters.get("quantity"),
                    "customerEmail": parameters.get("customer_email"),
                    "customerName": parameters.get("customer_name")
                })
                
                # Enhance response with payment instructions
                if result.get("requiresPayment"):
                    result["message"] = f"""
🎫 Ticket Reserved! Payment Required

Your tickets have been reserved. To complete your purchase:

💳 Payment Amount: ${result.get('paymentIntent', {}).get('amount', 0):.2f}
🪙 Pay with Crypto: {result.get('paymentUrl', 'N/A')}

Click the payment link to complete your purchase with Coinbase Commerce.
Your tickets will be confirmed once payment is received.

Payment Intent ID: {result.get('paymentIntent', {}).get('id', 'N/A')}
Expires: {result.get('paymentIntent', {}).get('expiresAt', 'N/A')}
"""
                return result
            
            elif tool_name == "check_payment_status":
                return self._call_mcp("check_payment_status", {
                    "paymentIntentId": parameters.get("payment_intent_id")
                })
            
            elif tool_name == "get_my_tickets":
                return self._call_mcp("get_my_tickets", parameters)
            
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

