# Credentials Directory

Place your Google Cloud service account JSON key file here.

## Steps:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Create a service account with BigQuery roles
3. Download the JSON key
4. Save it here as `service-account-key.json`
5. Update `.env` file:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/Users/kevinjones/google/credentials/service-account-key.json
   ```

⚠️ **Security Note**: This directory is in .gitignore - credentials won't be committed to git.

