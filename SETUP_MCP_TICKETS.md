# MCP Ticket Server Setup Guide

## 🎫 Overview

The Ticket Agent now sells tickets to events and venues using:

-   **FastMCP Server** (TypeScript) - Handles inventory and payments
-   **HTTP 402** - Payment Required flow
-   **Coinbase Commerce** - Cryptocurrency payments
-   **ADK Agent** (Python) - User-facing interface

## 🚀 Quick Start

### 1. Install MCP Server Dependencies

```bash
cd mcp-ticket-server
npm install
```

### 2. Start the MCP Server

```bash
cd mcp-ticket-server
npm run dev
```

The MCP server will start on port 3000.

### 3. Verify Connection

```bash
curl http://localhost:3000/health
```

Should return: `{"status":"healthy"}`

### 4. Restart Ticket Agent

```bash
cd ..
pkill -f "a2a_server.*ticket"
source venv/bin/activate
python a2a_server.py --agent ticket > logs/ticket_agent.log 2>&1 &
```

## 📋 Available Events

The system comes with sample events:

1. **Summer Music Festival 2025** - Hollywood Bowl - $150
2. **Tech Conference 2025** - Madison Square Garden - $299
3. **Rock Legends Concert** - The Fillmore - $75
4. **Broadway Musical Night** - Madison Square Garden - $120

## 💳 HTTP 402 Payment Flow

### How It Works

1. **List Events**

    ```bash
    curl -X POST http://localhost:8002/execute-tool \
      -H "Content-Type: application/json" \
      -d '{"tool_name": "list_events", "parameters": {}}'
    ```

2. **Purchase Tickets** (Triggers HTTP 402)

    ```bash
    curl -X POST http://localhost:8002/execute-tool \
      -H "Content-Type: application/json" \
      -d '{
        "tool_name": "purchase_tickets",
        "parameters": {
          "event_id": "event-1",
          "quantity": 2,
          "customer_email": "user@example.com",
          "customer_name": "John Doe"
        }
      }'
    ```

3. **Response Includes Payment URL**

    ```json
    {
      "success": false,
      "requiresPayment": true,
      "paymentUrl": "https://commerce.coinbase.com/charges/...",
      "ticket": {...},
      "paymentIntent": {
        "id": "...",
        "amount": 300.00,
        "status": "pending"
      }
    }
    ```

4. **User Pays at Payment URL**

    - Redirected to Coinbase Commerce
    - Pays with cryptocurrency
    - Coinbase sends webhook to confirm

5. **Check Payment Status**
    ```bash
    curl -X POST http://localhost:8002/execute-tool \
      -H "Content-Type: application/json" \
      -d '{
        "tool_name": "check_payment_status",
        "parameters": {
          "payment_intent_id": "your-payment-intent-id"
        }
      }'
    ```

## 🧪 Testing Without Real Payments

To test the flow without real Coinbase payments, simulate payment confirmation:

```bash
curl -X POST http://localhost:3000/mcp/tool/confirm_payment \
  -H "Content-Type: application/json" \
  -d '{
    "paymentIntentId": "your-payment-intent-id",
    "coinbaseChargeId": "your-charge-id"
  }'
```

This updates the ticket status to `paid` and generates a QR code.

## 🌐 Web Interface Updates

The web interface has been updated to support ticket sales:

-   Browse events by category
-   View event details with pricing
-   Purchase tickets (redirects to payment)
-   View purchased tickets with QR codes

Access at: http://localhost:8080

## 🔧 Configuration

### Environment Variables

In `.env`:

```bash
MCP_TICKET_SERVER_URL=http://localhost:3000
```

### Coinbase Commerce (Optional)

For real cryptocurrency payments:

1. Sign up at https://commerce.coinbase.com
2. Get your API key
3. Add to `mcp-ticket-server/.env`:
    ```
    COINBASE_COMMERCE_API_KEY=your-key-here
    ```

## 📊 Architecture

```
┌─────────────────┐
│   Web Browser   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Ticket Agent   │◄─────┤  MCP Server      │
│  (Python/ADK)   │      │  (TypeScript)    │
│  Port: 8002     │      │  Port: 3000      │
└─────────────────┘      └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Coinbase Commerce│
                         │  (Payments)      │
                         └──────────────────┘
```

## 🎯 Key Features

✅ FastMCP-based ticket inventory
✅ HTTP 402 Payment Required responses  
✅ Coinbase Commerce integration
✅ Event and venue management
✅ Real-time ticket availability
✅ QR code generation
✅ Payment status tracking
✅ Cryptocurrency payments

## 🐛 Troubleshooting

### MCP Server Won't Start

```bash
cd mcp-ticket-server
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Ticket Agent Can't Connect

1. Check MCP server is running: `curl http://localhost:3000/health`
2. Check .env has correct URL
3. Restart ticket agent

### Payment Not Confirming

-   Use the test endpoint to simulate payment confirmation
-   Check payment intent ID matches
-   Verify charge ID is correct

## 📚 MCP Tools

The MCP server exposes these tools:

-   `list_events` - Browse available events
-   `get_event` - Get event details
-   `list_venues` - Browse venues
-   `purchase_tickets` - Buy tickets (returns 402)
-   `check_payment_status` - Check payment
-   `confirm_payment` - Confirm payment (webhook)
-   `get_my_tickets` - View purchased tickets

## 🔐 Production Considerations

Before going to production:

1. **Real Coinbase Account**

    - Set up real Coinbase Commerce account
    - Configure webhooks properly
    - Implement webhook signature verification

2. **Security**

    - Use HTTPS for all communication
    - Implement authentication
    - Secure webhook endpoints
    - Rate limiting

3. **Database**

    - Replace in-memory storage with PostgreSQL
    - Implement proper inventory management
    - Transaction handling

4. **Monitoring**
    - Set up logging
    - Payment tracking
    - Error alerting

---

Ready to sell tickets! 🎉

