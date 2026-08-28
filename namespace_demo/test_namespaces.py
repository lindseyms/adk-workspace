"""
Test state namespaces to see persistence differences.
Run with: python test_namespaces.py
"""

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Setup
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name="namespace_demo_app",
    user_id="user1",
    session_id="session1"
)

runner = Runner(
    agent=root_agent,
    app_name="namespace_demo_app",
    session_service=session_service
)

# Set all four namespace types
print("=== Setting state in all namespaces ===")
session.state["app:name"] = "Namespace Demo"
session.state["app:version"] = "2.0"
session.state["user:theme"] = "dark"
session.state["topic"] = "state management"
session.state["temp:step"] = "initialization"

print(f"State before run: {session.state}\n")

# Run agent
print("=== Running agent (Turn 1) ===")
result = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Show me the namespace values")])
)

# Show response
for event in result:
    if event.is_final_response():
        print(f"Agent response:\n{event.content.parts[0].text}\n")
    
# Check state after turn
print("=== State after Turn 1 ===")
print(f"Full state: {session.state}")
print(f"temp:step: {session.state.get('temp:step')}") # Should be GONE
print(f"topic: {session.state.get('topic')}") # Should persist
print(f"user:theme: {session.state.get('user:theme')}") # Should persist
print(f"app:version: {session.state.get('app:version')}") # Should persist

print("\n=== Simulating Turn 2 ===")

result2 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Check state again")])
)

for event in result2:
    if event.is_final_response():
        print(f"Agent response:\n{event.content.parts[0].text}\n")

print("=== State after Turn 2 ===")
print(f"Full state: {session.state}")
print(f"temp:step: {session.state.get('temp:step')}") # Still GONE
print(f"topic: {session.state.get('topic')}") # Still here (session state)
print(f"user:theme: {session.state.get('user:theme')}") # Still here (user state)

# Simulate new session
print("\n=== Simulating NEW Session (session2)===")
session2 = session_service.create_session(
    app_name="namespace_demo_app",
    user_id="user1", # Same user
    session_id="session2" # Different session
)

print(f"New session state: {session2.state}")
print(f"topic: {session2.state.get('topic')}") # Should be GONE (session-scoped)
print(f"user:theme: {session2.state.get('user:theme')}") # Should PERSIST (user-scoped)
print(f"app:version: {session2.state.get('app:version')}") # Should PERSIST (app-scoped)
