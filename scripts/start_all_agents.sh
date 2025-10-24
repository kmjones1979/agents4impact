#!/bin/bash

# Start all A2A agents in separate processes
# This script is for development/testing purposes

echo "Starting Google ADK A2A Multi-Agent System..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

# Start each agent in the background
echo "Starting BigQuery Agent on port 8001..."
python a2a_server.py --agent bigquery > logs/bigquery_agent.log 2>&1 &
BIGQUERY_PID=$!

echo "Starting Ticket Agent on port 8002..."
python a2a_server.py --agent ticket > logs/ticket_agent.log 2>&1 &
TICKET_PID=$!

echo "Starting Maps Agent on port 8003..."
python a2a_server.py --agent maps > logs/maps_agent.log 2>&1 &
MAPS_PID=$!

# Wait a bit for agents to start
sleep 3

echo "Starting Orchestrator Agent on port 8000..."
python a2a_server.py --agent orchestrator > logs/orchestrator_agent.log 2>&1 &
ORCHESTRATOR_PID=$!

# Save PIDs to file for cleanup
echo $BIGQUERY_PID > logs/pids.txt
echo $TICKET_PID >> logs/pids.txt
echo $MAPS_PID >> logs/pids.txt
echo $ORCHESTRATOR_PID >> logs/pids.txt

echo ""
echo "All agents started successfully!"
echo "================================"
echo "Orchestrator:    http://localhost:8000"
echo "BigQuery Agent:  http://localhost:8001"
echo "Ticket Agent:    http://localhost:8002"
echo "Maps Agent:      http://localhost:8003"
echo ""
echo "API Documentation:"
echo "  Orchestrator:    http://localhost:8000/docs"
echo "  BigQuery Agent:  http://localhost:8001/docs"
echo "  Ticket Agent:    http://localhost:8002/docs"
echo "  Maps Agent:      http://localhost:8003/docs"
echo ""
echo "Logs are being written to the logs/ directory"
echo "To stop all agents, run: ./scripts/stop_all_agents.sh"
echo ""
echo "Try the example client: python client_example.py"


