#!/bin/bash

# Stop all running A2A agents

echo "Stopping all agents..."

if [ -f "logs/pids.txt" ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping process $pid..."
            kill $pid
        fi
    done < logs/pids.txt
    
    rm logs/pids.txt
    echo "All agents stopped."
else
    echo "No PID file found. Agents may not be running."
    echo "You can manually stop processes using:"
    echo "  ps aux | grep a2a_server.py"
    echo "  kill <PID>"
fi

