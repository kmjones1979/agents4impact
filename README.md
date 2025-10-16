# Google ADK A2A Multi-Agent System

A production-ready multi-agent system built with Google's Agent Development Kit (ADK) and Agent-to-Agent (A2A) protocol. This system provides a high-level orchestrator agent that coordinates three specialized remote agents: BigQuery, Ticket Management, and Maps Generation.

Force restart the web server with

```
cd /Users/kevinjones/google/mcp-ticket-server && pkill -f "tsx watch src/server.ts" && sleep 2 && npm run dev &
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Orchestrator Agent                     │
│              (High-Level Coordinator)                   │
│                    Port: 8000                           │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬─────────────┐
        │                         │             │
        ▼                         ▼             ▼
┌───────────────┐        ┌───────────────┐  ┌──────────────┐
│ BigQuery Agent│        │ Ticket Agent  │  │  Maps Agent  │
│   Port: 8001  │        │  Port: 8002   │  │  Port: 8003  │
└───────────────┘        └───────────────┘  └──────────────┘
```

## 🌟 Features

### Orchestrator Agent

-   Coordinates between specialized agents
-   Intelligently routes requests to appropriate agents
-   Aggregates and synthesizes multi-agent responses
-   Provides unified interface for complex workflows

### BigQuery Agent

-   Execute SQL queries on BigQuery datasets
-   List datasets and tables
-   Get table schemas and metadata
-   Analyze query results with built-in intelligence
-   Query cost and performance monitoring

### Ticket Agent

-   Create and manage support tickets
-   Update ticket status and add notes
-   Search and filter tickets
-   Categorize tickets (bug, feature, question, incident)
-   Priority management (low, medium, high, critical)

### Maps Agent

-   Geocode addresses to coordinates
-   Reverse geocode coordinates to addresses
-   Get directions between locations
-   Calculate distances and travel times
-   Find nearby places
-   Generate static map URLs

## 📋 Prerequisites

-   Python 3.10 or higher
-   Google Cloud Project with:
    -   Gemini API enabled
    -   BigQuery API enabled (for BigQuery agent)
    -   Maps API enabled (for Maps agent, optional)
-   Service account credentials (JSON key file)

## 🚀 Quick Start

### 1. Setup

Run the setup script:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:

-   Create a Python virtual environment
-   Install all dependencies
-   Create a `.env` file from the template
-   Set up necessary directories

### 2. Authentication

**Recommended: Use Application Default Credentials (no service account key needed!)**

```bash
# Install gcloud SDK (if not already installed)
brew install google-cloud-sdk

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login
```

Then edit `.env` file:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_API_KEY=your-gemini-api-key
# GOOGLE_APPLICATION_CREDENTIALS not needed with ADC!
```

**Note**: If your organization blocks service account keys, see [AUTHENTICATION.md](AUTHENTICATION.md) for detailed setup.

For getting your API keys, see [GET_CREDENTIALS.md](GET_CREDENTIALS.md)

### 3. Start All Agents

```bash
source venv/bin/activate
./scripts/start_all_agents.sh
```

This starts all four agents on their respective ports:

-   Orchestrator: http://localhost:8000
-   BigQuery Agent: http://localhost:8001
-   Ticket Agent: http://localhost:8002
-   Maps Agent: http://localhost:8003

### 4. Test the System

Run the example client:

```bash
python client_example.py
```

Or access the interactive API documentation:

-   http://localhost:8000/docs (Orchestrator)
-   http://localhost:8001/docs (BigQuery)
-   http://localhost:8002/docs (Ticket)
-   http://localhost:8003/docs (Maps)

### 5. Stop All Agents

```bash
./scripts/stop_all_agents.sh
```

## 💻 Usage Examples

### Using the Python Client

```python
from client_example import A2AClient
from config import Config

# Connect to orchestrator
orchestrator = A2AClient(f"http://localhost:{Config.ORCHESTRATOR_PORT}")

# Chat with the orchestrator
response = orchestrator.chat("What agents are available?")
print(response)

# Get agent card
card = orchestrator.get_agent_card()
print(f"Agent: {card['name']}")
print(f"Description: {card['description']}")

# Execute a tool directly
result = orchestrator.execute_tool("list_available_agents", {})
print(result)
```

### Using the REST API

#### Chat with an agent:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "List available agents"}'
```

#### Execute a tool:

```bash
curl -X POST http://localhost:8001/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "list_datasets",
    "parameters": {}
  }'
```

#### Create a ticket:

```bash
curl -X POST http://localhost:8002/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "create_ticket",
    "parameters": {
      "title": "System issue",
      "description": "Database connection timeout",
      "category": "bug",
      "priority": "high"
    }
  }'
```

#### Geocode an address:

```bash
curl -X POST http://localhost:8003/execute-tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "geocode",
    "parameters": {
      "address": "1600 Amphitheatre Parkway, Mountain View, CA"
    }
  }'
```

## 🛠️ Running Individual Agents

You can run agents individually for development or testing:

```bash
# Orchestrator only
python a2a_server.py --agent orchestrator

# BigQuery agent only
python a2a_server.py --agent bigquery

# Ticket agent only
python a2a_server.py --agent ticket

# Maps agent only
python a2a_server.py --agent maps

# Custom port
python a2a_server.py --agent orchestrator --port 9000
```

