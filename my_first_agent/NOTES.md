## Step 1
1. Create the project by running (Think of this like Spring Initializr)
    - adk create your_project_name
        - This creates:
            your_project_name/
            |--- agent.py           # Main agent code (you'll edit this)
            |--- __init__.py        # Python package initialization
            |___ .env               # Environment variables (you'll edit this)
    - Understanding the files
        - agent.py: This is where you'll define your agent using Python code. This file brings together the model, tools and orchestration components. It contains your root_agent definition
        - __init__.py: Python package initialization file that imports your agent module. This is required for ADK to discover your agent
        - .env: A special file for storing sensitive info like API keys. ADK automatically loads this file, keeping secrets out of your code.