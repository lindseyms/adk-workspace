"""
Simple Weather Agent
Demonstrates basic Agent Engine deployment.

Reference: https://google.github.io/adk-docs/
"""

from google.adk.agents import Agent

root_agent = Agent(
    model='gemini-3.5-flash',
    name='weather_agent',
    description='Provides weather information and forecasts.',
    instruction="""
    You are a helpful weather assistant.

    When users ask about weather:
    1. Ask for city if not provided
    2. Provide weather information (simulated for now)
    3. Be friendly and helpful

    Example response:
    "The current weather in San Francisco is 68°F (20°C) with partly cloudy skies."

    Note: In production, this would integrate with a real wether API.
    For this demo, provide simulated weather information.
    """
)