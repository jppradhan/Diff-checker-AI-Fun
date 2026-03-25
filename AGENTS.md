# AI Agent Architecture

## Overview

**AI Diff Checker** implements a **two-stage LangChain agent pipeline** integrated with **FastAPI** for intelligent text diffing. The agents work collaboratively to analyze differences between texts and provide structured, human-readable output.

- **Framework**: LangChain + LangGraph
- **API Server**: FastAPI
- **Model Support**: OpenAI, Anthropic, Google, AWS, Mistral, Groq, Cohere
- **Python Version**: 3.11+

## High-Level Architecture

```
User Input (text1, text2)
        ↓
┌───────────────────────────────┐
│  Stage 1: Draft Diff Agent    │
│  - Analyze differences         │
│  - Use diff_checker tool       │
│  - Generate summary            │
└───────────────────────────────┘
        ↓ (draft summary)
┌───────────────────────────────┐
│ Stage 2: Review Diff Agent    │
│  - Review draft summary        │
│  - Validate against originals  │
│  - Categorize differences      │
└───────────────────────────────┘
        ↓
    JSON Output
    {
      "added": [...],
      "removed": [...],
      "changed": [...]
    }
```

## Project Structure

```
app/
├── main.py       # FastAPI application with endpoints
├── agent.py      # Agent creation and configuration (draft & review)
├── tools.py      # Tool definitions (diff_checker)
├── models.py     # Pydantic request/response models
├── utils.py      # Utility functions (JSON parsing)
└── __init__.py
```

## Components

### 1. FastAPI Application (`main.py`)

Provides RESTful API endpoints for the diff checking pipeline:

**Endpoints:**
- `GET /` - Root endpoint with API info
- `GET /health` - Health check with service status
- `POST /check_diff_agent` - Main diff checking endpoint
- `GET /tools` - List available tools

All endpoints include CORS middleware for cross-origin requests.

### 2. Agent Configuration (`agent.py`)

Two specialized agents work in sequence:

#### **Draft Diff Agent**
```python
def draft_diff_agent():
    system_prompt = """You are a AI diff checker agent.
    You will be given two pieces of text and you need to analyze the differences...
    """
```

**Purpose**: 
- Receives two text inputs
- Uses the `diff_checker` tool to generate unified diff format
- Analyzes the diff using AI reasoning
- Produces a natural language summary of differences
- Limited to 500 words for conciseness

**Returns**: Draft summary as text

#### **Review Diff Agent**
```python
def review_diff_agent():
    system_prompt = """You are a AI agent to review a diff summary draft.
    Your task is to review the diff summary draft and return the final diff summary...
    """
```

**Purpose**:
- Receives the draft summary and original texts
- Reviews the draft for accuracy and completeness
- Structures output in consistent JSON format
- Categorizes changes into: added, removed, changed

**Returns**: Structured JSON with `ReviewResponse` format

### 3. Tools (`tools.py`)

#### **diff_checker Tool**
```python
@tool
def diff_checker(first_string: str, second_string: str) -> str:
    """Check the differences between two strings using unified diff format."""
```

**Capabilities**:
- Uses Python's `difflib.unified_diff` for accurate line-by-line comparison
- Generates standard unified diff format with context lines
- Handles large texts efficiently
- Error handling for edge cases

**Input**:
- `first_string`: Original text
- `second_string`: Modified text

**Output**: Unified diff string or "No differences found" message

**Example Usage**:
```
--- original
+++ modified
@@ -1,3 +1,4 @@
 Line 1
 Line 2
+Line added
 Line 3
```

### 4. Data Models (`models.py`)

**DiffRequest**
```python
{
  "text1": str,  # First text to compare
  "text2": str   # Second text to compare
}
```

**ReviewResponse**
```python
{
  "added": [str],      # List of added items/lines
  "removed": [str],    # List of removed items/lines
  "changed": [str]     # List of changed items/lines
}
```

**AgentResponse**
```python
{
  "response": ReviewResponse,     # Structured diff output
  "tools_used": [str],           # Tools invoked by agents
  "messages": [dict],            # Full conversation history
  "more_context": str            # Draft summary from Stage 1
}
```

**HealthResponse**
```python
{
  "status": str,                 # "healthy"
  "version": str,                # API version
  "model": str,                  # Active model name
  "available_tools": [str]       # List of available tools
}
```

