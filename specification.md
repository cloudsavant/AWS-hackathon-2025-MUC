1. Prompts to Develop Each Stage
These prompts are what you can feed to your AI agents (or use yourself during design) to ensure each module works as intended.
🧭 Orchestrator (Trip Agent)
Prompt to design:
"You are the main travel planner agent. When a user requests a trip, break it into subtasks: flights, hotels, activities, and itinerary creation. Maintain memory of user preferences like budget, interests, and constraints. Return structured task requests to the relevant specialized agents."
✈️ Flights & Hotels Agent
Prompt to design:
"You are the flight and hotel agent. Given a destination, dates, budget, and traveler details, use the [Skyscanner/Booking API stubs] to fetch best options. Return results in structured JSON format with fields: option_id, price, duration, check_in/out, booking_link."
🏰 Activities Agent
Prompt to design:
"You are the activities agent. Based on user preferences (history, nightlife, food, etc.), find activities, tours, or events via APIs (TripAdvisor, Yelp, Eventbrite). Include times, prices, and ratings. Return results in JSON: activity_id, name, description, time_slots, price, location."
📅 Itinerary Agent
Prompt to design:
"You are the itinerary planner. Given flight, hotel, and activities data, assemble a day-by-day plan that balances travel time, rest, and preferences. Ensure feasibility by checking opening hours. Return the itinerary in human-readable markdown and JSON format."
2. System Architecture on AWS
Here’s a high-level design for AgentCore + Bedrock + APIs:
[User] 
   ↓
Amazon API Gateway (entrypoint, auth with Cognito/AgentCore Identity) 
   ↓
AgentCore Orchestrator Agent (Bedrock LLM, orchestrates subtasks)
   ↓
────────── Specialized Agents (AgentCore Rooms) ──────────
   ↓                ↓                  ↓
Flights/Hotels   Activities         Itinerary 
(Calls APIs)     (Calls APIs)       (Organizes output)
   ↓                ↓                  ↓
────────── Aggregated Response ──────────
   ↓
Orchestrator → Formats into Final Trip Plan → Returns to User
AWS Services Involved:
Amazon Bedrock: Core LLM reasoning.
AgentCore Gateway: Manages orchestration & sub-agent calls.
AgentCore Identity + Memory: User authentication + preference memory.
Lambda Functions: Connect to 3rd-party APIs (Skyscanner, Booking, TripAdvisor).
DynamoDB: Cache and store itineraries & user trip history.
CloudWatch: Logs & monitoring.
3. Deployment Roadmap (with Rooms)
You’ll use AgentCore Rooms (modular “chat rooms” for sub-agents). Here’s a step-by-step plan:
Room 1 – Orchestrator
Build main Trip Agent.
Connect to AgentCore Identity & Memory.
Store/retrieve user preferences (budget, interests).
Room 2 – Flights & Hotels
Create specialized room for travel data.
Integrate API connectors (Skyscanner, Booking).
Deploy via AWS Lambda + API Gateway.
Room 3 – Activities
Another room focused on experiences.
Connect to TripAdvisor/Yelp/Eventbrite APIs.
Normalize results into JSON.
Room 4 – Itinerary
Take structured results from other rooms.
Use Bedrock to generate day-by-day itinerary.
Output in both conversational + structured formats.
Room 5 – Integration
Orchestrator pulls all rooms together.
Test multi-turn conversations (user modifies budget, adds preferences, etc.).
Store itineraries in DynamoDB.
Final Step – Deployment
Deploy orchestrator + rooms into AWS AgentCore Gateway.
Hook into Cognito for secure user login.
Test with a sample use case (Munich Oktoberfest trip).
Add observability (CloudWatch dashboards + alarms).