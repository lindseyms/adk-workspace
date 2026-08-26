from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',                                           # Model (required): The reasoning engine)
    name='root_agent',                                                  # Name (required) - Identity: Required identifier
    description='A helpful assistant for user questions.',              # Purpose: What to act
    instruction='You are a helpful assistant.'                          # Instruction: How the agent should behave
                                                                        # Tools: Functions the agent calls to take action
                                                                        # Orchestration: Handled automatically by the Agent class - The Perceive -> Think -> Act -> Check loop
)
