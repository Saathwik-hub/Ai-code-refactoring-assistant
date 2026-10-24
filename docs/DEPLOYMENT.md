# Deployment & Operations Guide

This guide covers production deployment strategies for **AI Code Refactoring Assistant**, including local bare-metal, Docker containerization, and cloud PaaS platforms.

---

## 1. Quick Local Production Run

```bash
# 1. Clone repository
git clone https://github.com/Saathwik-hub/Ai-code-refactoring-assistant.git
cd Ai-code-refactoring-assistant

# 2. Configure environment
cp .env.example .env

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Launch with production Uvicorn workers
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 2. Docker Deployment

### 2.1 Single Container
```bash
# Build Docker image
docker build -t ai-code-refactoring-assistant .

# Run container
docker run -d \
  --name refactor-assistant \
  -p 8000:8000 \
  -v $(pwd)/backend/uploads:/app/backend/uploads \
  ai-code-refactoring-assistant
```

### 2.2 Docker Compose (with Optional Containerized Ollama)
```bash
# Standard application start
docker-compose up -d app

# Or start with containerized Ollama LLM service
docker-compose --profile with-ollama up -d
```

---

## 3. Cloud PaaS Deployment (Render / Railway / Fly.io / AWS ECS)

1. **Port Binding**: Configure the environment variable `PORT=8000` or map your provider's `$PORT` into Uvicorn.
2. **Persistent Disk**: Mount a persistent volume at `/app/backend/uploads` for file uploads, and optionally for `refactor_ai.db`.
3. **CORS**: Set `CORS_ORIGINS` to your production domain (e.g. `https://your-domain.com`).
4. **Health Check Path**: `/health` (HTTP 200).
