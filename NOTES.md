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
2. output_key: used to store the result of output_schema in the session state. useful for passing data between agents, simple value extraction.
3. generate_content_config: Pass an instance of google.genai.types.GenerateContentConfig to control parameters like temperature (randomness), max_output_tokens (response length), top_p, top_k, and safety settings
    - Parameters:
        - **Temperature**: controls randomness in model output
            - Low temperature (0.0-0.3) - deterministic. Use for data extraction, etc.
            - Medium temperature (0.4-0.7) - balanced. Use for customer support, tutoring, general conversations
            - High temperature (0.8-1.0) - creative. Use for: creative writing, brainstorming, marketing copy
        - **Safety settings**: configure content filtering thresholds for Gemini models
            - Safety thresholds
                - BLOCK_NONE - No filtering (not recommended in prod)
                - BLOCK_ONLY_HIGH - Block only high-probablity harmful content
                - BLOCK_MEDIUM_AND_ABOVE - Block medium and high probablity
                - BLOCK_LOW_AND_ABOVE - Most strict, blocks even low probablity
        - **Output tokens and sampling**: control response length and diversity
            - max_output_tokens: Maximum response length (defualt varies by model)
            - top_p: Nucleus sampling -- consider tokens comprising top P% of probablity
            - top_k: Only sample from the K most likely next tokens
    - **Example**: See model_comparison 
4. planner: Assign a BasePlanner instance to enable multi-step reasoning and planning before execution. BuiltInPlanner: Leverages the model's built-in planning capabilities (e.g., Gemini's thinking feature)
    - Parameters
        - **thinking_budget**: determines how deeply the model can think. Guides model on number of thinking tokens to use when generating a response.
            - Higher values (e.g. 2048) allow more thorough analysis for complex problems.
            - Lower values (e.g. 512) are faster for simpler tasks
        - **include_thoughts**: lets you see (and debug) the reasoning process. Controls whether the model should include raw thoughts and internal reasoning process in the response.
    - Choosing b/n planners
        - BuiltInPlanner (recommended for Gemini models)
            - leverages the model's native thinking capabilities
            - best for
                - Gemini models with built in thinking support
                - Transparent reasoning: see internal though process with include_thoughts=True
                - flexible control: adjust reasoning depth with thinking_budget
        - PlanReActPlanner (For non-gemini models)
            - best for
                - Non-Gemini models, and/or models without native thinking capabilites
                - structured output format: Enforces Planning -> Action -> reasoning -> Final answer
                - tool heavy workflows: explicit action/reasoning phases work well with tool calls
                - enforcing systematic approach: when you need guaranteed output structure
    - **Example**: See problem_solver
5. tools: provide a list of tools the agent can use.
    - Each item in the list can be:
        - A native function or method (wrapped as a FunctionTool)
            - ADK automatically wraps Python functions as FunctionTool
        - An instance of a class inheriting from BaseTool
        - An instance of another agent (AgentTool)
        
### The root agent
- ADK command line tools look for a python variable named root_agent as the *entry point* to your agent system. This is a convention that allows ADK to discover and run your agent. (The name parameter can be something else. This is used by the ADK internally)

## Configuring your model correctly -- Not using the default model
- Leaving the default model settings causes problems for systems such as:
    - No control over creativity vs consistency (temperature)
    - No safety thresholds configured
    - No token limits set
    - Same settings for all tasks (creative writing vs. data extraction)

### Choosing the correct model
- Gemini 2.5 Pro
    - start here for prototyping and establishing quality baselines
    - excellent reasoning for complex analysis and quality-critical tasks
    - 2M token context window for larger inputs
    - Best for initial development and evaluation
- Gemini 2.5 Flash
    - Switch to this model after initial prototyping. Cost and speed are improved.
    - ~2x faster response times
    - ~10x cheaper than pro
    - 1M token context window
    - Good reasoning for most straightforward tasks
    - Ideal for high-volume production workloads
    - Tip: Always perform gap analysis after switching from Pro to Flash to ensure Flash meets your quality requirements

## Reactive vs Thoughtful Agents
- Use reactive agents (agents that respond quickly) for simple problems that don't need planning
    - Direct factual questions ("What is the capital of France?")
    - Single calculations ("Convert 100 USD to EUR")
    - Straightforward tasks ("Greet the user warmly")
- Use thoughtful agents (agents that respond slowly and plan) for complex problems that require multiple considerations, trade-off analysis, or sequential reasoning:
    - Business strategy ("How can i reduce cloud costs by 30% without impacting performance?" - Requires analyzing cost drivers, perf requirements, and creating a phased approach)
    - Technical decisions ("Should I use microservices or monolithic architecture for my startup MVP?" - Requires weighing trade-offs: speed vs. scalability, team size, future growth)
    - Multi-step planning ("Plan a 2-week Japan trip for a family of 4 on a budget of $5000" - Requires coordinating flights, hotels, activities, meals--all within budget constraints)
    - **Without planning, agents struggle with multi-step reasoning**
