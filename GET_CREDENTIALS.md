# How to Get Google Cloud Credentials

## 🔑 1. GOOGLE_API_KEY (Gemini API)

**What it's for**: Powers the AI agents with Gemini models

**How to get it**:
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key
5. Add to `.env`:
   ```
   GOOGLE_API_KEY=AIzaSy...your-key-here
   ```

**Cost**: Free tier available (60 requests per minute)

---

## 📦 2. GOOGLE_CLOUD_PROJECT

**What it's for**: Your Google Cloud project identifier

**How to get it**:
1. Go to: https://console.cloud.google.com
2. Click "Select a project" dropdown at the top
3. Click **"NEW PROJECT"** or select existing
4. If creating new:
   - Name: `adk-agents` (or your choice)
   - Click **"CREATE"**
5. Copy the **Project ID** (not the name)
6. Add to `.env`:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id-12345
   ```

---

## 🔐 3. GOOGLE_APPLICATION_CREDENTIALS (Service Account)

**What it's for**: Authentication for BigQuery and other Google Cloud services

**How to get it**:

### Step 1: Go to Service Accounts
- Visit: https://console.cloud.google.com/iam-admin/serviceaccounts
- Select your project

### Step 2: Create Service Account
- Click **"+ CREATE SERVICE ACCOUNT"**
- **Service account name**: `adk-agent-service-account`
- **Service account ID**: Will auto-populate
- **Description**: `Service account for ADK A2A multi-agent system`
- Click **"CREATE AND CONTINUE"**

### Step 3: Grant Permissions
Add these roles:
- ✓ **BigQuery User**
- ✓ **BigQuery Data Viewer** 
- ✓ **BigQuery Job User**

Click **"CONTINUE"** → **"DONE"**

### Step 4: Create JSON Key
- Find your service account in the list
- Click the **email address** to open it
- Go to **"KEYS"** tab
- Click **"ADD KEY"** → **"Create new key"**
- Select **"JSON"** format
- Click **"CREATE"**
- **File downloads automatically** (e.g., `project-name-abc123.json`)

### Step 5: Save the File
```bash
# Move the downloaded file to the credentials directory
mv ~/Downloads/your-project-*.json /Users/kevinjones/google/credentials/service-account-key.json
```

### Step 6: Update .env
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/kevinjones/google/credentials/service-account-key.json
```

**Security Notes**:
- ⚠️ Keep this file secure - it's like a password
- ✓ The `credentials/` directory is in .gitignore
- ✓ Never commit this file to version control

---

## 🗺️ 4. MAPS_API_KEY (Optional)

**What it's for**: Real geocoding and maps functionality (Maps Agent uses mock data without it)

**How to get it**:

### Step 1: Enable Maps APIs
1. Go to: https://console.cloud.google.com/apis/library
2. Search for and enable:
   - **Maps JavaScript API**
   - **Geocoding API**
   - **Directions API**
   - **Distance Matrix API**
   - **Places API**

### Step 2: Create API Key
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click **"+ CREATE CREDENTIALS"** → **"API key"**
3. Copy the key
4. (Optional) Click **"RESTRICT KEY"** and limit to Maps APIs only

### Step 3: Add to .env
```bash
MAPS_API_KEY=AIzaSy...your-maps-key-here
```

**Cost**: 
- $200 free monthly credit
- Pay-as-you-go after that
- See: https://mapsplatform.google.com/pricing/

---

## 📊 5. BIGQUERY_DATASET (Optional)

**What it's for**: Default dataset for BigQuery queries

**How to get it**:

If you already have a BigQuery dataset:
```bash
BIGQUERY_DATASET=your_dataset_name
```

To create a new dataset:
1. Go to: https://console.cloud.google.com/bigquery
2. Click your project name
3. Click **"CREATE DATASET"**
4. Enter:
   - **Dataset ID**: `adk_test_dataset`
   - **Location**: `US` (or your preferred region)
5. Click **"CREATE DATASET"**
6. Add to `.env`:
   ```bash
   BIGQUERY_DATASET=adk_test_dataset
   ```

---

## ✅ Verify Your Setup

After setting up your credentials, run:

```bash
python3 check_config.py
```

This will verify all your credentials are configured correctly.

---

## 🚀 Next Steps

Once you have at minimum:
- ✓ GOOGLE_API_KEY
- ✓ GOOGLE_CLOUD_PROJECT

You can run:

```bash
# Setup the project
./scripts/setup.sh

# Start the agents
source venv/bin/activate
./scripts/start_all_agents.sh
```

The BigQuery agent will work in limited mode without `GOOGLE_APPLICATION_CREDENTIALS`, and the Maps agent will use mock data without `MAPS_API_KEY`.

---

## 💰 Costs

- **Gemini API**: Free tier available
- **BigQuery**: 
  - First 1 TB of queries per month: FREE
  - Storage: First 10 GB: FREE
- **Maps API**: $200/month free credit
- **Service Account**: FREE

---

## 🆘 Troubleshooting

### "Permission denied" errors
- Make sure service account has the correct roles
- Wait a few minutes for permissions to propagate

### "API not enabled" errors
- Enable the required APIs in Cloud Console
- Go to APIs & Services → Enable APIs

### "Invalid credentials" errors
- Check the JSON file path is correct
- Ensure the file is valid JSON
- Verify the service account still exists

### Need help?
- Check the logs in `logs/` directory
- Read `README.md` for more details
- Visit Google Cloud documentation: https://cloud.google.com/docs


