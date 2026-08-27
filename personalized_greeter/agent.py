"""
Personalized Greeter - Demonstrates State Templating
Shows how {var} templating injects state values into instructions.

Reference: https://google.github.io/adk-docs/sessions/state.md
"""

from google.adk.agents.llm_agent import Agent

# Agent with state templating
root_agent = Agent(
    model='gemini-3.6-flash',
    name='personalized_greeter',
    # line 23 is conditional line that only appears if membership_tier exists
    instruction="""
    You are a friendly assistant.

    User information:
    - Name {user_name?there}
    - Preferred language: {preferred_language?English}
    - Membership: {membership_tier?free}

    {membership_tier?Your membership level is {membership_tier}}

    Greet the user warmly and offer assistance.
    Respond in {user_language?English}.
    """,
)
