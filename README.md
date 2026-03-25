# AI Diff Checker

An intelligent diff checking tool powered by **LangChain AI agents** that analyzes and compares text, generating structured, user-friendly diffs using multiple AI model providers.

## Overview

**AI Diff Checker** uses a two-stage AI agent pipeline:

1. **Draft Diff Agent** - Analyzes two text inputs and generates a summary of differences
2. **Review Diff Agent** - Reviews the draft and structures the output into organized categories (added, removed, changed)

This approach ensures accurate, well-organized diff reports powered by AI reasoning.

### Key Features

- 🤖 **Dual-Agent Pipeline** - Draft and review stages for accurate diffs
- 🔧 **Tool Integration** - Uses Python's `difflib` for low-level diff generation
- 🌍 **Multi-Model Support** - OpenAI, Anthropic, Google, AWS, Mistral, Groq, Cohere
- ⚡ **FastAPI Server** - RESTful API with auto-generated documentation
- 📊 **Structured Output** - JSON-formatted diffs with categorized changes
- 🐳 **Docker Ready** - Includes Docker and Docker Compose support
- ⚙️ **Configurable** - Environment-based model and parameter configuration

## Tech Stack

- **Framework**: FastAPI, LangChain, LangGraph
- **Python**: 3.11+
- **Models**: Multiple provider support via LangChain
- **Validation**: Pydantic v2

## Quick Start

### Prerequisites
- Python 3.11+
- `uv` package manager (or `pip`)
- API keys for your preferred AI model provider

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-diff-checker
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Set your configuration in `.env`:
   ```bash
   # Model Configuration
   ANTHROPIC_MODEL_NAME=claude-haiku-4-5
   MODEL_TEMPERATURE=0.7
   MODEL_MAX_TOKENS=1000
   
   # API Keys (choose your provider)
   ANTHROPIC_API_KEY=sk-ant-...
   # or
   OPENAI_API_KEY=sk-...
   # or
   GOOGLE_API_KEY=...
   ```

### Running Locally

**Terminal 1 - Backend API:**
```bash
uv run python -m app.main
```

The API will be available at `http://localhost:8000`
Access interactive documentation at `http://localhost:8000/docs`

**Terminal 2 - Frontend (in a new terminal):**
```bash
cd frontend
npm install  # First time only
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Using Docker

Build and run both backend and frontend with Docker Compose:

```bash
docker compose up --build
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

Or build backend manually:

```bash
docker build -f Dockerfile -t ai-diff-checker .
docker run -p 8000:8000 --env-file .env ai-diff-checker
```

### Docker Hot Reload (Development)

Use the dev override file to enable hot reload for both API and frontend while keeping the default compose file production-like.

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Development behavior with this command:
- API runs with `uvicorn --reload` and watches `app/`.
- Frontend runs Vite dev server with hot module replacement.
- Source code is bind-mounted, so edits are reflected without rebuilding images.

Stop the dev stack:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml down
```

## Frontend (React + Vite)

A modern, lightweight React frontend is included for easy interaction with the diff API.

### Quick Start

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:5173` and automatically proxies API requests to `http://localhost:8000`.

### Features

- 📝 Side-by-side text input areas
- 🚀 Real-time diff analysis
- 📊 Organized result display (added, removed, changed)
- 💾 AI analysis summary
- 📱 Responsive design
- ⚡ Built with Vite and Tailwind CSS

### Frontend Build & Deploy

**Development**:
```bash
cd frontend
npm run dev
```

**Production Build**:
```bash
cd frontend
npm run build
npm run preview
```

For detailed frontend documentation, see [frontend/README.md](frontend/README.md).

## API Endpoints

### `GET /`
Returns API information and available tools.

**Response:**
```json
{
  "message": "AI Agent API",
  "docs": "/docs",
  "available_tools": ["diff_checker"]
}
```

### `GET /health`
Health check with service status and available tools.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model": "claude-haiku-4-5",
  "available_tools": ["diff_checker"]
}
```

### `POST /check_diff_agent`
Run the diff checking agent pipeline on two text inputs.

**Request:**
```json
{
  "text1": "original text content",
  "text2": "modified text content"
}
```

**Response:**
```json
{
  "response": {
    "added": ["new line 1", "new line 2"],
    "removed": ["old line 1"],
    "changed": ["line that was modified"]
  },
  "tools_used": [],
  "messages": [],
  "more_context": "initial draft analysis from the first agent..."
}
```

### `GET /tools`
List all available tools with their descriptions and arguments.

**Response:**
```json
{
  "tools": [
    {
      "name": "diff_checker",
      "description": "Check the differences between two strings using unified diff format.",
      "args": {...}
    }
  ]
}
```

## Usage Examples

### Compare Code Changes
```bash
curl -X POST http://localhost:8000/check_diff_agent \
  -H "Content-Type: application/json" \
  -d '{
    "text1": "def hello():\n  print(\"Hello\")",
    "text2": "def hello():\n  print(\"Hello World\")"
  }'
