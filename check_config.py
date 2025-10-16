#!/usr/bin/env python3
"""Check if all required configuration is set."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("🔍 Checking Configuration...")
print("=" * 50)

required = {
    "GOOGLE_API_KEY": "Gemini API Key",
    "GOOGLE_CLOUD_PROJECT": "Google Cloud Project ID",
}

optional = {
    "GOOGLE_APPLICATION_CREDENTIALS": "Service Account JSON (for BigQuery)",
    "BIGQUERY_DATASET": "BigQuery Dataset",
    "MAPS_API_KEY": "Google Maps API Key",
}

all_good = True

print("\n✅ Required Configuration:")
for key, description in required.items():
    value = os.getenv(key)
    if value and value != f"your-{key.lower().replace('_', '-')}":
        print(f"  ✓ {description}: {'*' * 10}{value[-4:]}")
    else:
        print(f"  ✗ {description}: NOT SET")
        all_good = False

print("\n⚙️  Optional Configuration:")
for key, description in optional.items():
    value = os.getenv(key)
    if value and value != f"your-{key.lower().replace('_', '-')}":
        if key == "GOOGLE_APPLICATION_CREDENTIALS" and value:
            exists = Path(value).exists()
            status = "EXISTS" if exists else "FILE NOT FOUND"
            print(f"  ✓ {description}: {status}")
            if not exists:
                all_good = False
        else:
            print(f"  ✓ {description}: SET")
    else:
        print(f"  - {description}: Not set (optional)")

print("\n" + "=" * 50)
if all_good:
    print("✅ All required configuration is set!")
    print("\nYou can now run:")
    print("  ./scripts/setup.sh")
    print("  source venv/bin/activate")
    print("  ./scripts/start_all_agents.sh")
else:
    print("⚠️  Please configure missing items in .env file")
    print("\nTo get your credentials:")
    print("  1. Gemini API: https://aistudio.google.com/app/apikey")
    print("  2. Cloud Project: https://console.cloud.google.com")
    print("  3. Service Account: Cloud Console → IAM → Service Accounts")

