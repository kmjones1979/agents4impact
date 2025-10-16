/**
 * MCP Ticket Sales Server with HTTP 402 Payment Support
 * Integrates with Coinbase Commerce for cryptocurrency payments
 */

import express from "express";
import cors from "cors";
import { v4 as uuidv4 } from "uuid";
import { events, venues, tickets, paymentIntents } from "./data.js";
import {
    Event,
    Venue,
    Ticket,
    PaymentIntent,
    TicketPurchaseRequest,
    PaymentResponse,
} from "./types.js";

// Initialize Express server
const app = express();
app.use(cors());
app.use(express.json());

/**
 * Tool: List all available events
 */
mcp.tool({
    name: "list_events",
    description: "List all available events with ticket information",
    parameters: z.object({
        category: z
            .enum([
                "concert",
                "sports",
                "theater",
                "festival",
                "conference",
                "other",
            ])
            .optional(),
        city: z.string().optional(),
    }),
    execute: async (args) => {
        let filteredEvents = Array.from(events.values());

        if (args.category) {
            filteredEvents = filteredEvents.filter(
                (e) => e.category === args.category
            );
        }

        if (args.city) {
            filteredEvents = filteredEvents.filter((e) => {
                const venue = venues.get(e.venueId);
                return venue?.city
                    .toLowerCase()
                    .includes(args.city.toLowerCase());
            });
        }

        return {
            success: true,
            count: filteredEvents.length,
            events: filteredEvents,
        };
    },
});

/**
 * Tool: Get event details
 */
mcp.tool({
    name: "get_event",
    description: "Get detailed information about a specific event",
    parameters: z.object({
        eventId: z.string(),
    }),
    execute: async (args) => {
        const event = events.get(args.eventId);

        if (!event) {
            return { success: false, error: "Event not found" };
        }

        const venue = venues.get(event.venueId);

        return {
            success: true,
            event,
            venue,
        };
    },
});

/**
 * Tool: List all venues
 */
mcp.tool({
    name: "list_venues",
    description: "List all available venues",
    parameters: z.object({
        city: z.string().optional(),
    }),
    execute: async (args) => {
        let filteredVenues = Array.from(venues.values());

        if (args.city) {
            filteredVenues = filteredVenues.filter((v) =>
                v.city.toLowerCase().includes(args.city.toLowerCase())
            );
        }

        return {
            success: true,
            count: filteredVenues.length,
            venues: filteredVenues,
        };
    },
});

/**
 * Tool: Purchase tickets (with HTTP 402 payment flow)
 */
mcp.tool({
    name: "purchase_tickets",
    description:
        "Purchase tickets for an event. Returns HTTP 402 if payment is required.",
    parameters: z.object({
        eventId: z.string(),
        quantity: z.number().min(1).max(10),
        customerEmail: z.string().email(),
        customerName: z.string(),
    }),
    execute: async (args): Promise<PaymentResponse> => {
        const event = events.get(args.eventId);

        if (!event) {
            return {
                success: false,
                requiresPayment: false,
                error: "Event not found",
            };
        }

        if (event.availableTickets < args.quantity) {
            return {
                success: false,
                requiresPayment: false,
                error: `Only ${event.availableTickets} tickets available`,
            };
        }

        const totalAmount = event.priceUSD * args.quantity;

        // Create ticket
        const ticketId = uuidv4();
        const ticket: Ticket = {
            id: ticketId,
            eventId: event.id,
            eventName: event.name,
            venue: event.venue,
            purchaseDate: new Date().toISOString(),
            eventDate: event.date,
            status: "pending_payment",
            priceUSD: totalAmount,
        };

        tickets.set(ticketId, ticket);

        // Create payment intent
        const paymentIntentId = uuidv4();
        const paymentIntent: PaymentIntent = {
            id: paymentIntentId,
            ticketId: ticketId,
            amount: totalAmount,
            currency: "USD",
            status: "pending",
            createdAt: new Date().toISOString(),
            expiresAt: new Date(Date.now() + 30 * 60 * 1000).toISOString(), // 30 minutes
        };

        // Simulate Coinbase Commerce integration
        const coinbaseChargeId = `charge_${uuidv4()}`;
        const paymentUrl = `https://commerce.coinbase.com/charges/${coinbaseChargeId}`;

        paymentIntent.coinbaseChargeId = coinbaseChargeId;
        paymentIntent.paymentUrl = paymentUrl;

        paymentIntents.set(paymentIntentId, paymentIntent);

        // Return HTTP 402 Payment Required response
        return {
            success: false,
            requiresPayment: true,
            paymentUrl: paymentUrl,
            ticket: ticket,
            paymentIntent: paymentIntent,
        };
    },
});

