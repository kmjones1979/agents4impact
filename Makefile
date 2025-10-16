.PHONY: help setup install start stop test clean

help:
	@echo "Google ADK A2A Multi-Agent System"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup      - Initial setup (create venv, install deps)"
	@echo "  make install    - Install/update dependencies"
	@echo "  make start      - Start all agents"
	@echo "  make stop       - Stop all agents"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up generated files"
	@echo "  make client     - Run example client"
	@echo ""

setup:
	@echo "Setting up project..."
	@./scripts/setup.sh

install:
	@echo "Installing dependencies..."
	@source venv/bin/activate && pip install -r requirements.txt

start:
	@echo "Starting all agents..."
	@./scripts/start_all_agents.sh

stop:
	@echo "Stopping all agents..."
	@./scripts/stop_all_agents.sh

test:
	@echo "Running tests..."
	@source venv/bin/activate && pytest tests/ -v

clean:
	@echo "Cleaning up..."
	@rm -rf venv/
	@rm -rf logs/*.log
	@rm -f logs/pids.txt
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup complete"

client:
	@echo "Running example client..."
	@source venv/bin/activate && python client_example.py

