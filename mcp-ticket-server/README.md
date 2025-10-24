# MCP Ticket Sales Server

FastMCP-based ticket sales server for events and venues with HTTP 402 payment support and Coinbase Commerce integration.

## Features

-   🎫 **Event & Venue Management** - Browse and search events and venues
-   💳 **HTTP 402 Payment Flow** - Proper payment required responses
-   🪙 **Coinbase Commerce** - Cryptocurrency payment integration
-   🔐 **MCP Protocol** - Standard Model Context Protocol implementation
-   ⚡ **FastMCP** - Built on FastMCP framework

## Installation

```bash
cd mcp-ticket-server
npm install
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:

-   `COINBASE_COMMERCE_API_KEY` - Your Coinbase Commerce API key
-   `PORT` - Server port (default: 3000)

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
npm start
```

## Available Tools

### `list_events`

List all available events with optional filtering

**Parameters:**

-   `category` (optional): Filter by event category
-   `city` (optional): Filter by city

### `get_event`

Get detailed information about a specific event

**Parameters:**

-   `eventId`: Event ID

### `list_venues`

List all available venues

**Parameters:**

-   `city` (optional): Filter by city

### `purchase_tickets`

Purchase tickets for an event (returns HTTP 402 for payment)

**Parameters:**

-   `eventId`: Event ID
-   `quantity`: Number of tickets (1-10)
-   `customerEmail`: Customer email
-   `customerName`: Customer name

**Response:**

-   Returns `requiresPayment: true` with `paymentUrl` for Coinbase Commerce
-   Ticket is created in `pending_payment` status

### `check_payment_status`

Check the status of a payment

**Parameters:**

-   `paymentIntentId`: Payment intent ID

### `confirm_payment`

Confirm a payment (simulates Coinbase webhook)

**Parameters:**

-   `paymentIntentId`: Payment intent ID
-   `coinbaseChargeId`: Coinbase charge ID

### `get_my_tickets`

Get all tickets

**Parameters:**

-   `status` (optional): Filter by ticket status

## Resources

-   `ticket://events` - All events listing
-   `ticket://venues` - All venues listing

## HTTP 402 Payment Flow

1. Client calls `purchase_tickets`
2. Server responds with `requiresPayment: true` and `paymentUrl`
3. Client redirects user to `paymentUrl` (Coinbase Commerce)
4. User completes payment
5. Coinbase webhook calls `confirm_payment`
6. Ticket status updated to `paid`
7. Client can retrieve ticket with QR code

## Integration with ADK Agent

The Python Ticket Agent connects to this MCP server and exposes ticket sales functionality through the ADK A2A protocol.

## Example Events

-   Summer Music Festival 2025 - Hollywood Bowl - $150
-   Tech Conference 2025 - Madison Square Garden - $299
-   Rock Legends Concert - The Fillmore - $75
-   Broadway Musical Night - Madison Square Garden - $120

## License

MIT

