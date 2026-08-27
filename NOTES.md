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
 -- OR --
1. Run the agent from the command line
    - adk run /path_to_agent
        - Good for:
            - Quick testing during development
            - Command-line workflows
            - Server environment without GUI
            - Automated testing scripts
            - CI/CD pipelines
        - Not for:
            - Presenting to stakeholders (use adk web instead)
            - Debugging complex conversations (use adk web instead)

## The development workflow
1. Edit agent.py - Define your agent's behavior
2. Run adk web - Test in the web interface
3. Iterate - Make changes, refresh, and test again

## Step 4 - Define your agent's identity
### 4 core paramerters
1. model (required)
    - underlying LLM that powers your agent's reasoning and decision-making
    - what it does
        - determines your agent's intelligence and capabilities
        - affects cost per request and response speed
        - different models have different strengths
2. name (required)
    - a unique string identifier for your agent
        - e.g. name='root_agent'
    - what it does
        - identifies your agent internally within ADK
        - Critcal in multi-agent systems where agents refer to each other
        - used for logging debugging, and agent delegation
    - naming conventions
        - use lowercase with underscores
        - be descriptive: data_analysis_agent, math_tutor_agent
        - avoid reserved names: user
        - dont use camelCase: use my_agent not myAgent
3. description (optional, recommended for multi-agent) - Helps other agents understand what it is
    - a concise summary of what your agent does
        - e.g. description='Answers user questions about the capital city of a given country.'
    - What this does:
        - used by other agents to deciside if they should route tasks to this agent
        - *helps in multi-agent systems where agents delegate to each other* - You should probably just add it
        - not used by the agent itself for its own behavior
    - Good description examples:
        - "Handles customer billing inquiries and processes payment updates"
        - "Analyzes sales data and generates weekly performance reports"
        - "Helps students learn algebra by guiding them through problem solving steps"
    - Bad description examples:
        - "Billing agent" (too vague)
        - "Helper" (not specific enough)
4. instruction (critical, but optional) - helps this agent understand what it is/its responsibilities
    - The behavioral blueprint that guides how your agent acts and responds
        - e.g. instruction="""You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose."""
    - What it does:
        - defines tha agent's personality and communication style
        - specifies the agent's core task or goal
        - sets boundaries and constraints on behavior
        - guides when and how to use tools
        - shapes the output format
        - *The most critical parameter for shaping an LlmAgent's behavior*
    - Tips for effective instructions
        - Be clear and specific: avoid ambiguity, clearly state the desired actions and outcomes
        - use markdown: improve readability for complex instructions using headings, lists, etc.
        - provide examples (few-shot): For complex tasks or specific output formats, include examples
        - Guide tool use: dont just list tools, explain when and why the agent should use them.
        - See customer_support_agent for example of well defined instructions!
        - The 4 key elements instruction parameter should define
            1) Core task
            2) personality
            3) constraints
            4) output format

### Additional Parameters
1. output_schema: Define a schema representing the desired agent output structure (pydantic). If set, the agent's final response must be a JSON string conforming to this schema
    - See an example in product_extractor
    - Use this if you dont want the response to be free form text
    - You MUST provide guidance in your agent instructions on the expected JSON format and structure, even though you provided the class definition in the output_schema arguemnt in the agent definition.
    - Tips:
        - Add descriptions to your pydantic fields. The LLM uses these to understand what the fields represent
        - The schema defines the EXACT output structure. The LLM will ONLY include fields you define in your Pydantic BaseModel. If you need nested objects like metadata, errors, or pagination in your output, you must explicitly define them all in the schema as you would any other field.
        
### The root agent
- ADK command line tools look for a python variable named root_agent as the *entry point* to your agent system. This is a convention that allows ADK to discover and run your agent. (The name parameter can be something else. This is used by the ADK internally)

## Configuring your model correctly -- Not using the default model
- Leaving the default model settings causes problems for systems such as:
    - No control over creativity vs consistency (temperature)
    - No safety thresholds configured
    - No token limits set
    - Same settings for all tasks (creative writing vs. data extraction)