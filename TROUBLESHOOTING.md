# Troubleshooting Guide

## 🔐 Authentication Issues

### Issue: "There was a problem with web authentication"

**Solution 1: Try `gcloud auth login` first**

```bash
# Regular gcloud auth (works more reliably)
gcloud auth login --no-browser

# Then try ADC
gcloud auth application-default login --no-launch-browser
```

**Solution 2: Use alternative ADC method**

If you're on macOS and having browser issues:

```bash
# Method 1: Try with different flags
gcloud auth application-default login --no-launch-browser

# Method 2: Use gcloud auth for everything
gcloud auth login --no-browser
gcloud config set project YOUR_PROJECT_ID

# The agents will automatically use your gcloud credentials
```

**Solution 3: Manual token copy**

1. On a machine WITH a browser (even your phone!):
    - Install gcloud if needed
    - Run: `gcloud auth application-default login`
2. After successful auth, copy the credentials file:

    - **macOS/Linux**: `~/.config/gcloud/application_default_credentials.json`
    - **Windows**: `%APPDATA%\gcloud\application_default_credentials.json`

3. Copy that file to the same location on your current machine

---

### Issue: "scope is required but not consented"

This means you didn't grant all permissions. Re-run and make sure to:

```bash
gcloud auth application-default login --no-browser
```

When the browser opens:

1. ✅ Check **all permission boxes**
2. ✅ Click "Allow" (not "Deny")
3. ✅ Grant access to "cloud-platform" scope

---

### Issue: "Permission denied" errors

**Check your permissions:**

```bash
# See what account you're using
gcloud auth list

# Check your project
gcloud config get-value project

# Verify you have BigQuery access
gcloud projects get-iam-policy $(gcloud config get-value project) \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:$(gcloud config get-value account)"
```

**Request BigQuery permissions from your admin:**

-   `roles/bigquery.user`
-   `roles/bigquery.dataViewer`
-   `roles/bigquery.jobUser`

---

### Issue: "API not enabled"

```bash
# Enable BigQuery API
gcloud services enable bigquery.googleapis.com

# Enable other APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

---

## 🚀 Agent Issues

### Issue: Agents won't start

**Check ports are available:**

```bash
# See what's using the ports
lsof -i :8000
lsof -i :8001
lsof -i :8002
lsof -i :8003

# Kill processes if needed
kill -9 <PID>
```

**Check virtual environment:**

```bash
# Make sure venv is activated
source venv/bin/activate

# Verify Python version
python --version  # Should be 3.10+

# Reinstall dependencies if needed
pip install -r requirements.txt
```

---

### Issue: "Module not found" errors

```bash
# Activate venv
source venv/bin/activate

# Reinstall everything
pip install --upgrade -r requirements.txt

# Verify installation
pip list | grep google
```

---

### Issue: Agents start but immediately crash

**Check the logs:**

```bash
# View logs
tail -f logs/orchestrator_agent.log
tail -f logs/bigquery_agent.log
tail -f logs/ticket_agent.log
tail -f logs/maps_agent.log