### 5. Utilities (`utils.py`)

**parse_fenced_json()**
- Parses JSON from markdown-fenced code blocks
- Handles tuple/list inputs
- Removes markdown syntax (triple backticks)
- Used for parsing structured agent outputs

## Agent Execution Flow

### Request Processing

```
POST /check_diff_agent
  ↓
1. Parse DiffRequest (text1, text2)
  ↓
2. Create draft_diff_agent()
  ↓
3. Invoke agent with:
     - HumanMessage("Compare these two texts. Text 1: " + text1)
     - HumanMessage("Text 2: " + text2)
  ↓
4. Agent invokes diff_checker tool
  ↓
5. Extract last message → draft_agent_response
  ↓
6. Create review_diff_agent()
  ↓
7. Invoke agent with:
     - HumanMessage("Here is draft: " + draft_agent_response)
     - HumanMessage("Text 1: " + text1)
     - HumanMessage("Text 2: " + text2)
  ↓
8. Agent structures output as JSON
  ↓
9. Return AgentResponse with structured diff
```

### Error Handling

Both agents catch exceptions during creation:
```python
except Exception as e:
    print(f"Error creating agent: {e}")
    agent = None
```

The `/check_diff_agent` endpoint wraps execution in try-catch:
```python
except Exception as e:
    logger.exception("Agent error")
    raise HTTPException(status_code=500, detail=str(e))
```

## Configuration

### Environment Variables

```bash
# Model Provider Configuration
ANTHROPIC_MODEL_NAME=claude-haiku-4-5         # Default model
MODEL_TEMPERATURE=0.7                          # Creativity (0-1)
MODEL_MAX_TOKENS=1000                          # Response length limit

# API Server Configuration
API_HOST=0.0.0.0                              # Bind address
API_PORT=8000                                  # Port number
API_RELOAD=true                                # Auto-reload on changes
LOG_LEVEL=INFO                                 # Logging level
APP_VERSION=1.0.0                             # API version

# Provider API Keys (choose one)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### Model Selection

The agents use LangChain's `init_chat_model()` for flexible provider support:

```python
agent = create_agent(
    model=os.getenv("ANTHROPIC_MODEL_NAME"),
    tools=[...],
    system_prompt=system_prompt
)
```

**Supported Providers:**

| Provider | Model Format | Required Key |
|----------|-------------|--------------|
| Anthropic | `claude-haiku-4-5` | `ANTHROPIC_API_KEY` |
| OpenAI | `gpt-4-turbo-preview` | `OPENAI_API_KEY` |
| Google Gemini | `gemini-1.5-pro` | `GOOGLE_API_KEY` |
| Vertex AI | `vertex_ai:gemini-1.5-pro` | `GOOGLE_CLOUD_*` |
| AWS Bedrock | `bedrock:anthropic.claude-3-sonnet` | AWS credentials |
| Mistral | `mistral-large` | `MISTRAL_API_KEY` |
| Groq | `mixtral-8x7b-32768` | `GROQ_API_KEY` |

## API Endpoints

### `POST /check_diff_agent`

The main endpoint that runs the complete diff checking pipeline.

**Request:**
```json
{
  "text1": "Original text content",
  "text2": "Modified text content"
}
```

**Response:**
```json
{
  "response": {
    "added": ["new line 1", "new line 2"],
    "removed": ["removed line"],
    "changed": ["line that changed"]
  },
  "tools_used": [],
  "messages": [],
  "more_context": "Draft summary from Stage 1 agent..."
}
```

**How It Works**:
1. Stage 1: Draft agent analyzes differences
2. Stage 2: Review agent structures the output
3. Both agents use the `diff_checker` tool and AI reasoning
4. Returns structured JSON with categorized changes

### `GET /health`

Health check endpoint showing service status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "claude-haiku-4-5",
  "available_tools": ["diff_checker"]
}
```

### `GET /tools`

List all available tools with descriptions.

**Response:**
```json
{
  "tools": [
    {
      "name": "diff_checker",
      "description": "Check the differences between two strings using unified diff format.",
      "args": {
        "first_string": {...},
        "second_string": {...}
      }
    }
  ]
}
```

## Usage Examples

### Example 1: Compare Code
```bash
curl -X POST http://localhost:8000/check_diff_agent \
  -H "Content-Type: application/json" \
  -d '{
    "text1": "def hello():\n  print(\"Hello\")",
    "text2": "def hello():\n  print(\"Hello World!\")"
  }'
```