```

### Compare Documents
```bash
curl -X POST http://localhost:8000/check_diff_agent \
  -H "Content-Type: application/json" \
  -d '{
    "text1": "Chapter 1: Introduction",
    "text2": "Chapter 1: Introduction\nChapter 2: First Steps"
  }'
```

### Check Health
```bash
curl http://localhost:8000/health
```

## Project Structure

```
ai-diff-checker/
├── app/                    # Backend FastAPI application
│   ├── main.py            # FastAPI app and endpoints
│   ├── agent.py           # Agent configuration (draft & review)
│   ├── tools.py           # Tool definitions (diff_checker)
│   ├── models.py          # Pydantic models
│   ├── utils.py           # Utility functions
│   └── __init__.py
├── frontend/              # React frontend (Vite + Tailwind)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api.js         # API client
│   │   ├── App.jsx        # Main component
│   │   ├── main.jsx       # Entry point
│   │   └── index.css      # Styles
│   ├── public/            # Static assets
│   ├── index.html         # HTML template
│   ├── vite.config.js     # Vite configuration
│   ├── tailwind.config.js # Tailwind configuration
│   ├── package.json       # Frontend dependencies
│   └── README.md          # Frontend documentation
├── Dockerfile             # Production Docker image (backend)
├── docker-compose.yml     # Docker Compose configuration
├── pyproject.toml         # Backend dependencies
├── AGENTS.md              # Agent architecture documentation
└── .env.example        # Example environment configuration
```

## Complete Setup Guide

### Option 1: Local Development (Recommended for Development)

This setup runs both backend and frontend locally with hot-reload.

**Step 1: Start the Backend API**
```bash
# Terminal 1
cp .env.example .env
# Edit .env and add your API keys (e.g., ANTHROPIC_API_KEY)
uv run python -m app.main
```

The API will be running at `http://localhost:8000`

**Step 2: Start the Frontend**
```bash
# Terminal 2
cd frontend
cp .env.example .env.local
# Edit .env.local if needed (usually localhost:8000 works by default)
npm install  # First time only
npm run dev
```

The frontend will be at `http://localhost:5173`

**Access the application:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

### Option 2: Docker Compose (Recommended for Production)

This setup containerizes both frontend and backend.

**Step 1: Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

**Step 2: Start with Docker Compose**
```bash
docker-compose up --build
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 3: Backend Only (API-Only Deployment)

If you only want the API without the frontend:

```bash
# Backend Docker
docker build -f Dockerfile -t ai-diff-checker .
docker run -p 8000:8000 --env-file .env ai-diff-checker

# Or locally
uv run python -m app.main
```

Then use the API directly or integrate with your own frontend.

## Configuration

### Environment Variables

```bash
# Model Configuration
ANTHROPIC_MODEL_NAME=claude-haiku-4-5    # LLM model name
MODEL_TEMPERATURE=0.7                     # Creativity level (0-1)
MODEL_MAX_TOKENS=1000                     # Max response length

# API Server
API_HOST=0.0.0.0                         # Server host
API_PORT=8000                             # Server port
API_RELOAD=true                           # Auto-reload on code changes
LOG_LEVEL=INFO                            # Logging level

# Rate limiting (requests per minute, per client IP and per endpoint)
API_RATE_LIMIT_PER_MINUTE=120
API_RATE_LIMIT_CHECK_DIFF_PER_MINUTE=20
API_RATE_LIMIT_HEALTH_PER_MINUTE=600
API_RATE_LIMIT_TOOLS_PER_MINUTE=120
API_RATE_LIMIT_ROOT_PER_MINUTE=120

