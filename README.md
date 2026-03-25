# AI Diff Checker

AI Diff Checker compares two texts using a two-stage AI pipeline and returns structured output:

- `added`
- `removed`
- `changed`

It includes:
- FastAPI backend
- React frontend (Vite)
- Docker setup for running both services

## Quick Start

### 1. Configure environment

```bash
cp .env.example .env
```

Set at least one provider key in `.env` (for example `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`).

### 2. Run locally

Backend:

```bash
uv sync
uv run python -m app.main
```

Frontend (new terminal):

```bash
cd frontend
npm install
npm run dev
```

URLs:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

### 3. Run with Docker

```bash
docker compose up --build
```

URLs:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Docker Guide

### Start all services (frontend + backend)

```bash
cp .env.example .env
docker compose up --build
```

Run in background:

```bash
docker compose up --build -d
```

### Stop services

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

### View logs

```bash
docker compose logs -f
```

API logs only:

```bash
docker compose logs -f api
```

Frontend logs only:

```bash
docker compose logs -f frontend
```

### Rebuild images

```bash
docker compose build --no-cache
docker compose up -d
```

### Run backend container only

```bash
docker build -f Dockerfile -t ai-diff-checker-api .
docker run --rm -p 8000:8000 --env-file .env ai-diff-checker-api
```

## API

### `POST /check_diff_agent`

Request:

```json
{
  "text1": "original text",
  "text2": "updated text"
}
```

Response:

```json
{
  "response": {
    "added": ["..."],
    "removed": ["..."],
    "changed": ["..."]
  },
  "tools_used": [],
  "messages": [],
  "more_context": "draft analysis summary"
}
```

### `GET /health`
Returns service health and active model metadata.

### `GET /tools`
Returns available tool definitions.

## Configuration

Important `.env` variables:

```bash
# Model
ANTHROPIC_MODEL_NAME=claude-haiku-4-5
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=1000

# Server
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
LOG_LEVEL=INFO

# Rate limiting (per client IP, per endpoint, per minute)
API_RATE_LIMIT_PER_MINUTE=120
API_RATE_LIMIT_CHECK_DIFF_PER_MINUTE=20
API_RATE_LIMIT_HEALTH_PER_MINUTE=600
API_RATE_LIMIT_TOOLS_PER_MINUTE=120
API_RATE_LIMIT_ROOT_PER_MINUTE=120
```

## Project Structure

```text
app/                 # FastAPI backend
frontend/            # React frontend
docker-compose.yml   # Full stack run
Dockerfile           # Backend image
frontend/Dockerfile  # Frontend image
```

## More Documentation

- Backend architecture: [AGENTS.md](AGENTS.md)
- Frontend details: [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)
- Frontend setup: [frontend/README.md](frontend/README.md)

## Troubleshooting

- Port in use:
  - Change `API_PORT` in `.env`
  - Or stop conflicting process
- Dependency issues:

```bash
uv sync --force
cd frontend && npm install
```
