"""
Test state templating with different state values.
Run with: python test_templating.py
"""
import asyncio

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Setup
session_service = InMemorySessionService()
session = asyncio.run(session_service.create_session(
    app_name="greeter_app",
    user_id="user1",
    session_id="session1"
))

runner = Runner(
    agent=root_agent,
    app_name="greeter_app",
    session_service=session_service
)

# Test 1: No state set (all defaults)
print("=== Test 1: No state set (all defaults) ===")
result1 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Hello")])
)

for event in result1:
    if event.is_final_response():
        print(f"Agent: {event.content.parts[0].text}\n")

# Test 2: State user name only
print("=== Test 2: State user name only ===")
session.state["user_name"] = "Alex"
result2 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Hello again")])
)

for event in result2:
    if event.is_final_response():
        print(f"Agent: {event.content.parts[0].text}\n")

# Test 3: State all state values
print("=== Test 3: State all state values ===")
session.state["user_name"] = "Alex"
session.state["user_language"] = "Spanish"
session.state["membership_tier"] = "premium"

result3 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Hola de nuevo")])
)

for event in result3:
    if event.is_final_response():
        print(f"Agent: {event.content.parts[0].text}\n")

print("=== Current state ===")
print(session.state)