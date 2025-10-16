/**
 * Sample data for events and venues
 */

import { Event, Venue, Ticket, PaymentIntent } from "./types.js";

export const venues: Map<string, Venue> = new Map([
    [
        "venue-1",
        {
            id: "venue-1",
            name: "Madison Square Garden",
            address: "4 Pennsylvania Plaza",
            city: "New York",
            state: "NY",
            zipCode: "10001",
            capacity: 20789,
            type: "arena",
            amenities: ["Parking", "Food Court", "VIP Lounge", "Accessibility"],
        },
    ],
    [
        "venue-2",
        {
            id: "venue-2",
            name: "The Fillmore",
            address: "1805 Geary Blvd",
            city: "San Francisco",
            state: "CA",
            zipCode: "94115",
            capacity: 1315,
            type: "club",
            amenities: ["Bar", "Coat Check", "Merchandise"],
        },
    ],
    [
        "venue-3",
        {
            id: "venue-3",
            name: "Hollywood Bowl",
            address: "2301 N Highland Ave",
            city: "Los Angeles",
            state: "CA",
            zipCode: "90068",
            capacity: 17500,
            type: "outdoor",
            amenities: ["Picnic Area", "Wine Bar", "Accessibility", "Parking"],
        },
    ],
]);

export const events: Map<string, Event> = new Map([
    [
        "event-1",
        {
            id: "event-1",
            name: "Summer Music Festival 2025",
            description:
                "Three days of incredible live music featuring top artists",
            venue: "Hollywood Bowl",
            venueId: "venue-3",
            date: "2025-07-15",
            time: "18:00",
            category: "festival",
            priceUSD: 1.0,
            availableTickets: 5000,
            totalTickets: 10000,
            tags: ["music", "outdoor", "summer"],
        },
    ],
    [
        "event-2",
        {
            id: "event-2",
            name: "Tech Conference 2025",
            description:
                "Leading technology conference with keynotes and workshops",
            venue: "Madison Square Garden",
            venueId: "venue-1",
            date: "2025-09-20",
            time: "09:00",
            category: "conference",
            priceUSD: 1.0,
            availableTickets: 3000,
            totalTickets: 5000,
            tags: ["tech", "conference", "networking"],
        },
    ],
    [
        "event-3",
        {
            id: "event-3",
            name: "Rock Legends Concert",
            description:
                "An unforgettable night with classic rock performances",
            venue: "The Fillmore",
            venueId: "venue-2",
            date: "2025-06-10",
            time: "20:00",
            category: "concert",
            priceUSD: 1.0,
            availableTickets: 800,
            totalTickets: 1200,
            tags: ["rock", "music", "concert"],
        },
    ],
    [
        "event-4",
        {
            id: "event-4",
            name: "Broadway Musical Night",
            description: "Experience the magic of Broadway musicals",
            venue: "Madison Square Garden",
            venueId: "venue-1",
            date: "2025-08-05",
            time: "19:30",
            category: "theater",
            priceUSD: 1.0,
            availableTickets: 2000,
            totalTickets: 3000,
            tags: ["theater", "musical", "broadway"],
        },
    ],
]);

export const tickets: Map<string, Ticket> = new Map();
export const paymentIntents: Map<string, PaymentIntent> = new Map();