# Check for errors
grep ERROR logs/*.log
```

**Common causes:**

1. Missing `.env` configuration
2. Invalid API keys
3. Missing authentication

---

## 🔧 Configuration Issues

### Issue: "Missing required environment variables"

**Check your .env file:**

```bash
# View current config (without showing secrets)
python3 check_config.py

# Or manually check
cat .env
```

**Required variables:**

-   `GOOGLE_API_KEY` - From https://aistudio.google.com/app/apikey
-   `GOOGLE_CLOUD_PROJECT` - Your GCP project ID

**Optional but recommended:**

-   Authentication via `gcloud auth application-default login`

---

### Issue: Can't edit .env file

```bash
# Check if file exists
ls -la .env

# Create from template if missing
cp .env.example .env

# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env
```

---

## 🌐 Network Issues

### Issue: "Connection refused" when calling agents

**Verify agents are running:**

```bash
# Check processes
ps aux | grep a2a_server

# Check if ports are listening
lsof -i :8000
netstat -an | grep 8000
```

**Test with curl:**

```bash
# Test orchestrator
curl http://localhost:8000/health

# Should return: {"status": "healthy", "agent": "Orchestrator Agent"}
```

---

### Issue: "Connection timeout" errors

**Check firewall:**

```bash
# macOS - check if Python is allowed
system_profiler SPFirewallDataType

# Temporarily disable firewall to test
# System Preferences → Security & Privacy → Firewall
```

**Try different host:**

```bash
# Edit a2a_server.py temporarily
# Change: uvicorn.run(app, host="0.0.0.0", port=port)
# To:     uvicorn.run(app, host="127.0.0.1", port=port)
```

---

## 💾 BigQuery Issues

### Issue: "Dataset not found"

```bash
# List your datasets
gcloud bigquery datasets list --project=YOUR_PROJECT_ID

# Create a test dataset
gcloud bigquery datasets create test_dataset \
  --location=US \
  --project=YOUR_PROJECT_ID
```

**Update .env:**

```env
BIGQUERY_DATASET=test_dataset
```

---

### Issue: "Query too expensive"

The agents have a 10GB billing limit by default for safety.

**To adjust:**

Edit `agents/bigquery_agent.py`:

```python
job_config = bigquery.QueryJobConfig(
    maximum_bytes_billed=100 * 1024 * 1024 * 1024  # 100 GB
)
```

---

## 🗺️ Maps Issues

### Issue: Maps agent returns mock data

This is expected! The Maps agent uses mock data by default.

**To enable real Maps API:**

1. Get a Maps API key: https://console.cloud.google.com/google/maps-apis
2. Add to `.env`:
    ```env
    MAPS_API_KEY=AIzaSy...your-maps-key
    ```
3. Restart agents

---

## 📦 Installation Issues

### Issue: "Python version too old"

```bash
# Check version
python3 --version

# Install Python 3.10+ via Homebrew
brew install python@3.11

# Use specific version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: "pip install fails"

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -v -r requirements.txt

# Try without cache
pip install --no-cache-dir -r requirements.txt
```

---

## 🧪 Testing Issues

### Issue: Tests fail

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/test_agents.py::TestTicketAgent::test_create_ticket -v
```

---

## 🐛 Still Having Issues?

### Collect debug information:

```bash
# System info
python --version
gcloud --version
which python
which gcloud

# Check auth status
gcloud auth list
gcloud config list

# Check environment
env | grep GOOGLE

# Check agent status
ps aux | grep a2a_server
lsof -i :8000-8003

# Check logs
ls -lh logs/
tail -20 logs/*.log
```

### Get help:

1. Check existing documentation:

    - `README.md`
    - `AUTHENTICATION.md`
    - `GET_CREDENTIALS.md`

2. Review logs in `logs/` directory

3. Try running with verbose output:
    ```bash
    python a2a_server.py --agent orchestrator --port 8000 2>&1 | tee debug.log
    ```

---

## 🔄 Nuclear Option: Clean Reinstall

If all else fails:

```bash
# Stop everything
./scripts/stop_all_agents.sh
pkill -f a2a_server

# Clean up
make clean
# or manually:
rm -rf venv/
rm -rf logs/*.log
find . -type d -name __pycache__ -exec rm -rf {} +

# Reinstall
./scripts/setup.sh

# Reconfigure
# Edit .env file with your credentials

# Restart
source venv/bin/activate
./scripts/start_all_agents.sh
```

---

## ✅ Verification Checklist

Before asking for help, verify:

-   [ ] Python 3.10+ installed: `python3 --version`
-   [ ] gcloud installed: `gcloud --version`
-   [ ] Authenticated: `gcloud auth list` shows active account
-   [ ] Project set: `gcloud config get-value project`
-   [ ] Virtual environment activated: `which python` shows venv path
-   [ ] Dependencies installed: `pip list | grep google`
-   [ ] .env file configured: `cat .env` shows your keys
-   [ ] Ports available: `lsof -i :8000` shows nothing or your agents
-   [ ] APIs enabled: BigQuery, AI Platform
-   [ ] Logs checked: `tail logs/*.log`

---

Good luck! 🚀
