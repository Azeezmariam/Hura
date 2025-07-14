import logging
import requests
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

from config import settings

logger = logging.getLogger(__name__)

class MapsService:
    def __init__(self):
        self.api_key = settings.google_maps_api_key
        self.default_location = settings.default_location
        
    def is_maps_query(self, text: str) -> bool:
        """Detect if a query is related to maps/location"""
        maps_keywords = [
            "where is", "location", "address", "directions", "how to get",
            "how do i get", "route", "map", "nearby", "close to",
            "kimironko", "nyarutarama", "kacyiru", "remera", "kicukiro",
            "airport", "hotel", "restaurant", "museum", "market", "bank",
            "atm", "pharmacy", "hospital", "school", "university"
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in maps_keywords)
    
    def extract_location_from_query(self, text: str) -> Optional[str]:
        """Extract location name from user query"""
        # Common patterns for location queries
        patterns = [
            r"where is (.+?)(?:\?|$)",
            r"location of (.+?)(?:\?|$)",
            r"address of (.+?)(?:\?|$)",
            r"how to get to (.+?)(?:\?|$)",
            r"directions to (.+?)(?:\?|$)",
            r"route to (.+?)(?:\?|$)",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                location = match.group(1).strip()
                # Add "Kigali" if not specified
                if "kigali" not in location.lower():
                    location = f"{location}, Kigali"
                return location
        
        return None
    
    def search_place(self, query: str) -> Optional[Dict]:
        """Search for a place using Google Places API"""
        if not self.api_key:
            logger.warning("Google Maps API key not configured")
            return None
        
        try:
            # Add Kigali context if not present
            if "kigali" not in query.lower():
                query = f"{query}, Kigali"
            
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                "query": query,
                "key": self.api_key,
                "region": "rw"  # Rwanda
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                place = data["results"][0]
                return {
                    "name": place.get("name", ""),
                    "address": place.get("formatted_address", ""),
                    "location": place.get("geometry", {}).get("location", {}),
                    "rating": place.get("rating"),
                    "types": place.get("types", []),
                    "place_id": place.get("place_id", "")
                }
            else:
                logger.warning(f"Place search failed: {data.get('status')}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching place: {e}")
            return None
    
    def get_directions(self, origin: str, destination: str) -> Optional[Dict]:
        """Get directions between two locations"""
        if not self.api_key:
            logger.warning("Google Maps API key not configured")
            return None
        
        try:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {
                "origin": origin,
                "destination": destination,
                "key": self.api_key,
                "region": "rw"  # Rwanda
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("routes"):
                route = data["routes"][0]
                leg = route["legs"][0]
                
                return {
                    "distance": leg.get("distance", {}).get("text", ""),
                    "duration": leg.get("duration", {}).get("text", ""),
                    "steps": [
                        {
                            "instruction": step.get("html_instructions", ""),
                            "distance": step.get("distance", {}).get("text", ""),
                            "duration": step.get("duration", {}).get("text", "")
                        }
                        for step in leg.get("steps", [])
                    ],
                    "start_address": leg.get("start_address", ""),
                    "end_address": leg.get("end_address", "")
                }
            else:
                logger.warning(f"Directions failed: {data.get('status')}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting directions: {e}")
            return None
    
    def get_nearby_places(self, location: str, place_type: str = "restaurant", radius: int = 5000) -> Optional[List[Dict]]:
        """Get nearby places of a specific type"""
        if not self.api_key:
            logger.warning("Google Maps API key not configured")
            return None
        
        try:
            # First get coordinates for the location
            place_info = self.search_place(location)
            if not place_info or not place_info.get("location"):
                return None
            
            lat = place_info["location"]["lat"]
            lng = place_info["location"]["lng"]
            
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": f"{lat},{lng}",
                "radius": radius,
                "type": place_type,
                "key": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return [
                    {
                        "name": place.get("name", ""),
                        "address": place.get("vicinity", ""),
                        "rating": place.get("rating"),
                        "types": place.get("types", [])
                    }
                    for place in data.get("results", [])[:5]  # Limit to 5 results
                ]
            else:
                logger.warning(f"Nearby search failed: {data.get('status')}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting nearby places: {e}")
            return None
    
    def process_maps_query(self, query: str) -> str:
        """Process a maps-related query and return a response"""
        if not self.api_key:
            return "I'm sorry, but I don't have access to maps and location services at the moment. Please check with your hotel or local information center for directions."
        
        # Extract location from query
        location = self.extract_location_from_query(query)
        if not location:
            return "I'm not sure what location you're asking about. Could you please be more specific? For example: 'Where is Kimironko?' or 'How do I get to the airport?'"
        
        # Check if it's a directions query
        if any(word in query.lower() for word in ["how to get", "directions", "route"]):
            # For directions, we need origin and destination
            # For now, assume origin is "Kigali" and extract destination
            destination = location
            directions = self.get_directions("Kigali, Rwanda", destination)
            
            if directions:
                return f"To get to {destination} from Kigali:\n" \
                       f"• Distance: {directions['distance']}\n" \
                       f"• Duration: {directions['duration']}\n" \
                       f"• Start: {directions['start_address']}\n" \
                       f"• End: {directions['end_address']}"
            else:
                return f"I couldn't find directions to {destination}. Please check the location name and try again."
        
        else:
            # It's a location search
            place_info = self.search_place(location)
            
            if place_info:
                response = f"📍 **{place_info['name']}**\n"
                response += f"📍 Address: {place_info['address']}\n"
                
                if place_info.get("rating"):
                    response += f"⭐ Rating: {place_info['rating']}/5\n"
                
                # Get nearby places if it's a restaurant or hotel
                if any(word in query.lower() for word in ["restaurant", "food", "eat", "hotel", "accommodation"]):
                    nearby = self.get_nearby_places(location, "restaurant" if "restaurant" in query.lower() else "lodging")
                    if nearby:
                        response += "\n🍽️ **Nearby places:**\n"
                        for place in nearby[:3]:
                            response += f"• {place['name']} ({place['address']})\n"
                
                return response
            else:
                return f"I couldn't find information about {location}. Please check the spelling or try a different location name."
    
    def initialize(self):
        """Initialize the maps service"""
        if not self.api_key:
            logger.warning("Google Maps API key not configured - maps features will be disabled")
        else:
            logger.info("Google Maps service initialized successfully") 