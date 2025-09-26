
https://gemini.google.com/share/d96f0ff67110 
Session: f42784f2-0f1d-4d01-b69e-1839ff0611b7                                                   │
     3  │ Request ID: afe93eb5-53db-457f-885c-6d16768bcc3f                                                │
     4  │ ARN: arn:aws:bedrock-agentcore:us-west-2:362485256406:runtime/travel_orchestrator-BVUvNxBN5c    │
     5  │ Logs: aws logs tail /aws/bedrock-agentcore/runtimes/travel_orchestrator-BVUvNxBN5c-DEFAULT      │
     6  │ --log-stream-name-prefix "2025/09/26/[runtime-logs]" --follow                                   │
     7  │       aws logs tail /aws/bedrock-agentcore/runtimes/travel_orchestrator-BVUvNxBN5c-DEFAULT      │
     8  │ --log-stream-name-prefix "2025/09/26/[runtime-logs]" --since 1h                                 │
     9  │ GenAI Dashboard:                                                                                │
    10  │ https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#gen-ai-observability/agent-core

    ----

    cd /home/buxi/development/AWS-hackathon-2025-MUC && agentcore invoke '{"prompt": "Plan a family trip to London for 4 people with kids, budget $3000"}' | sed -n '14,31p' | tr -d '\n' | jq .

    