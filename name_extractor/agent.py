"""
Name Extractor - Demonstrates Session State Basics
Shows how to use output_key to save data and access it via session.state.
"""

from google.adk.agents.llm_agent import Agent

# Single agent that extracts and saves name
root_agent = Agent(
    model='gemini-3.6-flash',
    name='name_extractor',
    description="Extracts a person's name from the message.",
    instruction="Extract the person's name from the message. Return ONLY the name, nothing else.",
    output_key="user_name" # Automatically saves response to state["user_name"]. After the agent runs, state["user_name"] will contain the extracted name. No manual state management code needed.
)
