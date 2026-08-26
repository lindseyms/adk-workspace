from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    # Model (required): The reasoning engine)
    model='gemini-2.5-flash',
    # Name (required) - Identity: Required identifier
    name='math_tutor_agent',
    # Purpose: What it does - used by other internal agents to determine how to interact with it
    description='Helps students learn algebra by guiding them through problem-solving steps.',
    # Instruction: How the agent should behave
    instruction='You are a helpful assistant.'
    # Tools: Functions the agent calls to take action
    # Orchestration: Handled automatically by the Agent class - The Perceive -> Think -> Act -> Check loop
)
