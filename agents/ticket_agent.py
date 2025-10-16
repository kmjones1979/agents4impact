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
            instructions="""You are a ticket sales expert agent with integrated USDC payment capabilities. Your role is to:
1. Help customers find and browse events and venues
2. Provide detailed information about events, dates, and pricing
3. Process ticket purchases with USDC blockchain payments on Base Sepolia
4. AUTOMATICALLY complete payments when asked to "pay", "complete payment", or "send payment"
5. Track payment status and confirm ticket purchases
6. Check your wallet balance when needed

IMPORTANT PAYMENT FLOW:
- When user says "buy ticket and pay" or "purchase and complete payment", you should:
  1. First call purchase_tickets to reserve the ticket
  2. Extract the payment address and amount from the response
  3. IMMEDIATELY call send_payment with those details
  4. Return the transaction confirmation

- When user says "send payment" without details, check if they just purchased a ticket and use those payment details

You have a USDC wallet on Base Sepolia that can send payments automatically.
Always provide clear pricing and guide users through the complete purchase flow.""",
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
                "description": "Use this tool ONLY when user wants to BROWSE or SEE what events are available. Do NOT use this if they want to BUY/PURCHASE tickets (use purchase_tickets instead).",
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
                "description": "Use this tool when user wants to BUY, PURCHASE, or GET tickets for an event. Accepts event name (e.g. 'Broadway Musical Night', 'Tech Conference 2025') or event ID (e.g. 'event-1'). Returns USDC payment instructions on Base Sepolia blockchain.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "event_id": {
                            "type": "string",
                            "description": "The event ID or event name (e.g., 'event-2' or 'Tech Conference 2025')"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Number of tickets (1-10)",
                            "minimum": 1,
                            "maximum": 10,
                            "default": 1
                        },
                        "customer_email": {
                            "type": "string",
                            "description": "Customer email address",
                            "default": "customer@example.com"
                        },
                        "customer_name": {
                            "type": "string",
                            "description": "Customer name",
                            "default": "Customer"
                        }
                    },
                    "required": ["event_id"]
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
            },
            {
                "name": "send_payment",
                "description": "Use this to COMPLETE PAYMENT for a ticket purchase. Send USDC to the payment address from a purchase_tickets response. Can also send USDC to any address on Base Sepolia.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to_address": {
                            "type": "string",
                            "description": "Payment address from ticket purchase (e.g., '0x8af5...')"
                        },
                        "amount_usd": {
                            "type": "string",
                            "description": "Amount in USD from ticket purchase (e.g., '1.00')"
                        },
                        "memo": {
                            "type": "string",
                            "description": "Optional memo/note for the payment"
                        }
                    },
                    "required": ["to_address", "amount_usd"]
                }
            },
            {
                "name": "get_wallet_balance",
                "description": "Check the agent's wallet balance on Base Sepolia",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]

    def _find_event_by_name(self, event_name: str) -> str:
        """Find event ID by event name with fuzzy matching."""
        # Get all events first
        result = self._call_mcp("list_events", {})
        if result.get("success") and result.get("events"):
            event_name_lower = event_name.lower().strip()
            events = result["events"]
            
            # Try exact substring match first
            for event in events:
                if event_name_lower in event["name"].lower():
                    return event["id"]
            
            # Try reverse substring match (input contains event name)
            for event in events:
                if event["name"].lower() in event_name_lower:
                    return event["id"]
            
            # Try fuzzy matching - find best match with similarity score
            def similarity(s1: str, s2: str) -> float:
                """Calculate similarity between two strings (0-1)."""
                s1, s2 = s1.lower(), s2.lower()
                # Count matching characters in order
                matches = sum(1 for a, b in zip(s1, s2) if a == b)
                max_len = max(len(s1), len(s2))
                return matches / max_len if max_len > 0 else 0
            
            # Find event with highest similarity (threshold 0.7)
            best_match = None
            best_score = 0.7  # Minimum 70% similarity
            
            for event in events:
                score = similarity(event_name_lower, event["name"].lower())
                if score > best_score:
                    best_score = score
                    best_match = event["id"]
            
            if best_match:
                return best_match
                
        return None

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute ticket sales tools."""
        try:
            if tool_name == "list_events":
                return self._call_mcp("list_events", parameters)
            
            elif tool_name == "get_event_details":
                event_id = parameters.get("event_id")
                # Try to find event by name if ID doesn't start with "event-"
                if event_id and not event_id.startswith("event-"):
                    found_id = self._find_event_by_name(event_id)
                    if found_id:
                        event_id = found_id
                return self._call_mcp("get_event", {"eventId": event_id})
            
            elif tool_name == "list_venues":
                return self._call_mcp("list_venues", parameters)
            
            elif tool_name == "purchase_tickets":
                # Get event_id and try to find by name if needed
                event_id = parameters.get("event_id")
                
                # If event_id doesn't look like an ID, try to find it by name
                if event_id and not event_id.startswith("event-"):
                    found_id = self._find_event_by_name(event_id)
                    if found_id:
                        event_id = found_id
                    else:
                        return {
                            "success": False,
                            "error": f"Event '{event_id}' not found. Please use one of: Summer Music Festival 2025, Tech Conference 2025, Rock Legends Concert, or Broadway Musical Night"
                        }
                
                # This will trigger blockchain payment flow
                result = self._call_mcp("purchase_tickets", {
                    "eventId": event_id,
                    "quantity": parameters.get("quantity", 1),
                    "customerEmail": parameters.get("customer_email", "customer@example.com"),
                    "customerName": parameters.get("customer_name", "Customer")
                })
                
                # Enhance response with blockchain payment instructions
                if result.get("requiresPayment"):
                    payment_intent = result.get('paymentIntent', {})
                    blockchain = payment_intent.get('blockchain', {})
                    
                    message = f"""
