"""
Model configuration demo showing factual vs creative optimization.
Demonstrates ADK's generate_content_config with different settings.
"""

from google.adk.agents.llm_agent import Agent
from google.genai import types

# Agent 1: Optimized for Factual Data Extraction
# Uses low temperature for consistecy, strict safety for accuracy
factual_agent = Agent(
    model="gemini-3.5-flash",   #Flash is sufficient for extraction
    name="data_extractor",
    description="Extracts factual information with high consistency",
    instruction="""You are a precise data extractor.
    Extract facts exactly as stated. Do not:
    - Add information not presented in the input
    - Make assumptions or inferences
    - Use creative language

    Be accurate, concise, and deterministic.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very Low temperature for consistency
        max_output_tokens=500,
        top_p=0.8,
        top_k=10,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
            )
        ]
    )
)

root_agent = Agent(
    model='<FILL_IN_MODEL>',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
