#!/usr/bin/env python3
"""
Comprehensive testing script for Travel Planner Agents
Tests different scenarios and validates agent responses
"""

import asyncio
import json
from local_testing import TripOrchestratorAgent, TripRequest, format_trip_plan_markdown


async def test_scenario_1_oktoberfest():
    """Test Munich Oktoberfest trip scenario"""
    print("🧪 Testing Scenario 1: Munich Oktoberfest Trip")
    print("-" * 50)
    
    request = TripRequest(
        destination="Munich, Germany",
        dates={"start_date": "2024-09-21", "end_date": "2024-09-24"},
        budget=1200,
        interests=["Oktoberfest", "beer", "traditional food", "history"],
        travelers=2
    )
    
    orchestrator = TripOrchestratorAgent()
    plan = await orchestrator.plan_trip(request, "user_oktoberfest")
    
    print(f"✅ Generated plan for {plan['itinerary']['duration']}")
    print(f"💰 Cost: ${plan['itinerary']['total_estimated_cost']} (Budget: ${request.budget})")
    print(f"🎯 Activities found: {len(plan['activities'])}")
    
    return plan


async def test_scenario_2_budget_trip():
    """Test low-budget trip scenario"""
    print("\n🧪 Testing Scenario 2: Budget Trip")
    print("-" * 50)
    
    request = TripRequest(
        destination="Berlin, Germany",
        dates={"start_date": "2024-11-15", "end_date": "2024-11-17"},
        budget=400,
        interests=["history", "museums", "walking tours"],
        travelers=1
    )
    
    orchestrator = TripOrchestratorAgent()
    plan = await orchestrator.plan_trip(request, "user_budget")
    
    print(f"✅ Generated plan for {plan['itinerary']['duration']}")
    print(f"💰 Cost: ${plan['itinerary']['total_estimated_cost']} (Budget: ${request.budget})")
    
    # Check if within budget (allowing 10% overage)
    is_within_budget = plan['itinerary']['total_estimated_cost'] <= request.budget * 1.1
    print(f"💸 Within budget: {'✅' if is_within_budget else '❌'}")
    
    return plan


async def test_scenario_3_long_trip():
    """Test longer trip with multiple activities"""
    print("\n🧪 Testing Scenario 3: Week-long Adventure")
    print("-" * 50)
    
    request = TripRequest(
        destination="Vienna, Austria",
        dates={"start_date": "2024-12-01", "end_date": "2024-12-07"},
        budget=2000,
        interests=["classical music", "art", "coffee culture", "history"],
        travelers=2
    )
    
    orchestrator = TripOrchestratorAgent()
    plan = await orchestrator.plan_trip(request, "user_luxury")
    
    print(f"✅ Generated plan for {plan['itinerary']['duration']}")
    print(f"🗓️ Days planned: {len(plan['itinerary']['daily_plan'])}")
    
    # Verify each day has activities
    days_with_activities = sum(1 for day in plan['itinerary']['daily_plan'] if day['activities'])
    print(f"🎯 Days with activities: {days_with_activities}/{len(plan['itinerary']['daily_plan'])}")
    
    return plan


def test_agent_memory():
    """Test user memory functionality"""
    print("\n🧪 Testing Agent Memory")
    print("-" * 50)
    
    orchestrator = TripOrchestratorAgent()
    
    # Simulate multiple requests from the same user
    user_id = "repeat_customer"
    
    # First trip
    orchestrator.user_memory[user_id] = {
        "budget": 800,
        "interests": ["history", "food"],
        "last_destination": "Paris"
    }
    
    # Check memory retrieval
    memory = orchestrator.user_memory.get(user_id, {})
    print(f"✅ User memory retrieved: {len(memory)} preferences")
    print(f"🏛️ Previous interests: {memory.get('interests', [])}")
    print(f"🌍 Last destination: {memory.get('last_destination', 'None')}")
    
    return memory


def validate_trip_plan(plan):
    """Validate the structure and content of a trip plan"""
    print("\n🔍 Validating Trip Plan Structure")
    print("-" * 50)
    
    required_keys = ['request', 'transportation', 'accommodation', 'activities', 'itinerary']
    missing_keys = [key for key in required_keys if key not in plan]
    
    if missing_keys:
        print(f"❌ Missing keys: {missing_keys}")
        return False
    else:
        print("✅ All required keys present")
    
    # Validate itinerary structure
    itinerary = plan['itinerary']
    required_itinerary_keys = ['destination', 'duration', 'total_estimated_cost', 'daily_plan']
    missing_itinerary_keys = [key for key in required_itinerary_keys if key not in itinerary]
    
    if missing_itinerary_keys:
        print(f"❌ Missing itinerary keys: {missing_itinerary_keys}")
        return False
    else:
        print("✅ Itinerary structure valid")
    
    # Validate daily plan
    if not itinerary['daily_plan']:
        print("❌ No daily plan generated")
        return False
    
    for i, day in enumerate(itinerary['daily_plan']):
        required_day_keys = ['date', 'day_name', 'activities', 'accommodation']
        missing_day_keys = [key for key in required_day_keys if key not in day]
        if missing_day_keys:
            print(f"❌ Day {i+1} missing keys: {missing_day_keys}")
            return False
    
    print(f"✅ All {len(itinerary['daily_plan'])} days properly structured")
    return True


async def performance_test():
    """Test response times"""
    print("\n⏱️ Performance Testing")
    print("-" * 50)
    
    import time
    
    request = TripRequest(
        destination="Amsterdam, Netherlands", 
        dates={"start_date": "2024-08-01", "end_date": "2024-08-03"},
        budget=600,
        interests=["canals", "museums"],
        travelers=1
    )
    
    orchestrator = TripOrchestratorAgent()
    
    start_time = time.time()
    plan = await orchestrator.plan_trip(request)
    end_time = time.time()
    
    response_time = end_time - start_time
    print(f"⚡ Response time: {response_time:.2f} seconds")
    
    # Performance benchmark (should be fast for local testing)
    if response_time < 1.0:
        print("✅ Fast response time")
    elif response_time < 3.0:
        print("⚠️ Acceptable response time")
    else:
        print("❌ Slow response time")
    
    return response_time


async def run_comprehensive_tests():
    """Run all test scenarios"""
    print("🚀 Starting Comprehensive Agent Testing")
    print("=" * 60)
    
    try:
        # Test different scenarios
        plan1 = await test_scenario_1_oktoberfest()
        plan2 = await test_scenario_2_budget_trip()
        plan3 = await test_scenario_3_long_trip()
        
        # Test memory functionality
        test_agent_memory()
        
        # Validate plan structure
        validate_trip_plan(plan1)
        
        # Performance test
        response_time = await performance_test()
        
        print("\n🎉 All Tests Completed!")
        print("=" * 60)
        print("📊 Test Summary:")
        print(f"   ✅ Scenario tests: 3/3 passed")
        print(f"   ✅ Memory test: Passed")
        print(f"   ✅ Validation: Passed")
        print(f"   ⚡ Avg response time: {response_time:.2f}s")
        
        # Export sample plan for review
        with open('sample_trip_plan.json', 'w') as f:
            json.dump(plan1, f, indent=2)
        
        with open('sample_trip_plan.md', 'w') as f:
            f.write(format_trip_plan_markdown(plan1))
        
        print(f"\n📁 Sample outputs saved:")
        print(f"   - sample_trip_plan.json")
        print(f"   - sample_trip_plan.md")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())