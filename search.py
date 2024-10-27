import os
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun

# Set the GROQ_API_KEY if not already set
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual key

# Initialize Groq LLM and DuckDuckGo Search
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Step 1. Instantiating your TavilyClient
from tavily import TavilyClient


def query_tavily(query):
    """Perform a quick search using DuckDuckGo for immediate answers."""
    client = TavilyClient(api_key="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")
    response = client.search(query)
    return response

def query_llm(prompt, system_instruction=""):
    # Convert prompt to string
    prompt_str = str(prompt)
    # Optionally, you can use the system instruction if needed
    if system_instruction:
        prompt_str = f"{system_instruction}\n{prompt_str}"
    # Invoke the LLM with the converted string
    response = llm.invoke(prompt_str) 
    print(response.content) # Pass the string directly
    return response.content