- Planning vs multi-agent
    - Use planning when a single agent needs to reason through multiple steps or trade-ffs within their domain. Use multiple agents when the problem requires distinct specialized skills that should be divided among separate agents.

## Session State
- A collection (dict or map) holding key-value pairs.
- Used to allow your code to check values/make programmatic decisions based on conversation data such as:
    - Personalize interaction: Remember user preferences mentioned earlier (e.g., 'user_preference_theme': 'dark')
    - Track task progress: keep tabs on steps in a multi-turn process (e.g. 'booking_step': 'confirm_payment')
    - accumulate information: Build lists or summaries (e.g., 'shopping_cart_items': ['book', 'pen'])
    - Make informed decisions: Store flags or values influencing the next response (e.g., 'user_is_authenticated': True)
- accessible through session.state attribute
- Do not use this for only providing contet to LLM (conversation history does this already)
- Save responses with output_key in the agent definition
- **Example**: name_extractor
- Common pattern
    1) Agent saves to state with output_key
        ```python
        agent=Agent(..., output_key="result")
        ```
    2) Run agent
        ```python
        runner.run(...)
        ```
    3) Access state programmatically
        ```python
        if session.state.get("result"):
            # Make decisions based on state
            pass
        ```
- Templating can also be used to pass information in to the instructions to make instructions dynamic.
    - **Example**: personalized_greeter
    - Optional syntax prevents errors:
        - {var} -> Errors if missing (Strict mode)
        - {var?} -> Empty if missing (Optional mode)
        - {var?default} -> Uses default text if missing
        - {var?Conditional text} -> Shows text only if var exists
    - Common Pattern
        1) State is ste (from previous turn or external data)
            ```python
            session.state["user_name"] = "Alex"
            ```
        2) Agent uses templating
            ```python
            agent=Agent(
                ...,
                instruction="Hello {user_name?there}"
            )
            ```
        3) Instruction resolves automatically
            - LLM receives: "Hello Alex"

## Tools
- LLM handles reasoning and decision making. Tools handle action and data retrieval
- Tools enable
    - Access real-time info: web search, weather APIs, stock prices
    - perform calculations: execute code, run financial models, process data
    - query databases: retrieve customer orders, product inventory, user profiles
    - interact with external systems: send emails, book appts, process payments
    - take actions in the world: update records, trigger workflows, control devices
- The process
    1) Reasoning: The agent's LLM analyzes its system instruction, conversation hisotry and user request
    2) Selection: Based on the analysis, the LLM decides on which tool, if any, to execute, based on the tools available to the agent and the docstrings that describe each tool
    3) Invocation: The LLM generates the required arguments (inputs) for the selected tool and triggers its execution
    4) Observation: The agent receives the output (result) returned by the tool
    5) Finalization: The agent incorporates the tool's output into its ongoing reasoning process to formulate the next repsonse, decide on subsequent step, or determine if the goal has been acheived.
    - **example**
        - User asks "What's the weather in Paris?"
            |
            v
        - Step 1 - Reasoning: Agent analyzes: "User needs current weather data for Paris"
            |
            V
        - Step 2 - Selection: Agent decides: "get_weather tool matches this need"
            |
            V
        - Step 3 - Invocation: Agent calls: get_weather(city="Paris")
            |
            V
        - Step 4 - Observation: Tool returns: {"status": "success", "report": "Paris is sunny, 20 C"}
            |
            V
        - Step 5 - Finalization: Agent responds: "The current weather in Paris is sunny with a temperature of 20 C"
- Tool types in ADK
    - Function tools: Tools created by you
    - Built-in tools: Ready to use tools provided by the framework for common tasks (Google Search, Code Execution, Retrieval Augemented Generation (RAG))
    - Third-Party tools: Integrate tools seamlessly from popular external libraries.
- Function name, docstring, and params guide LLM decision on which tool to use
- **Example**: geography_assistant
- Agent behavior:
    - Tools are only called when needed. Agent uses reasoning to determine tool necessity. Not every query requires a tool.
    - Tools are optional - agnets call tools only when reasoning determines them necessary
    - multiple calls possible - agents can call the same tool multiple times
    - Error handling - tools should return clear error messages for failure cases
- Best practices:
    - Descriptive function names
    - Clear docstrings - explain what the tool does and when to use it
    - Type hints - Help ADK generate proper schema for the LLM
    - Simple return values - Start with basic types before complex structures

# Todo
1) Look up ADK agent loop and understand this