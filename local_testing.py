#!/usr/bin/env python3
"""
Local testing framework for Travel Planner Agents
Tests each agent (Orchestrator, Flights/Hotels, Activities, Itinerary) independently
"""

import json
import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TripRequest:
    destination: str
    dates: Dict[str, str]  # start_date, end_date
    budget: int
    interests: List[str]
    travelers: int = 1


class MockFlightsHotelsAgent:
    """Mock implementation of Flights & Hotels Agent"""
    
    def search_flights_hotels(self, request: TripRequest) -> Dict[str, Any]:
        # Simulate API call to Skyscanner/Booking
        return {
            "flights": [
                {
                    "option_id": "flight_001",
                    "price": 450,
                    "duration": "2h 30m",
                    "departure": "10:30",
                    "arrival": "13:00",
                    "booking_link": "https://example.com/book/flight_001"
                }
            ],
            "hotels": [
                {
                    "option_id": "hotel_001", 
                    "name": "Munich City Hotel",
                    "price": 120,
                    "check_in": request.dates["start_date"],
                    "check_out": request.dates["end_date"],
                    "rating": 4.2,
                    "booking_link": "https://example.com/book/hotel_001"
                }
            ]
        }


class MockActivitiesAgent:
    """Mock implementation of Activities Agent"""
    
    def search_activities(self, request: TripRequest) -> Dict[str, Any]:
        # Simulate API calls to TripAdvisor/Yelp
        activities = []
        
        if "history" in request.interests:
            activities.append({
                "activity_id": "act_001",
                "name": "Marienplatz Historical Tour",
                "description": "Guided tour of Munich's historic city center",
                "time_slots": ["10:00", "14:00", "16:00"],
                "price": 25,
                "location": "Marienplatz",
                "rating": 4.6
            })
            
        if "craft beer" in request.interests or "beer" in request.interests:
            activities.append({
                "activity_id": "act_002", 
                "name": "Hofbräu Beer Garden",
                "description": "Traditional Bavarian beer garden experience",
                "time_slots": ["12:00", "17:00", "19:00"],
                "price": 15,
                "location": "Hofbräu München",
                "rating": 4.4
            })
            
        return {"activities": activities}


class MockItineraryAgent:
    """Mock implementation of Itinerary Agent"""
    
    def create_itinerary(self, flights_hotels: Dict, activities: Dict, request: TripRequest) -> Dict[str, Any]:
        # Simulate intelligent itinerary planning
        start_date = datetime.strptime(request.dates["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(request.dates["end_date"], "%Y-%m-%d")
        
        days = []
        current_date = start_date
        
        while current_date <= end_date:
            day_activities = []
            
            # Add activities based on availability and preferences
            for activity in activities.get("activities", []):
                if len(day_activities) < 2:  # Max 2 activities per day
                    day_activities.append({
                        "time": activity["time_slots"][0],
                        "activity": activity["name"],
                        "location": activity["location"],
                        "price": activity["price"]
                    })
            
            days.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_name": current_date.strftime("%A"),
                "activities": day_activities,
                "accommodation": flights_hotels.get("hotels", [{}])[0].get("name", "TBD")
            })
            
            current_date += timedelta(days=1)
        
        return {
            "itinerary": {
                "destination": request.destination,
                "duration": f"{len(days)} days",
                "total_estimated_cost": self._calculate_total_cost(flights_hotels, activities, days),
                "daily_plan": days
            }
        }
    
    def _calculate_total_cost(self, flights_hotels: Dict, activities: Dict, days: List) -> int:
        flight_cost = sum(f["price"] for f in flights_hotels.get("flights", []))
        hotel_cost = sum(h["price"] for h in flights_hotels.get("hotels", [])) * len(days)
        activity_cost = sum(a["price"] for day in days for a in day["activities"])
        return flight_cost + hotel_cost + activity_cost


