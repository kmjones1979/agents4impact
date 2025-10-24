/**
 * Type definitions for the MCP Ticket Sales Server
 */

export interface Event {
    id: string;
    name: string;
    description: string;
    venue: string;
    venueId: string;
    date: string;
    time: string;
    category:
        | "concert"
        | "sports"
        | "theater"
        | "festival"
        | "conference"
        | "other";
    priceUSD: number;
    availableTickets: number;
    totalTickets: number;
    imageUrl?: string;
    tags: string[];
}

export interface Venue {
    id: string;
    name: string;
    address: string;
    city: string;
    state: string;
    zipCode: string;
    capacity: number;
    type: "stadium" | "arena" | "theater" | "club" | "outdoor" | "other";
    amenities: string[];
}

export interface Ticket {
    id: string;
    eventId: string;
    eventName: string;
    venue: string;
    purchaseDate: string;
    eventDate: string;
    status: "pending_payment" | "paid" | "cancelled" | "used";
    priceUSD: number;
    paymentId?: string;
    qrCode?: string;
    seatNumber?: string;
}

export interface PaymentIntent {
    id: string;
    ticketId: string;
    amount: number;
    currency: string;
    status: "pending" | "completed" | "failed" | "expired";
    coinbaseChargeId?: string;
    paymentUrl?: string;
    createdAt: string;
    expiresAt: string;
}

export interface TicketPurchaseRequest {
    eventId: string;
    quantity: number;
    customerEmail: string;
    customerName: string;
}

export interface PaymentResponse {
    success: boolean;
    requiresPayment: boolean;
    paymentUrl?: string;
    ticket?: Ticket;
    paymentIntent?: PaymentIntent;
    error?: string;
}

