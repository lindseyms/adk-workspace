"""
Customer Support Agent with Coordinated Tools
Demonstrates strategic tool combination, error handling, and agent-as-tool pattern.

Reference: https://google.github.io/adk-docs/tools-custom/
"""

from google.adk.agents import Agent

# Simulated database
ORDERS_DB = {
 "ORD123": {"status": "shipped", "total": 99.99, "customer": "john@email.com"},
 "ORD456": {"status": "processing", "total": 149.99, "customer":
"jane@email.com"},
 "ORD789": {"status": "delivered", "total": 249.99, "customer": "bob@email.com"},
}

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