/**
 * Tool: Check payment status
 */
mcp.tool({
    name: "check_payment_status",
    description: "Check the status of a payment",
    parameters: z.object({
        paymentIntentId: z.string(),
    }),
    execute: async (args) => {
        const paymentIntent = paymentIntents.get(args.paymentIntentId);

        if (!paymentIntent) {
            return { success: false, error: "Payment intent not found" };
        }

        const ticket = tickets.get(paymentIntent.ticketId);

        return {
            success: true,
            paymentIntent,
            ticket,
        };
    },
});

/**
 * Tool: Confirm payment (webhook simulation)
 */
mcp.tool({
    name: "confirm_payment",
    description: "Confirm a payment (simulates Coinbase webhook)",
    parameters: z.object({
        paymentIntentId: z.string(),
        coinbaseChargeId: z.string(),
    }),
    execute: async (args) => {
        const paymentIntent = paymentIntents.get(args.paymentIntentId);

        if (!paymentIntent) {
            return { success: false, error: "Payment intent not found" };
        }

        if (paymentIntent.coinbaseChargeId !== args.coinbaseChargeId) {
            return { success: false, error: "Invalid charge ID" };
        }

        // Update payment status
        paymentIntent.status = "completed";
        paymentIntents.set(args.paymentIntentId, paymentIntent);

        // Update ticket status
        const ticket = tickets.get(paymentIntent.ticketId);
        if (ticket) {
            ticket.status = "paid";
            ticket.paymentId = paymentIntent.id;
            ticket.qrCode = `QR-${uuidv4()}`;
            tickets.set(ticket.id, ticket);

            // Update available tickets
            const event = events.get(ticket.eventId);
            if (event) {
                event.availableTickets -= 1;
                events.set(event.id, event);
            }
        }

        return {
            success: true,
            message: "Payment confirmed",
            ticket,
            paymentIntent,
        };
    },
});

/**
 * Tool: Get my tickets
 */
mcp.tool({
    name: "get_my_tickets",
    description: "Get all tickets (useful for testing)",
    parameters: z.object({
        status: z
            .enum(["pending_payment", "paid", "cancelled", "used"])
            .optional(),
    }),
    execute: async (args) => {
        let filteredTickets = Array.from(tickets.values());

        if (args.status) {
            filteredTickets = filteredTickets.filter(
                (t) => t.status === args.status
            );
        }

        return {
            success: true,
            count: filteredTickets.length,
            tickets: filteredTickets,
        };
    },
});

/**
 * Resource: Event listings
 */
mcp.resource({
    uri: "ticket://events",
    name: "All Events",
    description: "Complete list of all available events",
    mimeType: "application/json",
    text: async () => {
        return JSON.stringify(Array.from(events.values()), null, 2);
    },
});

/**
 * Resource: Venue listings
 */
mcp.resource({
    uri: "ticket://venues",
    name: "All Venues",
    description: "Complete list of all venues",
    mimeType: "application/json",
    text: async () => {
        return JSON.stringify(Array.from(venues.values()), null, 2);
    },
});

// Start the MCP server
const PORT = process.env.PORT || 3000;

console.log(`🎫 MCP Ticket Sales Server starting...`);
console.log(`📍 Port: ${PORT}`);
console.log(`💳 HTTP 402 Payment Support: Enabled`);
console.log(`🪙 Coinbase Commerce Integration: Ready`);
console.log(`✅ FastMCP Server Ready!`);

// Export for use
export { mcp };

// Start server if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
    mcp.listen(PORT as number);
}
