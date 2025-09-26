#!/usr/bin/env python3
"""
Travel Orchestrator Agent for AWS Bedrock AgentCore
Main orchestrator that coordinates all sub-agents
"""

try:
    from bedrock_agentcore import BedrockAgentCoreApp
    AGENTCORE_AVAILABLE = True
    app = BedrockAgentCoreApp()
except ImportError:
    AGENTCORE_AVAILABLE = False
    print("Running in local test mode - AgentCore SDK not available")

import json
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any

class TravelOrchestratorAgent:
    """Main orchestrator agent for travel planning"""
    
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
    def parse_trip_request(self, user_input: str) -> Dict[str, Any]:
        """Parse user input into structured trip request"""
        # Use Bedrock to parse natural language into structured data
        prompt = f"""
        Parse this travel request into structured JSON:
        "{user_input}"
        
        Return only valid JSON with these fields:
        {{
            "destination": "city, country",
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD", 
            "budget": number,
            "interests": ["interest1", "interest2"],
            "travelers": number
        }}
        """
        # TODO - LLM call to Bedrock
        
        # For now, use a simple parser (in production, use Bedrock)
        return {
            "destination": "Munich, Germany",
            "start_date": "2024-10-01",
            "end_date": "2024-10-03",
            "budget": 800,
            "interests": ["history", "beer", "Oktoberfest"],
            "travelers": 1
        }
    
    def call_flights_hotels_agent(self, request: Dict) -> Dict:
        """Call the flights & hotels agent"""
        # Simulate agent-to-agent communication
        return {
            "flights": [{
                "id": "flight_001",
                "price": 450,
                "duration": "2h 30m",
                "departure": "10:30",
                "arrival": "13:00"
            }],
            "hotels": [{
                "id": "hotel_001",
                "name": "Munich City Hotel",
                "price": 120,
                "rating": 4.2
            }]
        }
    
    def call_activities_agent(self, request: Dict) -> Dict:
        """Call the activities agent"""
        activities = []
        
        if "history" in request.get("interests", []):
            activities.append({
                "id": "act_001",
                "name": "Marienplatz Historical Tour",
                "price": 25,
                "location": "Marienplatz",
                "rating": 4.6
            })
            
        if any(beer in request.get("interests", []) for beer in ["beer", "Oktoberfest"]):
            activities.append({
                "id": "act_002",
                "name": "Hofbräu Beer Garden",
                "price": 15,
                "location": "Hofbräu München",
                "rating": 4.4
            })
            
        return {"activities": activities}
    
    def call_itinerary_agent(self, flights_hotels: Dict, activities: Dict, request: Dict) -> Dict:
        """Call the itinerary agent"""
        start_date = datetime.strptime(request["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(request["end_date"], "%Y-%m-%d")
        
        days = []
        current_date = start_date
        
        while current_date <= end_date:
            day_activities = []
            for i, activity in enumerate(activities.get("activities", [])):
                if i < 2:  # Max 2 activities per day
                    day_activities.append({
                        "time": "10:00" if i == 0 else "14:00",
                        "activity": activity["name"],
                        "location": activity["location"],
                        "price": activity["price"]
                    })
            
            days.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_name": current_date.strftime("%A"),
                "activities": day_activities
            })
            
            current_date += timedelta(days=1)
        
        # Calculate total cost
        flight_cost = sum(f["price"] for f in flights_hotels.get("flights", []))
        hotel_cost = sum(h["price"] for h in flights_hotels.get("hotels", [])) * len(days)
        activity_cost = sum(a["price"] for day in days for a in day["activities"])
        
        return {
            "destination": request["destination"],
            "duration": f"{len(days)} days",
            "total_cost": flight_cost + hotel_cost + activity_cost,
            "daily_plan": days
        }
    
    def generate_ai_summary(self, trip_plan_data: Dict[str, Any], user_input: str) -> str:
        """Use Bedrock LLM to generate a natural language summary of the trip plan"""
        print(f"🤖 Starting AI summary generation with model: {self.model_id}")
        try:
            # Extract key information for the prompt
            destination = trip_plan_data["trip_plan"]["request"]["destination"]
            duration = trip_plan_data["trip_plan"]["itinerary"]["duration"]
            total_cost = trip_plan_data["trip_plan"]["itinerary"]["total_cost"]
            budget = trip_plan_data["trip_plan"]["request"]["budget"]
            interests = ", ".join(trip_plan_data["trip_plan"]["request"]["interests"])
            activities = [act["name"] for act in trip_plan_data["trip_plan"]["activities"]]
            hotel = trip_plan_data["trip_plan"]["accommodation"][0]["name"]
            
            # Create a comprehensive prompt for the LLM
            prompt = f"""You are a friendly and professional travel agent. Based on the trip planning data below, create an engaging and personalized travel summary for the customer.

User's Original Request: "{user_input}"

Trip Details:
- Destination: {destination}
- Duration: {duration}
- Budget: ${budget}
- Total Estimated Cost: ${total_cost}
- Interests: {interests}
- Hotel: {hotel}
- Activities planned: {', '.join(activities)}

Please write a warm, enthusiastic, and informative summary that:
1. Acknowledges their specific interests and budget
2. Highlights the exciting experiences they'll have
3. Mentions the great value (cost vs budget)
4. Creates excitement about their upcoming trip
5. Keep it concise but engaging (2-3 paragraphs)

Write in a friendly, professional tone as if you're personally excited to help them plan this amazing trip."""

            # Prepare the request for Bedrock
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            ai_summary = response_body['content'][0]['text']
            
            return ai_summary
            
        except Exception as e:
            # Fallback to basic message if LLM call fails - include error details for debugging
            error_msg = f"LLM call failed: {type(e).__name__}: {str(e)}"
            print(error_msg)
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            # Return error details in the fallback message for debugging
            return f"Generated complete trip plan for {trip_plan_data['trip_plan']['request']['destination']} ({trip_plan_data['trip_plan']['itinerary']['duration']}). Total estimated cost: ${trip_plan_data['trip_plan']['itinerary']['total_cost']} [DEBUG: {error_msg}]"