# Provider API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
GOOGLE_CLOUD_PROJECT=your-project
GOOGLE_CLOUD_LOCATION=us-central1
```

### Supported Models

The agent supports multiple LLM providers through LangChain:

| Provider | Model Format | Environment Variable |
|----------|-------------|----------------------|
| Anthropic | `claude-haiku-4-5` | `ANTHROPIC_API_KEY` |
| OpenAI | `gpt-4-turbo-preview` | `OPENAI_API_KEY` |
| Google Gemini | `gemini-1.5-pro` | `GOOGLE_API_KEY` |
| Google Vertex AI | `vertex_ai:gemini-1.5-pro` | `GOOGLE_CLOUD_*` |
| AWS Bedrock | `bedrock:anthropic.claude-3-sonnet` | AWS credentials |
| Mistral | `mistral-large` | `MISTRAL_API_KEY` |
| Groq | `mixtral-8x7b-32768` | `GROQ_API_KEY` |

## How It Works

### Two-Stage Diff Processing

1. **Stage 1: Draft Diff Agent**
   - Receives two text inputs
   - Uses the `diff_checker` tool to generate a unified diff
   - AI analyzes the diff and creates a summary
   - Output: Natural language summary of changes

2. **Stage 2: Review Diff Agent**
   - Receives the draft summary + original texts
   - AI reviews and categorizes the changes
   - Structures output into categories: added, removed, changed
   - Output: Structured JSON with organized differences

### Tools

**diff_checker**
- Uses Python's `difflib.unified_diff` for accurate, line-by-line comparison
- Generates standard unified diff format
- Handles empty diffs gracefully
- Input: Two text strings to compare
- Output: Unified diff string or "No differences found"

## Development

### Run Tests
```bash
uv run pytest
```

### View Logs
```bash
tail -f logs/app.log
```

### Debug Mode
Set `LOG_LEVEL=DEBUG` for detailed logging:
```bash
LOG_LEVEL=DEBUG uv run python -m app.main
```

## Dependencies

Core dependencies are managed in `pyproject.toml`:

- **fastapi** `0.135.1` - Web framework
- **uvicorn** `0.41.0` - ASGI server
- **langchain** `1.2.10` - Agent framework
- **langgraph** `1.0.10` - Graph-based execution
- **langchain-anthropic** `1.3.4` - Anthropic integration
- **langchain-openai** `1.1.10` - OpenAI integration
- **pydantic** `>=2.12.5` - Data validation

Optional provider support:
```bash
uv sync --extra aws           # AWS Bedrock support
uv sync --extra mistral       # Mistral AI support
uv sync --extra groq          # Groq support
uv sync --extra cohere        # Cohere support
```

## Architecture Details

For comprehensive information about the agent architecture, tool integration, and AI model configuration, see:
- **Backend Architecture**: [AGENTS.md](AGENTS.md)
- **Frontend Development**: [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)

## Documentation Map

### For Backend Development
- **[AGENTS.md](AGENTS.md)** - Complete AI agent architecture, component descriptions, API specifications, and agent execution flow
- **[pyproject.toml](pyproject.toml)** - Backend dependencies and project configuration

### For Frontend Development
- **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** - React frontend guide with component documentation, styling, development tips, and deployment
- **[frontend/README.md](frontend/README.md)** - Frontend-specific setup and usage guide

### Getting Started
- **Quick setup:** Run `./setup.sh` for automated setup
- **Local development:** See "Complete Setup Guide" above
- **Docker deployment:** See "Configuration" above

### Key Files
- **README.md** (this file) - Project overview and unified setup guide
- **AGENTS.md** - Backend agent architecture details
- **FRONTEND_GUIDE.md** - Frontend development guide
- **Dockerfile** - Backend production container
- **frontend/Dockerfile** - Frontend production container
- **docker-compose.yml** - Complete stack (backend + frontend)

## Quick Reference

| Task | Command |
|------|---------|
| Setup everything | `./setup.sh` |
| Run backend locally | `uv run python -m app.main` |
| Run frontend locally | `cd frontend && npm run dev` |
| Run both with Docker | `docker-compose up --build` |
| Build production frontend | `cd frontend && npm run build` |
| View API docs | Visit `http://localhost:8000/docs` |
| Check API health | `curl http://localhost:8000/health` |

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
API_PORT=9000 uv run python -m app.main
```

### API Key Issues
- Verify your `.env` file is in the project root
- Ensure the API key has proper permissions
- Check that the model name matches your provider

### Import Errors
```bash
# Reinstall dependencies
uv sync --force
```

### Agent Errors
Enable debug logging to diagnose issues:
```bash
LOG_LEVEL=DEBUG uv run python -m app.main
```

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 standards
- New tools are properly documented
- Tests cover new functionality
- API changes are documented

## License

[Add your license here]

## Support

For issues or questions, please open an issue on the repository.