## 📁 Project Structure

```
google/
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Base agent class
│   ├── orchestrator.py         # Orchestrator agent
│   ├── bigquery_agent.py       # BigQuery agent
│   ├── ticket_agent.py         # Ticket management agent
│   └── maps_agent.py           # Maps generation agent
├── scripts/                     # Utility scripts
│   ├── setup.sh                # Setup script
│   ├── start_all_agents.sh     # Start all agents
│   └── stop_all_agents.sh      # Stop all agents
├── logs/                        # Agent logs
├── a2a_server.py               # A2A server implementation
├── client_example.py           # Example client code
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

| Variable                         | Description                         | Required |
| -------------------------------- | ----------------------------------- | -------- |
| `GOOGLE_CLOUD_PROJECT`           | Your Google Cloud project ID        | Yes      |
| `GOOGLE_API_KEY`                 | Gemini API key                      | Yes      |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account JSON        | Yes      |
| `BIGQUERY_DATASET`               | Default BigQuery dataset            | No       |
| `BIGQUERY_LOCATION`              | BigQuery location (default: US)     | No       |
| `MAPS_API_KEY`                   | Google Maps API key                 | No       |
| `ORCHESTRATOR_PORT`              | Orchestrator port (default: 8000)   | No       |
| `BIGQUERY_AGENT_PORT`            | BigQuery agent port (default: 8001) | No       |
| `TICKET_AGENT_PORT`              | Ticket agent port (default: 8002)   | No       |
| `MAPS_AGENT_PORT`                | Maps agent port (default: 8003)     | No       |

## 🚢 Deployment

### Local Development

Use the provided scripts (see Quick Start section).

### Docker (Coming Soon)

Dockerfiles for containerized deployment will be added in future updates.

### Cloud Run / Kubernetes

Each agent can be deployed independently as a microservice:

1. Containerize each agent
2. Deploy to Cloud Run or Kubernetes
3. Update agent URLs in orchestrator configuration
4. Set up authentication between agents

### Production Considerations

1. **Security**:

    - Implement authentication between agents
    - Use HTTPS/TLS for all communications
    - Rotate API keys regularly
    - Use Secret Manager for sensitive data

2. **Monitoring**:

    - Set up Cloud Monitoring and Logging
    - Track agent health and performance
    - Monitor API usage and costs

3. **Scaling**:

    - Use load balancers for high availability
    - Implement horizontal scaling for agents
    - Cache frequent queries

4. **Error Handling**:
    - Implement retry logic
    - Add circuit breakers
    - Set up alerting for failures

## 🧪 Testing

To run tests (when implemented):

```bash
pytest tests/
```

## 📚 A2A Protocol

This project implements Google's Agent-to-Agent (A2A) protocol, which enables:

-   **Standardized Communication**: Agents communicate using a common protocol
-   **Agent Discovery**: Agents can discover each other's capabilities via agent cards
-   **Interoperability**: Works with agents from different frameworks and vendors
-   **Scalability**: Agents can be deployed and scaled independently

### Agent Card Structure

Each agent exposes an agent card at `/agent-card`:

```json
{
  "name": "Agent Name",
  "description": "Agent description",
  "capabilities": {
    "tools": [...]
  },
  "metadata": {
    "version": "1.0.0",
    "agent_type": "AgentClassName"
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is provided as-is for educational and development purposes.

## 🔗 Resources

-   [Google ADK Documentation](https://google.github.io/adk-docs/)
-   [A2A Protocol Specification](https://google.github.io/adk-docs/a2a/)
-   [Gemini API](https://ai.google.dev/)
-   [Google Cloud BigQuery](https://cloud.google.com/bigquery)
-   [Google Maps Platform](https://developers.google.com/maps)

## 💡 Next Steps

1. **Enhance Agent Intelligence**: Add more sophisticated reasoning and tool usage
2. **Add More Agents**: Create agents for other Google services (Cloud Storage, Vertex AI, etc.)
3. **Implement Authentication**: Add OAuth2 or JWT-based authentication
4. **Add Observability**: Implement distributed tracing and metrics
5. **Create UI**: Build a web interface for interacting with agents
6. **Add Tests**: Comprehensive unit and integration tests
7. **Docker Support**: Add Dockerfiles and docker-compose setup

## ⚠️ Notes

-   The Maps agent uses mock implementations by default. Configure `MAPS_API_KEY` for real API calls.
-   The Ticket agent uses in-memory storage. For production, integrate with a real ticketing system.
-   BigQuery queries have a 10GB billing limit by default for safety.
-   All agents use the `gemini-2.0-flash-exp` model by default.

## 🐛 Troubleshooting

### Agents won't start

-   Check that all environment variables are set correctly
-   Ensure ports 8000-8003 are not in use
-   Verify Google Cloud credentials are valid

### BigQuery errors

-   Ensure BigQuery API is enabled in your project
-   Verify service account has BigQuery permissions
-   Check dataset and table names are correct

### Connection errors

-   Ensure all agents are running
-   Check firewall settings
-   Verify port configurations

For more help, check the logs in the `logs/` directory.

---

Built with ❤️ using Google ADK and A2A Protocol