### Example 2: Compare Documents
```bash
curl -X POST http://localhost:8000/check_diff_agent \
  -H "Content-Type: application/json" \
  -d '{
    "text1": "Chapter 1\nIntroduction",
    "text2": "Chapter 1\nIntroduction\nChapter 2\nQuick Start"
  }'
```

### Example 3: Health Check
```bash
curl http://localhost:8000/health
```

### Python Client
```python
import requests

response = requests.post(
    "http://localhost:8000/check_diff_agent",
    json={
        "text1": "original text",
        "text2": "modified text"
    }
)

print(response.json())
```

## Extending the System

### Add a New Tool

1. Define the tool in `app/tools.py`:
```python
@tool
def new_tool(input: str) -> str:
    """Tool description."""
    return "result"
```

2. Add to `ALL_TOOLS` list:
```python
ALL_TOOLS = [diff_checker, new_tool]
```

3. Update agent system prompts to reference the new tool

### Customize Agent Behavior

Edit system prompts in `app/agent.py`:

**Draft Agent**:
```python
system_prompt = """You are a AI diff checker agent.
[Modify instructions here]
"""
```

**Review Agent**:
```python
system_prompt = """You are a AI agent to review a diff summary draft.
[Modify instructions here]
"""
```

### Change Response Format

Modify `ReviewResponse` in `app/models.py`:
```python
class ReviewResponse(BaseModel):
    added: List[str]
    removed: List[str]
    changed: List[str]
    # Add new fields here
```

## Dependencies

- **LangChain**: 1.2.10 - Agent framework
- **LangGraph**: 1.0.10 - Graph-based agent orchestration
- **FastAPI**: 0.135.1 - Web framework
- **Pydantic**: 2.12.5+ - Data validation
- **uvicorn**: 0.41.0 - ASGI server
- **python-dotenv**: 1.2.2 - Environment configuration

See `pyproject.toml` for complete dependency list.

## Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Agent Reasoning
The `more_context` field in `AgentResponse` contains the draft agent's reasoning:
```python
response = requests.post("http://localhost:8000/check_diff_agent", json=...)
print(response.json()["more_context"])  # Draft agent's analysis
```

### Check Message History
```python
print(response.json()["messages"])  # Full conversation
```

## Performance Considerations

- **Response time**: Depends on model latency (typically 2-5 seconds)
- **Text size**: Agents work efficiently with texts up to ~10,000 words
- **Token usage**: Draft agent ~300-500 tokens, Review agent ~200-400 tokens
- **Concurrency**: Use async client for multiple simultaneous requests

## Security Notes

- Validate input text sizes to prevent DoS attacks
- Keep API keys in `.env` file, never commit to version control
- Use environment-specific configurations for different deployments
- Implement rate limiting in production

## Running the Project

### With Docker
```bash
docker-compose up --build
```

### Locally
```bash
uv sync
uv run python -m app.main
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Server                        │
│                  (app/main.py)                           │
├─────────────────────────────────────────────────────────┤
│ GET / │ GET /health │ POST /check_diff_agent │ GET /tools│
└────────────┬──────────────────────────────────────────────┘
             │
             ↓ DiffRequest(text1, text2)
┌─────────────────────────────────────────────────────────┐
│           Draft Diff Agent (app/agent.py)                │
│  - System Prompt from agent.py                          │
│  - Uses: diff_checker tool                              │
│  - Output: Draft summary (text)                         │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓ (draft_agent_response)
┌─────────────────────────────────────────────────────────┐
│          Review Diff Agent (app/agent.py)                │
│  - System Prompt from agent.py                          │
│  - Validates against text1, text2                       │
│  - Output: ReviewResponse (JSON)                        │
└────────────┬──────────────────────────────────────────────┘
             │
             ↓ AgentResponse
┌─────────────────────────────────────────────────────────┐
│        return AgentResponse (app/models.py)              │
│  - response: ReviewResponse                             │
│  - more_context: draft summary                          │
│  - tools_used: []                                       │
│  - messages: []                                         │
└─────────────────────────────────────────────────────────┘
```

## Version History

- **1.0.0** - Initial release with dual-agent diff checking pipeline

## Support & Contributing

For issues, improvements, or feature requests, please refer to the main README.md or open an issue in the repository.