class TripOrchestratorAgent:
    """Main orchestrator that coordinates all sub-agents"""
    
    def __init__(self):
        self.flights_hotels_agent = MockFlightsHotelsAgent()
        self.activities_agent = MockActivitiesAgent()
        self.itinerary_agent = MockItineraryAgent()
        self.user_memory = {}  # Simulate AgentCore Memory
    
    async def plan_trip(self, request: TripRequest, user_id: str = "test_user") -> Dict[str, Any]:
        """Main trip planning orchestration"""
        
        # Store user preferences in memory
        self.user_memory[user_id] = {
            "budget": request.budget,
            "interests": request.interests,
            "last_destination": request.destination
        }
        
        print(f"🧭 Orchestrator: Planning trip to {request.destination}")
        print(f"   Budget: ${request.budget}, Interests: {', '.join(request.interests)}")
        
        # Step 1: Get flights and hotels
        print("\n✈️ Fetching flights and hotels...")
        flights_hotels = self.flights_hotels_agent.search_flights_hotels(request)
        
        # Step 2: Get activities
        print("🏰 Finding activities...")  
        activities = self.activities_agent.search_activities(request)
        
        # Step 3: Create itinerary
        print("📅 Creating itinerary...")
        itinerary = self.itinerary_agent.create_itinerary(flights_hotels, activities, request)
        
        # Combine all results
        final_plan = {
            "request": {
                "destination": request.destination,
                "dates": request.dates,
                "budget": request.budget,
                "interests": request.interests
            },
            "transportation": flights_hotels["flights"],
            "accommodation": flights_hotels["hotels"], 
            "activities": activities["activities"],
            "itinerary": itinerary["itinerary"],
            "user_memory": self.user_memory.get(user_id, {})
        }
        
        return final_plan


def format_trip_plan_markdown(plan: Dict[str, Any]) -> str:
    """Format the trip plan into readable markdown"""
    
    md = f"""# Trip Plan: {plan['request']['destination']}

## 📋 Trip Overview
- **Destination**: {plan['request']['destination']}
- **Dates**: {plan['request']['dates']['start_date']} to {plan['request']['dates']['end_date']}
- **Budget**: ${plan['request']['budget']}
- **Interests**: {', '.join(plan['request']['interests'])}
- **Estimated Total Cost**: ${plan['itinerary']['total_estimated_cost']}

## ✈️ Transportation
"""
    
    for flight in plan['transportation']:
        md += f"- **Flight {flight['option_id']}**: ${flight['price']}, {flight['duration']}\n"
        md += f"  Departure: {flight['departure']} → Arrival: {flight['arrival']}\n"
        md += f"  [Book Now]({flight['booking_link']})\n\n"
    
    md += "## 🏨 Accommodation\n"
    for hotel in plan['accommodation']:
        md += f"- **{hotel['name']}**: ${hotel['price']}/night, Rating: {hotel['rating']}/5\n"
        md += f"  Check-in: {hotel['check_in']} → Check-out: {hotel['check_out']}\n"
        md += f"  [Book Now]({hotel['booking_link']})\n\n"
    
    md += "## 📅 Daily Itinerary\n"
    for day in plan['itinerary']['daily_plan']:
        md += f"### {day['day_name']}, {day['date']}\n"
        md += f"**Accommodation**: {day['accommodation']}\n\n"
        
        for activity in day['activities']:
            md += f"- **{activity['time']}**: {activity['activity']} (${activity['price']})\n"
            md += f"  📍 {activity['location']}\n\n"
    
    return md


async def test_trip_agent():
    """Test the complete trip planning flow"""
    
    # Create a test trip request
    test_request = TripRequest(
        destination="Munich, Germany",
        dates={"start_date": "2024-10-01", "end_date": "2024-10-03"},
        budget=800,
        interests=["history", "craft beer", "Oktoberfest"],
        travelers=1
    )
    
    # Initialize orchestrator
    orchestrator = TripOrchestratorAgent()
    
    # Plan the trip
    trip_plan = await orchestrator.plan_trip(test_request)
    
    # Output results
    print("\n" + "="*60)
    print("🎉 TRIP PLAN GENERATED!")
    print("="*60)
    
    # Print as JSON for API testing
    print("\n📄 JSON Output:")
    print(json.dumps(trip_plan, indent=2))
    
    # Print as markdown for user presentation  
    print("\n📝 Markdown Output:")
    print(format_trip_plan_markdown(trip_plan))


if __name__ == "__main__":
    asyncio.run(test_trip_agent())