# Demo Scenarios & Examples

## 🎬 **Live Demo Script**

### Demo Flow (5 minutes total)
1. **Introduction** (30s): Project overview
2. **Live Demo** (2m): Agent in action  
3. **Architecture** (1m): Technical deep dive
4. **AWS Integration** (1m): Cloud services showcase
5. **Closing** (30s): Key value propositions

## 🧪 **Demo Scenarios**

### Scenario 1: Oktoberfest Trip Planning
**Command**:
```bash
agentcore invoke '{"prompt": "Plan a 3-day trip to Munich for Oktoberfest with a $1000 budget and interests in history and beer"}'
```

**Expected Response**:
```json
{
  "trip_plan": {
    "request": {
      "destination": "Munich, Germany",
      "start_date": "2024-10-01", 
      "end_date": "2024-10-03",
      "budget": 800,
      "interests": ["history", "beer", "Oktoberfest"],
      "travelers": 1
    },
    "transportation": [
      {"id": "flight_001", "price": 450, "duration": "2h 30m", "departure": "10:30", "arrival": "13:00"}
    ],
    "accommodation": [
      {"id": "hotel_001", "name": "Munich City Hotel", "price": 120, "rating": 4.2}
    ],
    "activities": [
      {"id": "act_001", "name": "Marienplatz Historical Tour", "price": 25, "location": "Marienplatz", "rating": 4.6},
      {"id": "act_002", "name": "Hofbräu Beer Garden", "price": 15, "location": "Hofbräu München", "rating": 4.4}
    ],
    "itinerary": {
      "destination": "Munich, Germany",
      "duration": "3 days",
      "total_cost": 930,
      "daily_plan": [
        {
          "date": "2024-10-01",
          "day_name": "Tuesday", 
          "activities": [
            {"time": "10:00", "activity": "Marienplatz Historical Tour", "location": "Marienplatz", "price": 25},
            {"time": "14:00", "activity": "Hofbräu Beer Garden", "location": "Hofbräu München", "price": 15}
          ]
        },
        // ... similar for other days
      ]
    }
  },
  "message": "Generated complete trip plan for Munich, Germany (3 days). Total estimated cost: $930"
}
```

**Demo Points to Highlight**:
- ✅ **Natural Language Understanding**: Parsed complex request
- ✅ **Interest Matching**: Found history + beer activities
- ✅ **Budget Awareness**: $930 cost within $1000 budget
- ✅ **Complete Planning**: Flights, hotels, activities, schedule
- ✅ **Structured Output**: API-ready JSON + human message

### Scenario 2: Budget-Conscious Planning
**Command**:
```bash
agentcore invoke '{"prompt": "Plan a weekend trip to Berlin focused on museums and history, budget $600"}'
```

**Demo Points**:
- Shows budget constraint handling
- Interest-based activity selection
- Different destination handling
- Cost optimization logic

### Scenario 3: Family Travel
**Command**:
```bash
agentcore invoke '{"prompt": "Plan a family trip to London for 4 people with kids, budget $3000"}'
```

**Demo Points**:
- Multiple travelers consideration
- Family-friendly planning
- Larger budget management
- Scalable request handling

### Scenario 4: Quick Business Trip
**Command**:
```bash
agentcore invoke '{"prompt": "Plan a 2-day business trip to Paris with focus on meetings and good restaurants"}'
```

**Demo Points**:
- Different trip purpose recognition
- Business-oriented planning
- Short duration optimization
- Professional focus matching

## 📊 **Performance Demonstration**

### Speed Test
```bash
# Time the response
time agentcore invoke '{"prompt": "Quick trip to Amsterdam"}'
```
**Expected**: < 1 second response time

### Concurrent Requests
```bash
# Multiple simultaneous requests
agentcore invoke '{"prompt": "Trip to Rome"}' &
agentcore invoke '{"prompt": "Trip to Tokyo"}' &  
agentcore invoke '{"prompt": "Trip to NYC"}' &
wait
```
**Demo Point**: Shows auto-scaling capabilities

### Status Check
```bash
agentcore status
```
**Expected Output**:
```
Ready - Agent deployed and endpoint available
Agent ARN: arn:aws:bedrock-agentcore:us-west-2:362485256406:runtime/travel_orchestrator-BVUvNxBN5c
Endpoint: DEFAULT (READY)
```

## 🔍 **Monitoring Demonstration**

### Real-time Logs
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/travel_orchestrator-BVUvNxBN5c-DEFAULT --log-stream-name-prefix "2025/09/26/[runtime-logs]" --follow
```
**Demo Point**: Show live execution monitoring

### CloudWatch Dashboard
**URL**: https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core
**Demo Point**: AWS GenAI observability integration

## 💬 **Presentation Talking Points**

### Opening Hook
> "What if you could plan a complete vacation just by saying: 'Plan a 3-day trip to Munich for Oktoberfest with a $1000 budget'? Let me show you an AI agent that does exactly that, deployed on AWS Bedrock AgentCore."

### Technical Innovation
> "This isn't just a chatbot - it's a sophisticated multi-agent system where specialized agents handle different aspects: one finds flights and hotels, another matches your interests to activities, and a third creates the optimal day-by-day schedule."

### AWS Integration  
> "Built on AWS Bedrock AgentCore, this demonstrates serverless AI agent deployment with automatic scaling, comprehensive monitoring, and production-grade security - all deployed in under 4 hours."

### Business Value
> "This architecture pattern can be applied to any domain requiring complex orchestration: financial planning, event management, or supply chain optimization."

### Demo Transition
> "Let me show you this in action. I'll ask our AI agent to plan a trip, and you'll see the complete orchestration happen in real-time."

## 🎯 **Interactive Elements**

### Audience Participation
1. **Ask for Trip Ideas**: "Where would you like to travel?"
2. **Live Input**: Use audience suggestions for demo commands
3. **Budget Game**: "What budget would you set?"
4. **Interest Matching**: Show how different interests change results

### Q&A Preparation
**Common Questions & Answers**:

**Q**: "How does it handle different destinations?"
**A**: The orchestrator adapts to any destination, with activity agents matching local experiences to user interests.

**Q**: "What about real API integration?"  
**A**: The architecture is designed for easy API integration - we use mock data for reliable demos, but production would connect to Skyscanner, Booking.com, etc.

**Q**: "How does it scale?"
**A**: AWS Bedrock AgentCore provides serverless auto-scaling. Each request gets its own isolated microVM with automatic resource management.

**Q**: "What's the cost?"
**A**: Pay-per-use model - you only pay when the agent is actively processing requests, not for idle time.

## 🚨 **Backup Demo Options**

### If Live Demo Fails
1. **Screenshots**: Pre-captured successful responses
2. **Local Version**: Fall back to `python3 local_testing.py`
3. **Video**: Screen recording of successful deployment
4. **Architecture Focus**: Emphasize technical design over live demo

### If Network Issues
1. **Offline Architecture Diagrams**
2. **Code Walkthrough**: Show `travel_orchestrator.py`
3. **Documentation Review**: `DEPLOYMENT_STATUS.md`
4. **Local Testing**: Run without AWS connection

---

**Demo Status**: ✅ Multiple scenarios tested and validated  
**Backup Plans**: Comprehensive fallback options prepared  
**Interactive Elements**: Audience engagement strategies ready  
**Technical Depth**: Both high-level and detailed explanations available