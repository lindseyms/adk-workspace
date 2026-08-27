"""
Product extraction agent with structured JSON output.
Demonstrates ADK's output_schema with Pydantic BaseModel.
"""

from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field

# Step 1: Define the output structure with Pydantic
class ProductInfo(BaseModel):
    product_name: str = Field(description="The full name of the product")
    price: float = Field(description="The price in USD")
    storage: str = Field(description="Storage capacity (e.g., '256GB')")
    color: str = Field(default="Not specified", description="Product color if mentioned")

root_agent = Agent(
    model='gemini-3.6-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)