# Create agent instance
orchestrator = TravelOrchestratorAgent()

def invoke_handler(payload):
    """Main agent entrypoint"""
    try:
        user_input = payload.get("prompt", "Plan a trip to Munich")
        
        # Step 1: Parse user request
        trip_request = orchestrator.parse_trip_request(user_input)
        
        # Step 2: Call sub-agents
        flights_hotels = orchestrator.call_flights_hotels_agent(trip_request)
        activities = orchestrator.call_activities_agent(trip_request)
        itinerary = orchestrator.call_itinerary_agent(flights_hotels, activities, trip_request)
        
        # Step 3: Format response
        response = {
            "trip_plan": {
                "request": trip_request,
                "transportation": flights_hotels["flights"],
                "accommodation": flights_hotels["hotels"],
                "activities": activities["activities"],
                "itinerary": itinerary
            },
            "message": f"Generated complete trip plan for {itinerary['destination']} ({itinerary['duration']}). Total estimated cost: ${itinerary['total_cost']}"
        }
        
        # Step 4: Generate AI-powered natural language summary using Bedrock
        try:
            ai_summary = orchestrator.generate_ai_summary(response, user_input)
            response["ai_summary"] = ai_summary
            print(f"✅ AI Summary generated successfully")
        except Exception as e:
            print(f"⚠️ AI Summary generation failed: {e}")
            # Continue with basic response
        
        return response
        
    except Exception as e:
        return {
            "error": f"Failed to generate trip plan: {str(e)}",
            "message": "Sorry, I encountered an error while planning your trip. Please try again."
        }

# Configure for AgentCore or local testing
if AGENTCORE_AVAILABLE:
    @app.entrypoint
    def invoke(payload):
        return invoke_handler(payload)

# Local testing server
if __name__ == "__main__":
    if AGENTCORE_AVAILABLE:
        app.run()
    else:
        # Simple local test
        test_payload = {"prompt": "Plan a 3-day trip to Munich for Oktoberfest"}
        result = invoke_handler(test_payload)
        print("Local Test Result:")
        print(json.dumps(result, indent=2))