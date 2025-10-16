# Authentication Guide

## 🔐 Secure Authentication (Recommended)

Your organization has disabled service account key creation for security. This is great! Here's the **more secure alternative**:

### Application Default Credentials (ADC)

This method uses your own Google Cloud credentials instead of a service account key file.

#### Prerequisites

1. **Install Google Cloud SDK** (if not already installed):
   ```bash
   # On macOS
   brew install google-cloud-sdk
   
   # On Linux
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   
   # On Windows
   # Download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Verify installation**:
   ```bash
   gcloud --version
   ```

#### Setup Steps

1. **Authenticate with your Google account**:
   ```bash
   gcloud auth login
   ```
   This will open a browser window - sign in with your Google account.

2. **Set your default project**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```
   Replace `YOUR_PROJECT_ID` with your actual project ID.

3. **Create Application Default Credentials**:
   ```bash
   gcloud auth application-default login
   ```
   This will open another browser window and create credentials that the agents will use.

4. **Update your .env file**:
   ```bash
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_API_KEY=your-gemini-api-key
   # Leave GOOGLE_APPLICATION_CREDENTIALS empty or commented out
   ```

5. **Verify your setup**:
   ```bash
   python3 check_config.py
   ```

#### What This Does

- ✅ Uses **your** Google Cloud credentials
- ✅ No service account key files to manage
- ✅ More secure - credentials expire automatically
- ✅ Works with all your existing permissions
- ✅ No organization policy conflicts

#### Required Permissions

Make sure your Google account has these roles in the project:
- **BigQuery User** (roles/bigquery.user)
- **BigQuery Data Viewer** (roles/bigquery.dataViewer)
- **BigQuery Job User** (roles/bigquery.jobUser)

Ask your project admin to grant these if you don't have them.

---

## 🔑 Alternative: Service Account Key (If Allowed)

If your organization allows service account keys OR you need to use one anyway:

1. **Request Policy Exemption**:
   - Contact your Organization Policy Administrator
   - Reference tracking number: `c4853793317159548`
   - They need role: `roles/orgpolicy.policyAdmin`
   - They must disable: `iam.disableServiceAccountKeyCreation`

2. **Create Service Account Key**:
   - Follow the original instructions in `GET_CREDENTIALS.md`
   - Download the JSON key file
   - Set in `.env`:
     ```bash
     GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
     ```

---

## 🚀 Quick Start (Using ADC)

```bash
# 1. Install gcloud SDK
brew install google-cloud-sdk

# 2. Login to Google Cloud
gcloud auth login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Setup application default credentials
gcloud auth application-default login

# 5. Verify permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:YOUR_EMAIL"

# 6. Setup the project
./scripts/setup.sh

# 7. Edit .env file (add GOOGLE_API_KEY and GOOGLE_CLOUD_PROJECT)

# 8. Start agents
source venv/bin/activate
./scripts/start_all_agents.sh
```

---

## 🐛 Troubleshooting

### "ADC not found" error
```bash
# Re-run this command:
gcloud auth application-default login
```

### "Permission denied" errors
```bash
# Check your permissions:
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:$(gcloud config get-value account)"

# Request BigQuery roles from your admin
```

### "API not enabled" errors
```bash
# Enable required APIs:
gcloud services enable bigquery.googleapis.com
gcloud services enable bigquerystorage.googleapis.com
```

### "quota exceeded" errors
```bash
# Check your quota:
gcloud compute project-info describe --project=YOUR_PROJECT_ID
```

---

## 🔒 Security Best Practices

With ADC:
- ✅ Credentials automatically expire
- ✅ No credential files to secure
- ✅ Uses your existing permissions
- ✅ Audit trail tied to your account
- ✅ Can be revoked instantly

With Service Account Keys (if you must use them):
- ⚠️ Rotate keys every 90 days
- ⚠️ Never commit keys to git
- ⚠️ Use Secret Manager in production
- ⚠️ Monitor key usage
- ⚠️ Delete unused keys

---

## 📚 Additional Resources

- [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)
- [gcloud auth commands](https://cloud.google.com/sdk/gcloud/reference/auth)
- [BigQuery IAM roles](https://cloud.google.com/bigquery/docs/access-control)
- [Organization Policies](https://cloud.google.com/resource-manager/docs/organization-policy/overview)

---

## ✅ Verify Authentication

After setup, test authentication:

```bash
# Test gcloud authentication
gcloud auth list

# Test ADC
python3 << EOF
from google.cloud import bigquery
client = bigquery.Client()
print("✅ Authentication successful!")
print(f"Project: {client.project}")
EOF
```

If you see your project name, you're all set! 🎉

