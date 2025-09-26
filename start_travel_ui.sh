#!/bin/bash

# Start the Travel Planner Web Interface
echo "🚀 Starting AI Travel Planner Web Interface..."
echo "📍 Working directory: $(pwd)"

# Check if agentcore is available
if ! command -v agentcore &> /dev/null; then
    echo "❌ Error: 'agentcore' command not found"
    echo "Please ensure agentcore is installed and available in your PATH"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: 'python3' command not found"
    echo "Please ensure Python 3 is installed"
    exit 1
fi

echo "✅ agentcore found: $(which agentcore)"
echo "✅ Python found: $(which python3)"

# Start the server
echo ""
echo "🌍 Starting Travel Planner Server..."
echo "📂 Serving from: $(pwd)"
echo ""

python3 travel_server.py 8080