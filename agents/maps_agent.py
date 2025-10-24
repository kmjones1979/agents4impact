"""Maps generation agent for geospatial data and visualization."""

from typing import Any, Dict, List
import json
from .base_agent import BaseAgent
from config import Config


class MapsAgent(BaseAgent):
    """Agent for generating maps and geospatial information."""

    def __init__(self):
        """Initialize the maps agent."""
        super().__init__(
            name="Maps Agent",
            description="Specialized agent for generating maps and providing geospatial information",
            instructions="""You are a maps and geospatial expert agent. Your role is to:
1. Generate map visualizations based on location data
2. Provide directions and route information
3. Geocode addresses to coordinates
4. Reverse geocode coordinates to addresses
5. Calculate distances and travel times
6. Find nearby places and points of interest
7. Create static map URLs for embedding

Always provide accurate location information and handle ambiguous locations appropriately.
Use appropriate zoom levels and map types for different use cases.""",
        )

        self.api_key = Config.MAPS_API_KEY

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get maps-specific tools."""
        return [
            {
                "name": "geocode",
                "description": "Convert an address to geographic coordinates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "The address to geocode",
                        }
                    },
                    "required": ["address"],
                },
            },
            {
                "name": "reverse_geocode",
                "description": "Convert coordinates to an address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "Latitude coordinate",
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Longitude coordinate",
                        },
                    },
                    "required": ["latitude", "longitude"],
                },
            },
            {
                "name": "get_directions",
                "description": "Get directions between two locations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Starting location (address or coordinates)",
                        },
                        "destination": {
                            "type": "string",
                            "description": "Ending location (address or coordinates)",
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["driving", "walking", "bicycling", "transit"],
                            "description": "Travel mode",
                            "default": "driving",
                        },
                    },
                    "required": ["origin", "destination"],
                },
            },
            {
                "name": "calculate_distance",
                "description": "Calculate distance and duration between locations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origins": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of origin locations",
                        },
                        "destinations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of destination locations",
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["driving", "walking", "bicycling", "transit"],
                            "description": "Travel mode",
                            "default": "driving",
                        },
                    },
                    "required": ["origins", "destinations"],
                },
            },
            {
                "name": "find_nearby_places",
                "description": "Find places near a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Center location for search",
                        },
                        "place_type": {
                            "type": "string",
                            "description": "Type of place to find (e.g., restaurant, hotel, gas_station)",
                        },
                        "radius": {
                            "type": "number",
                            "description": "Search radius in meters (default: 1000)",
                            "default": 1000,
                        },
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "generate_static_map",
                "description": "Generate a static map URL for embedding",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "center": {
                            "type": "string",
                            "description": "Center location (address or coordinates)",
                        },
                        "zoom": {
                            "type": "integer",
                            "description": "Zoom level (0-21)",
                            "default": 13,
                        },
                        "size": {
                            "type": "string",
                            "description": "Image size (e.g., '600x400')",
                            "default": "600x400",
                        },
                        "markers": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of marker locations",
                        },
                    },
                    "required": ["center"],
                },
            },
        ]

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute maps tools."""
        try:
            if tool_name == "geocode":
                return self._geocode(parameters["address"])

            elif tool_name == "reverse_geocode":
                return self._reverse_geocode(
                    parameters["latitude"], parameters["longitude"]
                )

            elif tool_name == "get_directions":
                return self._get_directions(
                    parameters["origin"],
                    parameters["destination"],
                    parameters.get("mode", "driving"),
                )

            elif tool_name == "calculate_distance":
                return self._calculate_distance(
                    parameters["origins"],
                    parameters["destinations"],
                    parameters.get("mode", "driving"),
                )

            elif tool_name == "find_nearby_places":
                return self._find_nearby_places(
                    parameters["location"],
                    parameters.get("place_type"),
                    parameters.get("radius", 1000),
                )

            elif tool_name == "generate_static_map":
                return self._generate_static_map(parameters)

            else:
                return {"error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            return {"error": str(e)}

    def _geocode(self, address: str) -> Dict[str, Any]:
        """Geocode an address to coordinates."""
        # Mock implementation - in production, use Google Maps Geocoding API
        return {
            "success": True,
            "address": address,
            "location": {
                "latitude": 37.7749,  # Example: San Francisco
                "longitude": -122.4194,
            },
            "formatted_address": f"{address} (geocoded)",
            "note": "This is a mock implementation. Configure MAPS_API_KEY for real geocoding.",
        }

    def _reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Reverse geocode coordinates to an address."""
        # Mock implementation - in production, use Google Maps Geocoding API
        return {
            "success": True,
            "location": {"latitude": latitude, "longitude": longitude},
            "formatted_address": f"Address at ({latitude}, {longitude})",
            "note": "This is a mock implementation. Configure MAPS_API_KEY for real reverse geocoding.",
        }

    def _get_directions(
        self, origin: str, destination: str, mode: str = "driving"
    ) -> Dict[str, Any]:
        """Get directions between two locations."""
        # Mock implementation - in production, use Google Maps Directions API
        return {
            "success": True,
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "routes": [
                {
                    "summary": f"Route from {origin} to {destination}",
                    "distance": {"text": "10.5 km", "value": 10500},
                    "duration": {"text": "15 mins", "value": 900},
                    "steps": [
                        {"instruction": "Head north", "distance": "500 m"},
                        {"instruction": "Turn right", "distance": "2 km"},
                        {"instruction": "Continue straight", "distance": "8 km"},
                    ],
                }
            ],
            "note": "This is a mock implementation. Configure MAPS_API_KEY for real directions.",
        }

    def _calculate_distance(
        self, origins: List[str], destinations: List[str], mode: str = "driving"
    ) -> Dict[str, Any]:
        """Calculate distance matrix between locations."""
        # Mock implementation - in production, use Google Maps Distance Matrix API
        return {
            "success": True,
            "origins": origins,
            "destinations": destinations,
            "mode": mode,
            "matrix": [
                [
                    {
                        "origin": origin,
                        "destination": dest,
                        "distance": {"text": "5.2 km", "value": 5200},
                        "duration": {"text": "8 mins", "value": 480},
                    }
                    for dest in destinations
                ]
                for origin in origins
            ],
            "note": "This is a mock implementation. Configure MAPS_API_KEY for real distance calculations.",
        }

    def _find_nearby_places(
        self, location: str, place_type: str = None, radius: int = 1000
    ) -> Dict[str, Any]:
        """Find nearby places."""
        # Mock implementation - in production, use Google Maps Places API
        return {
            "success": True,
            "location": location,
            "place_type": place_type,
            "radius": radius,
            "places": [
                {
                    "name": "Example Place 1",
                    "address": "123 Main St",
                    "rating": 4.5,
                    "distance": 250,
                },
                {
                    "name": "Example Place 2",
                    "address": "456 Oak Ave",
                    "rating": 4.2,
                    "distance": 500,
                },
            ],
            "note": "This is a mock implementation. Configure MAPS_API_KEY for real nearby search.",
        }

    def _generate_static_map(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a static map URL."""
        center = params["center"]
        zoom = params.get("zoom", 13)
        size = params.get("size", "600x400")
        markers = params.get("markers", [])

        # Build Google Static Maps API URL
        base_url = "https://maps.googleapis.com/maps/api/staticmap"
        markers_param = "|".join(markers) if markers else ""

        url = f"{base_url}?center={center}&zoom={zoom}&size={size}"

        if markers_param:
            url += f"&markers={markers_param}"

        if self.api_key:
            url += f"&key={self.api_key}"

        return {
            "success": True,
            "url": url,
            "center": center,
            "zoom": zoom,
            "size": size,
            "markers": markers,
        }


