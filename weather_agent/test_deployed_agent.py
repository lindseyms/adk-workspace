"""
Test Deployed Weather Agent
"""
import os
from google.cloud import aiplatform

# Initialize
aiplatform.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)

# Connect to deployed agent (REPLACE WITH YOUR RESOURCE NAME - get this from your local console output after successful deployment)
resource_name = "projects/801299566055/locations/us-central1/reasoningEngines/1107768410344783872"
remote_app = aiplatform.ReasoningEngine(resource_name=resource_name)

# Test query 1
print("=" * 60)
print("Test 1: Weather query")
print("=" * 60)
response = remote_app.query("What's the weather in San Francisco?")
print(f"Agent response: {response}")
print()

# Test query 2
print("=" * 60)
print("Test 2: Weather forecast")
print("=" * 60)
response2 = remote_app.query("Will it rain tomorrow in Seattle?")
print(f"Agent response: {response2}")
print()

print("=" * 60)
print("✔️ Deployed agent working successfully.")
print("=" * 60)