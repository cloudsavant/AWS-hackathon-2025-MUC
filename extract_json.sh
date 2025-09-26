#!/bin/bash
# Helper script to extract JSON from agentcore invoke responses

# Run agentcore command and extract just the JSON response
agentcore invoke "$1" | sed -n '/^{.*$/,/}$/p' | tr -d '\n' | jq .