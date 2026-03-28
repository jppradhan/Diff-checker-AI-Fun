from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import certifi
from dotenv import load_dotenv
from pprint import pprint
import truststore
from pathlib import Path

truststore.inject_into_ssl()

# Load environment variables from .env file
load_dotenv()


# def configure_ssl_ca_bundle() -> None:
#     """Merge optional corporate CA with certifi bundle for outbound HTTPS clients."""
#     default_bundle_path = Path(certifi.where())
#     custom_ca_path = Path(os.getenv("CUSTOM_CA_CERT_PATH", "/app/certs/corporate-ca.pem"))

#     if not custom_ca_path.exists():
#         return

#     merged_bundle_path = Path("/tmp/ca-bundle-with-custom.pem")
#     merged_bundle_path.write_text(
#         default_bundle_path.read_text() + "\n" + custom_ca_path.read_text(),
#         encoding="utf-8",
#     )

#     merged_bundle = str(merged_bundle_path)
#     os.environ["SSL_CERT_FILE"] = merged_bundle
#     os.environ["REQUESTS_CA_BUNDLE"] = merged_bundle
#     os.environ["CURL_CA_BUNDLE"] = merged_bundle

#     certifi.where = lambda: merged_bundle  # type: ignore[assignment]


# configure_ssl_ca_bundle()

from app.models import AgentRequest, AgentResponse, HealthResponse, DiffRequest
from app.agent import draft_diff_agent, review_diff_agent
from app.middleware.rate_limit import RateLimitMiddleware
from app.tools import ALL_TOOLS
from langchain.messages import AIMessage, HumanMessage
from app.utils import parse_fenced_json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent API",
    description="Minimal LangChain Agent with Tools - FastAPI Boilerplate",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Agent API",
        "docs": "/docs",
        "available_tools": [tool.name for tool in ALL_TOOLS]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=os.getenv("APP_VERSION", "1.0.0"),
        model=os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
        available_tools=[tool.name for tool in ALL_TOOLS]
    )


@app.post("/check_diff_agent", response_model=AgentResponse)
async def check_diff_agent(request: DiffRequest):
    try:
        # Create the agent
        draft_agent = draft_diff_agent()
        draft_agent_result = draft_agent.invoke({
            "messages": [
                HumanMessage("Compare these two texts. Text 1: " + request.text1),
                HumanMessage("Text 2: " + request.text2),
            ]
        })
        
        # Invoke the agent with the user's message
        # result = agent.invoke({
        #     "messages": [{"role": "user", "content": request.message}]
        # })
        
        # Extract the response and tool usage
        messages = draft_agent_result.get("messages", [])

        draft_agent_response = ""

        last_message = messages[-1] if messages else None
        if last_message and hasattr(last_message, 'content'):
            draft_agent_response = last_message.content

        
        diff_agent = review_diff_agent()
        review_diff_agent_result = diff_agent.invoke({
            "messages": [
                HumanMessage("Here is the diff summary draft: " + draft_agent_response),
                HumanMessage("Text 1: " + request.text1),
                HumanMessage("Text 2: " + request.text2),
            ]
        })

        diff_agent_response = review_diff_agent_result.get("structured_response", {})
        pprint(diff_agent_response)

        return AgentResponse(
            response=diff_agent_response,
            tools_used=[],
            messages=[],
            more_context=draft_agent_response,
        )
        
    except Exception as e:
        logger.exception("Agent error")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List all available tools for the agent."""
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "args": tool.args
            }
            for tool in ALL_TOOLS
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("API_RELOAD", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO").lower()
    )
