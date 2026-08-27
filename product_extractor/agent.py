"""
Product extraction agent with structured JSON output.
Demonstrates ADK's output_schema with Pydantic BaseModel.
"""

from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field

root_agent = Agent(
    model='gemini-3.6-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
