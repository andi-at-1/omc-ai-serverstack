# OMC AI ServerStack

Self-hosted AI development stack with Docker Compose. Modified for OMC environment.

## What's included

- n8n - Workflow automation platform with 400+ integrations
- Supabase - PostgreSQL database with REST API and realtime subscriptions
- Open WebUI - ChatGPT-like interface for local LLM interaction
- Flowise - Visual AI agent builder for creating LLM workflows
- Qdrant - High-performance vector database for RAG applications
- Neo4j - Graph database for knowledge graphs and connected data
- Langfuse - LLM observability and tracing platform
  - ClickHouse - Columnar database for Langfuse analytics
  - MinIO - S3-compatible object storage for Langfuse
  - PostgreSQL - Dedicated database for Langfuse metadata
  - Redis/Valkey - In-memory cache and queue for Langfuse
- Portainer - Web UI for Docker container management

## Prerequisites

- Docker from official repo
- Python 3
- python-is-python3 package

## Installation

1. Copy and edit environment file:
```
cp .env.example .env
nano .env
```

2. Set required secrets (use `openssl rand -hex 32` to generate):
```
N8N_ENCRYPTION_KEY=
N8N_USER_MANAGEMENT_JWT_SECRET=
POSTGRES_PASSWORD=
JWT_SECRET=
ANON_KEY=
SERVICE_ROLE_KEY=
DASHBOARD_USERNAME=
DASHBOARD_PASSWORD=
NEO4J_AUTH=neo4j/yourpassword
CLICKHOUSE_PASSWORD=
MINIO_ROOT_PASSWORD=
LANGFUSE_SALT=
NEXTAUTH_SECRET=
ENCRYPTION_KEY=
```

## Usage

Start all services:
```
python start_services.py --profile none --environment omc
```

WARNING: omc environment exposes all ports on 0.0.0.0. Only use in trusted environments.

## Service Access

Main services:
- n8n: http://localhost:5678
- Open WebUI: http://localhost:8080
- Flowise: http://localhost:3001
- Supabase: http://localhost:8000
- Neo4j: http://localhost:7474
- Qdrant: http://localhost:6333
- Langfuse: http://localhost:3000
  - ClickHouse: http://localhost:8123 (HTTP), localhost:9000 (native)
  - MinIO Console: http://localhost:9011
  - PostgreSQL: localhost:5433
  - Redis: localhost:6379
- Portainer: http://localhost:9123

First access to n8n and Open WebUI requires local account setup.

## Service Connection Info

For n8n workflows:
- Postgres host: `db`
- Qdrant: `http://qdrant:6333`

## n8n + Open WebUI Integration

1. Create n8n workflow with webhook trigger
2. Copy production webhook URL
3. Open WebUI: Workspace -> Functions -> Add Function
4. Paste code from `n8n_pipe.py`
5. Set n8n_url to webhook URL
6. Enable function

## Upgrading

```
docker compose -p localai down
docker compose -p localai pull
python start_services.py --profile none --environment omc
```

## Local File Access

n8n can access files in `./shared` directory at container path `/data/shared`

## Troubleshooting

Common issues:

- Supabase pooler restarting: Check https://github.com/supabase/supabase/issues/30210
- Supabase analytics fails after password change: Delete `supabase/docker/volumes/db/data`
- Docker Desktop: Enable "Expose daemon on tcp://localhost:2375 without TLS"
- Supabase connection fails: No "@" in POSTGRES_PASSWORD
- SearXNG restarting: Run `chmod 755 searxng`
- Missing Supabase files: Delete `supabase/` folder and restart

## License

Apache License 2.0 - Based on n8n Local AI Starter Kit
