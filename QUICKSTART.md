# Quick Start Guide

Get started with the Google ADK A2A Multi-Agent System in 5 minutes!

## Prerequisites

- Python 3.10+
- Google Cloud account
- Gemini API key

## Step 1: Setup

```bash
# Clone or navigate to the project
cd google

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Step 2: Authenticate & Configure

**Authenticate with Google Cloud (Recommended - No service account key needed!)**:

```bash
# Install gcloud SDK
brew install google-cloud-sdk

# Login and setup ADC
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

**Edit `.env` file**:

```bash
# Required
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_API_KEY=your-gemini-api-key

# Optional
BIGQUERY_DATASET=your-dataset
MAPS_API_KEY=your-maps-key
```

**Note**: See [AUTHENTICATION.md](AUTHENTICATION.md) if you have organization policy restrictions.

## Step 3: Start Agents

```bash
# Activate virtual environment
source venv/bin/activate

# Start all agents
./scripts/start_all_agents.sh
```

You should see:
```
All agents started successfully!
================================
Orchestrator:    http://localhost:8000
BigQuery Agent:  http://localhost:8001
Ticket Agent:    http://localhost:8002
Maps Agent:      http://localhost:8003
```

## Step 4: Test the System

### Option A: Use the Example Client

```bash
python client_example.py
```

### Option B: Try the API Directly

```bash
# Chat with orchestrator
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What agents are available?"}'

# Create a ticket
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "create_ticket",
    "parameters": {
      "title": "My first ticket",
      "description": "Testing the system",
      "category": "question",
      "priority": "medium"
    }
  }'

# Geocode an address
curl -X POST http://localhost:8003/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "geocode",
    "parameters": {
      "address": "1600 Amphitheatre Parkway, Mountain View, CA"
    }
  }'
```

### Option C: Explore the Interactive API Docs

Open in your browser:
- http://localhost:8000/docs - Orchestrator
- http://localhost:8001/docs - BigQuery Agent
- http://localhost:8002/docs - Ticket Agent
- http://localhost:8003/docs - Maps Agent

## Step 5: Stop Agents

```bash
./scripts/stop_all_agents.sh
```

## Using Make Commands

```bash
make help      # Show all available commands
make setup     # Initial setup
make start     # Start all agents
make stop      # Stop all agents
make test      # Run tests
make client    # Run example client
make clean     # Clean up
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the README**: See `README.md` for detailed documentation
3. **Customize agents**: Edit files in `agents/` directory
4. **Add your own agent**: Follow the guide in `CONTRIBUTING.md`

## Common Issues

### Port already in use
```bash
# Check what's using the port
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Module not found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Authentication errors
- Verify `GOOGLE_API_KEY` is set correctly
- Check service account credentials path
- Ensure required APIs are enabled in Google Cloud

## Docker Quick Start

Prefer Docker? Use docker-compose:

```bash
# Build and start all agents
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all agents
docker-compose down
```

## Need Help?

- Check the logs: `tail -f logs/orchestrator_agent.log`
- Read the full README: `README.md`
- See examples: `client_example.py`
- Open an issue on GitHub

Happy building! 🚀