🎫 Ticket Reserved! USDC Payment Required

Your tickets have been reserved. To complete your purchase:

💵 Payment Amount: ${payment_intent.get('amount', 0):.2f} USDC

📬 Send USDC to this address on Base Sepolia:
{blockchain.get('paymentAddress', 'N/A')}

🌐 Network: {blockchain.get('network', 'Base Sepolia')}
🔗 Chain ID: {blockchain.get('chainId', 84532)}
💎 Currency: USDC (Stablecoin - always $1)
📄 USDC Contract: 0x036CbD53842c5426634e7929541eC2318f3dCF7e

⏰ Expires: {payment_intent.get('expiresAt', 'N/A')}
🎟️ Payment Intent ID: {payment_intent.get('id', 'N/A')}

📌 IMPORTANT:
1. Send EXACTLY ${payment_intent.get('amount', 0):.2f} USDC
2. Send to the address above on Base Sepolia network
3. Use the check_payment_status tool to verify your payment
4. Get Base Sepolia testnet USDC from: https://faucet.circle.com/

✅ Your ticket will be automatically confirmed once the USDC transaction is detected!
"""
                    # Return success=True with the formatted message for base_agent to display
                    return {
                        "success": True,
                        "result": message,
                        "paymentIntent": payment_intent
                    }
                return result
            
            elif tool_name == "check_payment_status":
                return self._call_mcp("check_payment_status", {
                    "paymentIntentId": parameters.get("payment_intent_id")
                })
            
            elif tool_name == "get_my_tickets":
                return self._call_mcp("get_my_tickets", parameters)
            
            elif tool_name == "send_payment":
                # Agent sends USDC payment
                result = self._call_mcp("send_payment", {
                    "toAddress": parameters.get("to_address"),
                    "amountUSD": parameters.get("amount_usd"),
                    "memo": parameters.get("memo", "")
                })
                
                if result.get("success"):
                    result["message"] = f"""
✅ USDC Payment Sent Successfully!

💵 Amount: ${parameters.get('amount_usd')} USDC
📬 To: {parameters.get('to_address')}
🔗 Transaction: {result.get('transactionHash')}
🌐 View on Explorer: {result.get('explorerUrl')}

Your USDC payment has been confirmed on Base Sepolia blockchain!
"""
                else:
                    result["message"] = f"❌ Payment failed: {result.get('error', 'Unknown error')}"
                
                return result
            
            elif tool_name == "get_wallet_balance":
                # Check agent's wallet balance
                try:
                    response = requests.get(f"{self.mcp_server_url}/mcp/tool/get_balance", timeout=10)
                    response.raise_for_status()
                    result = response.json()
                    
                    if result.get("success"):
                        result["message"] = f"""
💰 Agent Wallet Balance

📬 Address: {result.get('address')}
💵 USDC Balance: ${result.get('balanceUSDC', '0.00')}
⛽ ETH Balance (for gas): {result.get('balanceETH', '0.0')} ETH
🌐 Network: {result.get('network')}
🔗 Chain ID: {result.get('chainId')}
💎 USDC Contract: {result.get('usdcContract')}

This wallet can send USDC payments for ticket purchases!
"""
                    return result
                except Exception as e:
                    return {"success": False, "error": str(e)}
            
            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

