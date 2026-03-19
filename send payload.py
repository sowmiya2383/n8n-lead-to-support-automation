import requests
import json
import os

webhook_url = "https://sowmiya23.app.n8n.cloud/webhook/lead-webhook"
payloads_folder = "sample payloads"

for filename in os.listdir(payloads_folder):
    if filename.endswith('.json'):
        with open(os.path.join(payloads_folder, filename), 'r') as f:
            payload = json.load(f)
        print(f"Testing {filename}...")
        response = requests.post(webhook_url, json=payload)
        print(f"Status: {response.status_code}")
        print("---")
