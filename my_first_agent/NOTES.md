## Concepts
1. Model
    - Your .env file configures access to Gemini
    - Gemini is the LLM that provides reasoning and decision-making
    - This is the "brain" that understands language and makes choices
2. Tools (coming in module 3)
    - Functions your agent can call to take actions
    - Examples: search the web, read files, and send emails
    - These bridge "knowing" to "doing"
3. Orchestration (provided by ADK)
    - The framework that runs the agent loop
    - Manages: Perceive -> think -> act -> check -> repeat
    
## Step 1 - Environment Set Up
1. Verify python installation
    - python --version
2. Create a workspace directory for your adk projects
    - mkdir adk-workspace
    - cd adk-workspace
3. Create a virtual environment & activate it
    - python -m venv .venv
    - source .venv/bin/activate (Linux) OR .venv\Scripts\Activate.ps1 (Powershell) OR .venv\Scripts\activate.bat (Command Prompt)
4. Install ADK within virtual environment
    - pip install google-adk
        - this installs:
            - ADK framework with agent abstractions (LlmAgent, Runner, etc.)
            - CLI tools (adk command)
            - Dependencies for working with Google's Gemini models
5. Get API key in Google AI Studio
    - add the key to env file

## Step 2 - Create the project
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
    - How the files fit together
        - agent.py -> Where everything connects
            - The model is defined, named, behavior is described, tools are referenced, and orchestration (this occurs automatically by the agent class -- The Perceive -> Think -> Act -> Check loop)
        - .env -> Secure credentials
            - Keeps API keys out of code, automatically loaded by ADK, never committed to Git
        - __init__.py -> Package initialization
            - Makes your folder a Python package, imports your agent module, Required for ADK to discover agents.
## Step 3 - Verify setup
1. Start ADK web interface
    - adk web
2. Navigate to http://localhost:8000

## The development workflow
1. Edit agent.py - Define your agent's behavior
2. Run adk web - Test in the web interface
3. Iterate - Make changes, refresh, and test again
