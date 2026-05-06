# Embedding Service

A lightweight FastAPI service for loading local sentence-transformer models and generating text embeddings via a provider-based architecture.

## Overview

This service loads model configurations from `config/models.yaml`, initializes providers from `app/providers`, preloads local models, and exposes a REST API for embedding generation.

## Key Features

- Provider-based model loading
- Local `SentenceTransformer` model support
- Model registry configuration via YAML
- Health endpoint and model listing endpoint
- Asynchronous embedding generation
- Docker and Docker Compose deployment

## Prerequisites

- Python 3.14+ (project requires Python >= 3.14)
- `pip` package manager
- `git` (optional)
- Docker and Docker Compose (optional for container deployment)

## Install dependencies

Create and activate a virtual environment, then install required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install fastapi uvicorn[standard] sentence-transformers
```

> Note: The repository currently uses a minimal `requirements.txt`, so the additional packages above are required for local development.

## Configuration

The service loads model definitions from `config/models.yaml`.

Example entry:

```yaml
models:
  - name: all-MiniLM-L6-v2
    provider: local
    path: models/all-MiniLM-L6-v2
```

For environment configuration, create a `.env` file in the repository root with values like:

```env
DEBUG=true
LOG_LEVEL=INFO
```

## Running locally

Start the application with Uvicorn:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

By default, the app listens on `http://127.0.0.1:8000`.

## API Endpoints

### Health check

- `GET /health`
- Returns service status, provider count, and model count.

### List available models

- `GET /models`
- Returns a JSON object listing configured models.

### Create embeddings

- `POST /embeddings`
- Request body:

```json
{
  "provider": "local",
  "model": "all-MiniLM-L6-v2",
  "input": "Hello world"
}
```

or for multiple inputs:

```json
{
  "provider": "local",
  "model": "all-MiniLM-L6-v2",
  "input": ["Hello world", "Second sentence"]
}
```

- Response:

```json
{
  "model": "all-MiniLM-L6-v2",
  "embeddings": [[...], [...]]
}
```

## Docker deployment

Build and run with Docker Compose:

```powershell
docker-compose up --build
```

The service is published on port `8000`.

## Project layout

- `app/main.py` - FastAPI application and startup lifecycle
- `app/api/routes.py` - HTTP routes for health, models, and embeddings
- `app/engine/embedding_engine.py` - request orchestration and provider dispatch
- `app/core/model_registry.py` - YAML model registry loader
- `app/core/provider_loader.py` - dynamic provider discovery and loading
- `app/providers/local/provider.py` - local `SentenceTransformer` provider implementation
- `config/models.yaml` - registered models and provider bindings
- `requirements.txt` - base Python dependencies
- `docker-compose.yml`, `Dockerfile` - container deployment

## Notes

- The current implementation includes a local provider with model preloading and embedding support.
- Add new providers by creating a folder under `app/providers`, implementing a `Provider` class, and registering the provider in `config/models.yaml`.
- Ensure your local models are available in the `models/` directory and referenced correctly in `config/models.yaml`.
