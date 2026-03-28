"""Agent creation using LangChain's create_agent."""
import os
from langchain.agents import create_agent
from app.tools import diff_checker
from app.models import ReviewResponse
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME"),
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    temperature=0.5,  # Lower temperature for more deterministic agent responses
    # max_output_tokens=2048,
)


def draft_diff_agent():
    system_prompt ="""You are a AI diff checker agent.
    You will be given two pieces of text and you need to analyze the differences between them.
    You should provide a clear and concise summary draft of the differences, including:
    - What was added, removed, or changed
    Rules:
    - Summary should not exceed 500 words
    """
    try:
        agent = create_agent(
            model=model,
            tools=[diff_checker],
            system_prompt=system_prompt
        )
    except Exception as e:
        print(f"Error creating draft diff agent: {e}")
        agent = None
    
    return agent


def review_diff_agent():
    system_prompt = """You are a AI agent to review a diff summary draft.
    You will be given a diff summary draft and the original two pieces of text.
    Your task is to review the diff summary draft and return the final diff summary in the following JSON format:
    {
        "added": [],
        "removed": [],
        "changed": []
    }
    """

    try:
        agent = create_agent(
            model=model,
            tools=[],
            system_prompt=system_prompt,
            response_format=ReviewResponse
        )
    except Exception as e:
        print(f"Error creating review diff agent: {e}")
        agent = None
    
    return agent
