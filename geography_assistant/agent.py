"""
Geography Assistant Agent
Demonstrates ADK's tools parameter with a simple custom function tool.

Reference: https://google.github.io/adk-docs/agents/llm-agents#tools
"""

from google.adk.agents.llm_agent import Agent

# Step 1: Define a tool function
def get_capital_city(country: str) -> str:
    """Retrieves the capital city for a specified country.

    Args:
        country (str): The name of the country.

    Returns:
        str: The capital city or error message..
    """
    # Simulated capital city database
    capitals = {
        "france": "Paris",
        "japan": "Tokyo",
        "canada": "Ottawa",
        "germany": "Berlin",
        "brazil": "Brasília",
        "australia": "Canberra",
        "italy": "Rome",
        "mexico": "Mexico City"
    }

    # Look up the capitals
    return capitals.get(
        country.lower(),
        f"Sorry, I don't have information about the capital of {country}.")

# Step 2: Create agent with the tool
root_agent = Agent(
    model='gemini-3.5-flash',
    name='geography_assistant',
    description='Helps users learn about world geography.',
    instruction="""
    You are a geography assistant that helps users learn about world capitals.

    When a user asks about a capital city:
    1. Use the get_capital_city tool to find the answer
    2. Provide the information in a friendly, educational way
    3. You can add interesting facts if you know them

    If the tool returns an error message, politely tell the user you don't have that information.
    """,
    tools=[get_capital_city]    # Provide a function as a tool
)
