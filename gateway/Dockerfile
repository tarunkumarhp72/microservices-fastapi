# API Gateway - Production Docker Image

# Purpose: Single entry point for all client requests
# Routing, authentication, rate limiting

#  STAGE 1: Builder - Install dependencies
# This stage installs all Python packages and can be cached separately
FROM python:3.12-slim AS builder

# Update package manager and install minimal runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

#  Install Python dependencies to user site-packages
# This reduces final image size (doesn't include apt cache)
# --user flag installs to /root/.local
RUN pip install --user --no-cache-dir --upgrade pip setuptools

WORKDIR /app

# Copy only requirements first for better layer caching
# If code changes, this layer is cached and reused (faster builds)
COPY gateway/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


#  STAGE 2: Runtime - Minimal production image
# Only includes what's needed to run the application
FROM python:3.12-slim

#  Container metadata
LABEL service="api-gateway" \
      version="1.0" \
      description="FastAPI API Gateway for social media platform"

#  Create non-root user for security
# Running as non-root prevents container escape attacks
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r app && useradd -r -g app app

#  Set working directory
WORKDIR /app

#  Environment configuration
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/app/.local/bin:$PATH

#  Copy installed Python packages from builder stage
# (much smaller than copying /usr/local/lib/python3.12)
COPY --from=builder /root/.local /home/app/.local

#  Copy application code
COPY shared_lib/shared /app/shared
COPY gateway/ /app/

#  Switch to non-root user
USER app

#  Health check endpoint
# Docker uses this to monitor if container is healthy
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD curl -f http://localhost:8000/health || exit 1

#  Start the application with Gunicorn + Uvicorn workers
# 4 worker processes: allows handling multiple requests concurrently
# UvicornWorker: async ASGI worker for FastAPI
# graceful-timeout: time to wait for workers to finish before killing
# max-requests: recycle workers to prevent memory leaks
CMD ["gunicorn", \
     "-w", "4", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--graceful-timeout", "30", \
     "--max-requests", "1000", \
     "--access-logfile", "-", \
     "main:app"]
