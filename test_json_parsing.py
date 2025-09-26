#!/usr/bin/env python3
"""
Test script to verify JSON parsing from agentcore output
"""

import json
import re

# Sample agentcore output (from your logs)
sample_output = """╭─────────────────────────────────────────────────────── travel_orchestrator ────────────────────────────────────────────────────────╮
│ Session: d60cac61-5627-44c6-b072-d4ad4f15ba54                                                                                      │
│ Request ID: 774b7e91-ca4e-4cab-9105-6aab75c3a79a                                                                                   │
│ ARN: arn:aws:bedrock-agentcore:us-west-2:362485256406:runtime/travel_orchestrator-BVUvNxBN5c                                       │
│ Logs: aws logs tail /aws/bedrock-agentcore/runtimes/travel_orchestrator-BVUvNxBN5c-DEFAULT --log-stream-name-prefix                │
│ "2025/09/26/[runtime-logs]" --follow                                                                                               │
│       aws logs tail /aws/bedrock-agentcore/runtimes/travel_orchestrator-BVUvNxBN5c-DEFAULT --log-stream-name-prefix                │
│ "2025/09/26/[runtime-logs]" --since 1h                                                                                             │
│ GenAI Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Response:
{"status": "success", "summary": "Dear valued traveler,\\n\\nI'm thrilled to present your exciting trip to Munich, Germany! While it's a slight change from your original Paris request, I believe you're in for an unforgettable adventure that perfectly aligns with your interests in history and culinary experiences. Your 3-day journey from September 26th to 28th, 2025, is packed with Bavarian charm and autumn festivities!\\n\\nGet ready to immerse yourself in Munich's rich history with a fascinating tour of Marienplatz, the city's central square. Then, embrace the lively Oktoberfest atmosphere at the world-famous Hofbräu Beer Garden, where you'll savor authentic German brews and cuisine. Your stay at the conveniently located Munich City Hotel puts you right in the heart of the action. The best part? We've managed to arrange all this for just $930, giving you excellent value within your $1200 budget and leaving some extra for those irresistible pretzels and souvenirs!\\n\\nI'm personally excited for you to experience the unique blend of history and celebration that Munich offers during this special time of year. Get ready for lederhosen, oompah bands, and unforgettable memories. Prost to your upcoming Bavarian adventure!", "trip_overview": {"destination": "Munich, Germany", "dates": "2024-10-01 to 2024-10-03", "duration": "3 days", "travelers": 1, "budget": "$800", "estimated_cost": "$930", "savings": "$0"}, "flight": {"id": "flight_001", "price": 450, "duration": "2h 30m", "departure": "10:30", "arrival": "13:00"}, "hotel": {"id": "hotel_001", "name": "Munich City Hotel", "price": 120, "rating": 4.2}, "activities": [{"name": "Marienplatz Historical Tour", "location": "Marienplatz", "price": "$25", "rating": "⭐ 4.6"}, {"name": "Hofbräu Beer Garden", "location": "Hofbräu München", "price": "$15", "rating": "⭐ 4.4"}], "daily_schedule": [{"date": "2024-10-01", "day": "Tuesday", "activities": ["10:00 - Marienplatz Historical Tour at Marienplatz ($25)", "14:00 - Hofbräu Beer Garden at Hofbräu München ($15)"]}, {"date": "2024-10-02", "day": "Wednesday", "activities": ["10:00 - Marienplatz Historical Tour at Marienplatz ($25)", "14:00 - Hofbräu Beer Garden at Hofbräu München ($15)"]}, {"date": "2024-10-03", "day": "Thursday", "activities": ["10:00 - Marienplatz Historical Tour at Marienplatz ($25)", "14:00 - Hofbräu Beer Garden at Hofbräu München ($15)"]}], "raw_data": {"trip_plan": {"request": {"destination": "Munich, Germany", "start_date": "2024-10-01", "end_date": "2024-10-03", "budget": 800, "interests": ["history", "beer", "Oktoberfest"], "travelers": 1}, "transportation": [{"id": "flight_001", "price": 450, "duration": "2h 30m", "departure": "10:30", "arrival": "13:00"}], "accommodation": [{"id": "hotel_001", "name": "Munich City Hotel", "price": 120, "rating": 4.2}], "activities": [{"id": "act_001", "name": "Marienplatz Historical Tour", "price": 25, "location": "Marienplatz", "rating": 4.6}, {"id": "act_002", "name": "Hofbräu Beer Garden", "price": 15, "location": "Hofbräu München", "rating": 4.4}], "itinerary": {"destination": "Munich, Germany", "duration": "3 days", "total_cost": 930, "daily_plan": [{"date": "2024-10-01", "day_name": "Tuesday", "activities": [{"time": "10:00", "activity": "Marienplatz Historical Tour", "location": "Marienplatz", "price": 25}, {"time": "14:00", "activity": "Hofbräu Beer Garden", "location": "Hofbräu München", "price": 15}]}, {"date": "2024-10-02", "day_name": "Wednesday", "activities": [{"time": "10:00", "activity": "Marienplatz Historical Tour", "location": "Marienplatz", "price": 25}, {"time": "14:00", "activity": "Hofbräu Beer Garden", "location": "Hofbräu München", "price": 15}]}, {"date": "2024-10-03", "day_name": "Thursday", "activities": [{"time": "10:00", "activity": "Marienplatz Historical Tour", "location": "Marienplatz", "price": 25}, {"time": "14:00", "activity": "Hofbräu Beer Garden", "location": "Hofbräu München", "price": 15}]}]}}}}"""

def test_json_parsing():
    print("🧪 Testing JSON parsing from agentcore output...")
    
    # Method 1: Look for "Response:" followed by JSON
    response_match = re.search(r'Response:\s*(\{.*\})', sample_output, re.DOTALL)
    if response_match:
        json_str = response_match.group(1).strip()
        try:
            response_data = json.loads(json_str)
            print("✅ Successfully extracted JSON from agentcore response!")
            print(f"📊 Status: {response_data.get('status')}")
            print(f"📍 Destination: {response_data.get('trip_overview', {}).get('destination')}")
            print(f"💰 Cost: {response_data.get('trip_overview', {}).get('estimated_cost')}")
            
            # Check if we have raw_data
            if 'raw_data' in response_data:
                print("✅ Found raw_data structure")
                trip_plan = response_data['raw_data']['trip_plan']
                print(f"🏨 Hotel: {trip_plan['accommodation'][0]['name']}")
                print(f"✈️ Flight: {trip_plan['transportation'][0]['duration']}")
            
            return response_data
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return None
    else:
        print("❌ Could not find Response: marker in output")
        return None

if __name__ == "__main__":
    result = test_json_parsing()
    if result:
        print("\n🎉 Test successful! JSON parsing should work in the web interface.")
    else:
        print("\n❌ Test failed! Need to fix JSON parsing.")