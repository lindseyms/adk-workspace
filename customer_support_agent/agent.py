"""
Professional customer support agent with structured instructions.
Demonstrates ADK best practices for instruction writing.

Reference: https://google.github.io/adk-docs/agents/llm-agents/
"""

from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.6-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
