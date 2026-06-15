# Social Media Feed System - Microservices Architecture

A **production-ready** microservices-based social media platform built with **FastAPI** and **Gunicorn**, featuring user management, post creation, follower relationships, personalized feed generation, and Redis caching.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Services](#services)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Production Setup](#production-setup)
- [Load Balancing](#load-balancing)
- [API Endpoints](#api-endpoints)
- [Managing Databases with pgAdmin](#-managing-databases-with-pgadmin)
- [Database Migrations](#-database-migrations)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

## 🎯 Project Overview

This project demonstrates a modern, **production-grade** microservices architecture for a social media platform. Each service is independently deployable, scalable, and manages its own database following the microservices pattern.

### Key Features:
- ✅ **User Authentication & Management** - Secure JWT-based authentication with bcrypt hashing
- ✅ **Post Management** - Create, retrieve, update, and manage user posts
- ✅ **Social Relationships** - Follow/unfollow with follower management
- ✅ **Personalized Feed** - Intelligent feed aggregation from followed users
- ✅ **Caching Layer** - Redis integration for performance (TTL: 5 minutes)
- ✅ **Production ASGI Server** - Gunicorn with Uvicorn workers (4 workers per service)
- ✅ **Auto-restart & Health Checks** - Docker health monitoring
- ✅ **Resource Limits** - CPU & memory constraints per container
- ✅ **Secure Logging** - Automatic log rotation to prevent disk issues

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   API Gateway (Port 8000)                   │
│        Gunicorn + Uvicorn (4 workers, Load Balanced)        │
│        Routes requests to microservices                      │
└────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼──────────────┬─────────────┐
        │                │              │             │
        ▼                ▼              ▼             ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐ ┌──────────┐
    │  User    │   │  Post    │   │Follower  │ │  Feed    │
    │ Service  │   │ Service  │   │ Service  │ │ Service  │
    │(8001)    │   │(8003)    │   │(8002)    │ │(8004)    │
    └──────────┘   └──────────┘   └──────────┘ └──────────┘
   Gunicorn (4)   Gunicorn (4)   Gunicorn (4) Gunicorn (4)
        │                │              │             │
        ▼                ▼              ▼             ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐ ┌──────────┐
    │ User DB  │   │ Post DB  │   │Follow DB │ │  Redis   │
    │(Postgres)   │(Postgres)   │(Postgres)   │  Cache   │
    └──────────┘   └──────────┘   └──────────┘ └──────────┘

    All services communicate via internal Docker network
```

## 🔧 Services

### 1. **User Service** (Port 8001)
Authentication and user profile management.

**Responsibilities:**
- User registration and login (JWT authentication)
- Profile management and updates
- Password hashing with bcrypt
- User validation for other services

**Database:** PostgreSQL (user_db)
**Ports:** 8001 (internal)
**Workers:** 4 Gunicorn + Uvicorn workers

---

### 2. **Post Service** (Port 8003)
Content creation and retrieval with caching.

**Responsibilities:**
- Create, read, update, delete posts
- User validation via User Service
- Post metadata and timestamps
- Follower information from Follower Service

**Database:** PostgreSQL (posts_db)
**Ports:** 8003 (internal)
**Workers:** 4 Gunicorn + Uvicorn workers
**Cache:** Redis (TTL: 5 minutes)

---

### 3. **Follower Service** (Port 8002)
User follow relationships and social graph.

**Responsibilities:**
- Follow/unfollow users
- Retrieve follower and following lists
- Check follow relationships
- Support for feed personalization

**Database:** PostgreSQL (follow_db)
**Ports:** 8002 (internal)
**Workers:** 4 Gunicorn + Uvicorn workers

---

### 4. **Feed Service** (Port 8004)
Personalized feed aggregation for users.

**Responsibilities:**
- Aggregate posts from followed users
- Generate personalized feeds
- Cache feed results
- Real-time feed updates

**Database:** None (read-only, queries other services)
**Ports:** 8004 (internal)
**Workers:** 4 Gunicorn + Uvicorn workers
**Cache:** Redis (TTL: 5 minutes)
**Dependencies:** Follower Service, Post Service

---

### 5. **API Gateway** (Port 8000)
Single entry point for all client requests.

**Responsibilities:**
- Route requests to appropriate microservices
- JWT token validation
- Rate limiting and request throttling
- Request/response logging
- Load balancing (Docker DNS-based)

**Ports:** 8000 (PUBLIC - exposed to internet)
**Workers:** 4 Gunicorn + Uvicorn workers
**Dependencies:** All microservices

## 💻 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.116.1 |
| **ASGI Server** | Gunicorn + Uvicorn | 23.0.0 + 0.35.0 |
| **ORM** | SQLAlchemy | 2.0.43 |
| **Database** | PostgreSQL | 15-Alpine |
| **Cache** | Redis | 7-Alpine |
| **Authentication** | JWT + Passlib + Bcrypt | Latest |
| **Migrations** | Alembic | 1.16.5 |
| **Containerization** | Docker & Docker Compose | Latest |
| **Language** | Python | 3.12-slim |

## 📦 Prerequisites

### Option 1: Docker (Recommended for Production)
- **Docker** v20.10+
- **Docker Compose** v2.0+
- 2GB RAM minimum
- 10GB free disk space

### Option 2: Local Development
- **Python** 3.12+
- **PostgreSQL** 15
- **Redis** 7
- **Pip** package manager

## 🚀 Getting Started

### Quick Start (Docker Compose)

1. **Clone and navigate:**
   ```bash
   cd d:\Amandeep\self practise projects\social_media_feed_system\microservices-fastapi
   ```

2. **Prepare environment:**
   ```bash
   # Copy .env template (if exists)
   copy .env.example .env
   
   # OR create manually with required variables
   ```

3. **Update .env with secure values:**
   ```env
   DB_PASSWORD=your_secure_password_here
   REDIS_PASSWORD=your_redis_password_here
   SECRET_KEY=your_jwt_secret_key_here
   JWT_ALGORITHM=HS256
   INTERNAL_SERVICE_TOKEN=your_internal_token_here
   ```

4. **Start all services:**
   ```bash
   docker-compose up -d
   ```

5. **Verify deployment:**
   ```bash
   docker-compose ps
   docker-compose logs -f gateway
   ```

6. **Test API Gateway:**
   ```bash
   curl http://localhost:8000/health
   ```

### Local Development Setup

1. **Install dependencies** (each service):
   ```bash
   cd services/user-microservices
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL and Redis:**
   ```bash
   docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start service** (with reload for development):
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

## ⚙️ Configuration

### Environment Variables (.env)

All variables required for production:

```env
# Database
DB_PASSWORD=your_secure_database_password              # Min 16 chars
REDIS_PASSWORD=your_secure_redis_password              # Min 16 chars

# Security
SECRET_KEY=your_super_secure_jwt_key                   # Min 32 chars
JWT_ALGORITHM=HS256                                     # Or HS512
INTERNAL_SERVICE_TOKEN=your_service_to_service_token   # Min 16 chars

# Optional
PYTHONPATH=.
CACHE_TTL=300                                           # 5 minutes
```

### Docker Compose Configuration

Key settings in `docker-compose.yml`:

**Resource Limits (per service):**
- CPU: 1 core max, 0.5 core reserved
- Memory: 512MB max, 256MB reserved

**Health Checks:**
- Interval: 30 seconds
- Timeout: 5 seconds
- Retries: 3 before marking unhealthy

**Restart Policy:**
- Condition: on-failure
- Max attempts: 5 within 120s window
- Delay: 5s before retry

**Logging:**
- Driver: json-file (Docker default)
- Max size: 20MB per file
- Max files: 5 (rotate automatically)

---

## 🚀 Production Setup

### Production Deployment Checklist

Before deploying to production, ensure:

- ✅ All passwords in `.env` are strong (min 16 chars with mixed case, numbers, symbols)
- ✅ `.env` file is NOT committed to Git (.gitignore entry exists)
- ✅ `.env` file has restricted permissions (chmod 600 on Linux/Mac)
- ✅ Database backups are configured and tested
- ✅ Health check endpoints are responding (curl localhost:8000/health)
- ✅ Resource limits are set (CPU, memory)
- ✅ Log rotation is enabled
- ✅ SSL/TLS certificates installed (if using HTTPS)
- ✅ External load balancer configured (if scaling horizontally)
- ✅ Monitoring and alerting configured

### Production Environment Variables

```env
# SECURITY - Use strong values!
SECRET_KEY=jK9$mP2@qL7!xR4&wN8yB3#sT6%vD1^cF5                # Min 32 chars
DB_PASSWORD=aK9$mP2@qL7!xR4&wN8yB3#sT6%vD1^cF5               # Min 16 chars
REDIS_PASSWORD=rD5#mK8$pQ2@tL9&vN3yB7*wF1^sH4                # Min 16 chars
INTERNAL_SERVICE_TOKEN=iS7#tK4@vP9$wL2&cN6%rD1^jF5$bM8       # Min 16 chars

# CONFIGURATION
JWT_ALGORITHM=HS256                                          # Or HS512
PYTHONPATH=.
CACHE_TTL=300                                                # 5 minutes

# LOGGING
LOG_LEVEL=INFO                                               # INFO, DEBUG, WARNING, ERROR
```

### Production Commands

```bash
# Start services in background
docker-compose up -d

# View logs (all services)
docker-compose logs -f

# View specific service logs
docker-compose logs -f gateway
docker-compose logs -f user-microservice

# Monitor container status
docker-compose ps

# Scale a service (if configured for replication)
docker-compose up -d --scale user-microservice=3

# Graceful shutdown
docker-compose down

# Remove all data (use with caution!)
docker-compose down -v
```

### Performance Tuning

**Gunicorn Workers (per service):**
- Current: 4 workers
- Calculation: (2 × CPU cores) + 1
- For 2-core server: 5 workers
- For 4-core server: 9 workers
- Adjust in `docker-compose.yml`

**Database Connection Pool:**
- Each service: max 20 connections
- Total pool: 20 connections × 5 services = 100
- Adjust in `app/database.py` if needed

**Redis Timeout:**
- Connection timeout: 5s
- Read timeout: 5s
- Adjust in `app/config.py` if needed

---

## ⚖️ Load Balancing

### Current Setup (Docker Compose)

**Type:** DNS-based load balancing (Docker built-in)

Docker Compose automatically provides:
- ✅ Service discovery via DNS (containers communicate by service name)
- ✅ Internal virtual IP for each service
- ✅ Automatic request distribution (round-robin) if service scaled

**How it works:**
1. Gateway tries to connect to `http://user-microservice:8001`
2. Docker DNS resolves to virtual IP
3. Requests automatically load balanced across containers

### Production Load Balancing

⚠️ **Current configuration lacks external load balancing!**

For production, add **Nginx** or **HAProxy** reverse proxy:

#### Option 1: Nginx Load Balancer (Recommended)

Create `nginx/nginx.conf`:
```nginx
upstream gateway {
    server gateway:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Add to `docker-compose.yml`:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - gateway
    networks:
      - app-network
```

#### Option 2: Service Replication

Scale services in `docker-compose.yml`:
```bash
# Start 3 instances of user-service
docker-compose up -d --scale user-microservice=3
```

Docker automatically distributes traffic across replicas.

#### Option 3: Kubernetes (Advanced)

For auto-scaling and advanced load balancing:
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
```

---

## 📡 API Endpoints

### Health Checks (Monitoring)

```
GET    /health         - Service health status (all services)
       Response: {"status": "healthy"}
```

### User Service (Port 8001)

```
POST   /api/v1/users/register          - Register new user
POST   /api/v1/users/login             - Login (returns JWT token)
GET    /api/v1/users/{user_id}         - Get user profile
PUT    /api/v1/users/{user_id}         - Update user profile
DELETE /api/v1/users/{user_id}         - Delete user
GET    /api/v1/users/search/{query}    - Search users
GET    /health                          - Health check
GET    /docs                            - API documentation (Swagger UI)
```

### Post Service (Port 8003)

```
POST   /api/v1/posts                   - Create new post
GET    /api/v1/posts/{post_id}         - Get post by ID
GET    /api/v1/posts/user/{user_id}    - Get user's posts
PUT    /api/v1/posts/{post_id}         - Update post
DELETE /api/v1/posts/{post_id}         - Delete post
GET    /health                          - Health check
GET    /docs                            - API documentation
```

### Follower Service (Port 8002)

```
POST   /api/v1/follow/{target_user_id} - Follow a user
DELETE /api/v1/follow/{target_user_id} - Unfollow a user
GET    /api/v1/followers/{user_id}     - Get user's followers
GET    /api/v1/following/{user_id}     - Get users this user follows
GET    /health                          - Health check
GET    /docs                            - API documentation
```

### Feed Service (Port 8004)

```
GET    /api/v1/feed                    - Get personalized feed
GET    /api/v1/feed/trending           - Get trending posts
GET    /api/v1/feed/recommendations    - Get recommendations
GET    /health                          - Health check
GET    /docs                            - API documentation
```

### API Gateway (Port 8000) - PUBLIC

```
GET    /health                          - Check all services
GET    /docs                            - Central API documentation
GET    /metrics                         - Service metrics (if enabled)

# Routes to services:
/api/users/*       →  User Service (8001)
/api/posts/*       →  Post Service (8003)
/api/followers/*   →  Follower Service (8002)
/api/feed/*        →  Feed Service (8004)
```

**Example Request:**
```bash
# Register user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secure123", "email": "john@example.com"}'

# Login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "secure123"}'

# Create post (requires JWT token)
curl -X POST http://localhost:8000/api/posts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!"}'
```

---

## � Managing Databases with pgAdmin

### What is pgAdmin?

**pgAdmin** is a web-based PostgreSQL database management tool. It provides a GUI to:
- Browse database schemas
- Execute SQL queries
- Manage users and permissions
- View tables, indexes, and sequences
- Export/import data

### Installation Options

#### Option 1: Download pgAdmin Locally (Windows)

1. **Download installer:**
   - Visit: https://www.pgadmin.org/download/pgadmin-4-windows/
   - Download latest stable version

2. **Install pgAdmin:**
   - Run the installer
   - Follow setup wizard
   - Note the password you set for `pgadmin4` account

3. **Launch pgAdmin:**
   - Start pgAdmin 4 from Start Menu
   - Opens at: http://localhost:5050
   - Login with email/password set during installation

#### Option 2: Docker pgAdmin (Easier Alternative)

Run pgAdmin in a Docker container:

```bash
docker run -d \
  --name pgadmin \
  -p 5050:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@example.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin123 \
  dpage/pgadmin4
```

Then access at: **http://localhost:5050**
- Email: `admin@example.com`
- Password: `admin123`

---

### Connecting to Your Databases

Once pgAdmin is running, connect to your Docker databases:

#### Step 1: Get Database Host IP

Since databases run in Docker containers, you need their internal network IP:

```bash
# Get the internal network gateway IP
docker network inspect microservices-fastapi_app-network | grep Gateway
```

**Output example:**
```
"Gateway": "172.18.0.1"
```

You can also use the **container name** directly as hostname (Docker DNS).

#### Step 2: Add Server Connection in pgAdmin

1. **Open pgAdmin:** http://localhost:5050

2. **Login** with your credentials

3. **Right-click "Servers"** → **Register** → **Server**

4. **Fill Connection Details:**

   **For User Database:**
   ```
   Name: user-microservice-db
   Host: docker-user-db          (or use 172.18.0.1)
   Port: 5432
   Username: postgres
   Password: (from .env DB_PASSWORD)
   Maintenance database: postgres
   ```

   **For Post Database:**
   ```
   Name: post-microservice-db
   Host: docker-post-db
   Port: 5432
   Username: postgres
   Password: (from .env DB_PASSWORD)
   Maintenance database: postgres
   ```

   **For Follower Database:**
   ```
   Name: follower-microservice-db
   Host: docker-follow-db
   Port: 5432
   Username: postgres
   Password: (from .env DB_PASSWORD)
   Maintenance database: postgres
   ```

5. **Click "Save"** → Server appears in left sidebar

6. **Browse tables:**
   - Expand Server → Databases → (database name) → Schemas → public → Tables

---

### Common pgAdmin Operations

#### View Table Data
1. Right-click table → **View/Edit Data** → **All Rows**
2. See all records with column headers

#### Run SQL Query
1. Right-click database → **Query Tool**
2. Write SQL and press F5 to execute:

```sql
-- Check users table
SELECT * FROM "user" LIMIT 10;

-- Check posts table
SELECT * FROM posts LIMIT 10;

-- Check follow relationships
SELECT * FROM follows LIMIT 10;

-- Count records
SELECT COUNT(*) FROM "user";
SELECT COUNT(*) FROM posts;
SELECT COUNT(*) FROM follows;
```

#### Export Data
1. Right-click table → **Backup**
2. Choose format (SQL, CSV, Custom)
3. Select destination folder

#### Monitor Database Performance
1. Tools → **Server** → **Properties** (bottom right)
2. View:
   - Database size
   - Table statistics
   - Connection info
   - Last vacuum/analyze time

---

### Troubleshooting pgAdmin Connections

**Problem: "Cannot connect to server"**
- ✅ Verify Docker containers are running: `docker-compose ps`
- ✅ Verify password matches `.env` DB_PASSWORD
- ✅ Check host name (use service name: `docker-user-db` not localhost)
- ✅ Ensure Docker network exists: `docker network ls`

**Problem: "Database not found"**
- ✅ Run migrations: `docker-compose exec user-microservice alembic upgrade head`
- ✅ Check if databases were created

**Problem: "Timeout connection"**
- ✅ Increase timeout in pgAdmin: Right-click server → Properties → Advanced → Connection timeout: 30

**Problem: "Port 5050 already in use"**
- ✅ Use different port: `-p 5051:80` in Docker command
- ✅ Or kill existing process using port 5050

---

## 🗄️ Database Migrations

### Running Migrations from Docker

```bash
# User Service
docker-compose exec user-microservice alembic upgrade head

# Post Service
docker-compose exec post-microservice alembic upgrade head

# Follower Service
docker-compose exec follower-microservice alembic upgrade head
```

### User Service
```bash
cd services/user-microservices
alembic upgrade head    # Apply migrations
alembic downgrade -1    # Rollback one migration
```

### Post Service
```bash
cd services/post-microservices
alembic upgrade head
```

### Follower Service
```bash
cd services/follower-microservice
alembic upgrade head
```

### Create New Migration
```bash
alembic revision --autogenerate -m "Add column description"
alembic upgrade head
```

---

## 🛠️ Development

### Local Testing

```bash
# Install dependencies
cd services/user-microservices
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --port 8001

# Run tests (if available)
pytest

# Code formatting
black .

# Linting
pylint app/
```

### Docker Compose Development

```bash
# Build images
docker-compose build

# Start with logs
docker-compose up

# Rebuild and restart single service
docker-compose up -d --build user-microservice

# Access container shell
docker-compose exec user-microservice bash

# View container logs
docker-compose logs -f --tail=100 user-microservice
```

---

## 📊 Monitoring & Logging

### Health Check Monitoring

```bash
# Test all services
curl http://localhost:8000/health

# Test individual services
curl http://localhost:8001/health  # User
curl http://localhost:8003/health  # Post
curl http://localhost:8002/health  # Follower
curl http://localhost:8004/health  # Feed
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service (last 100 lines)
docker-compose logs -f --tail=100 gateway

# Follow logs in real-time
docker-compose logs -f gateway user-microservice

# View historical logs
docker logs CONTAINER_ID
```

### Docker Stats (Resource Usage)

```bash
# Monitor CPU, memory, network
docker stats

# Watch specific container
docker stats gateway user-microservice
```

### Metrics Collection

If enabled, metrics available at:
```
GET http://localhost:9090/metrics  # Prometheus
```

---

## 🐛 Troubleshooting

### Service Not Starting

```bash
# Check logs
docker-compose logs gateway

# Common issues:
# 1. Port already in use
lsof -i :8000

# 2. Container crash loop
docker-compose up gateway  # See error output

# 3. Dependency not ready
# Wait for health checks: docker-compose logs -f
```

### Database Connection Issues

```bash
# Test database connection
docker-compose exec user-microservice \
  psql -h docker-user-db -U postgres -d user_db

# Check database is running
docker-compose ps | grep db

# View database logs
docker-compose logs docker-user-db
```

### Redis Connection Issues

```bash
# Test Redis connection
docker-compose exec docker-redis redis-cli ping

# Check Redis is running
docker-compose ps | grep redis

# View Redis logs
docker-compose logs docker-redis
```

### Health Check Failures

```bash
# Check service endpoint
curl -v http://localhost:8001/health

# If failing:
# 1. Service may still be starting (wait 30s)
# 2. Application error (check logs)
# 3. Port mismatch in config
```

### Memory Issues

```bash
# Check resource usage
docker stats

# If service OOM killed:
# Increase memory limit in docker-compose.yml
# Reduce worker count in CMD
```

### Clear Everything (Nuclear Option)

```bash
# Stop and remove all containers, volumes
docker-compose down -v

# Remove all images
docker rmi $(docker images -q)

# Restart fresh
docker-compose up -d
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gunicorn Documentation](https://gunicorn.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Redis Documentation](https://redis.io/documentation)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions welcome! Please follow:
1. Create feature branch: `git checkout -b feature/AmazingFeature`
2. Commit changes: `git commit -m 'Add AmazingFeature'`
3. Push to branch: `git push origin feature/AmazingFeature`
4. Open Pull Request

---

**Last Updated:** June 2026
**Version:** 1.0.0 (Production Ready)
- Post Service: http://localhost:8001/docs
- Feed Service: http://localhost:8002/docs

## 🗄️ Database Migrations

Each service uses **Alembic** for database migrations.

### Running Migrations

```bash
cd services/user-services
alembic upgrade head
```

### Creating a New Migration

```bash
cd services/user-services
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Migration History

Current migrations for each service:
- **User Service**: `67f141ac2709_add_created_at_to_users_remove_follower_.py`
- **Post Service**: `fa44fff5307d_create_posts_table.py`
- **Follower Service**: `baad22e76766_create_follows_table.py`

## 👨‍💻 Development

### Project Structure

```
microservices-fastapi/
├── gateway/                    # API Gateway service
│   ├── app/
│   │   ├── main.py
│   │   └── config.py
│   └── requirements.txt
├── services/
│   ├── user-services/         # User management service
│   ├── post-microservices/    # Post management service
│   ├── follower-microservice/ # Follower management service
│   └── feed-microservices/    # Feed aggregation service
├── shared/                     # Shared utilities (if any)
├── docker-compose.yml         # Docker composition
└── README.md                  # This file
```

### Adding a New Service

1. Create a new directory in `services/`
2. Create `app/main.py` with FastAPI app
3. Create `requirements.txt` with dependencies
4. Create `Dockerfile` for containerization
5. Add service to `docker-compose.yml`

### Running Tests

```bash
# For each service, run tests if available
cd services/user-services
pytest tests/
```

### Code Style

- Use **PEP 8** formatting
- Type hints recommended
- Docstrings for public functions/classes

## 🐳 Docker Deployment

### Build Services

```bash
docker-compose build
```

### Start Services

```bash
docker-compose up -d
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f user-service
```

### Stop Services

```bash
docker-compose down
```

### Clean Up (Remove volumes)

```bash
docker-compose down -v
```

### Docker Compose Services

| Service | Port | Image |
|---------|------|-------|
| user-service | 8000 | custom |
| post-service | 8001 | custom |
| feed-service | 8002 | custom |
| user-db | 5432 | postgres:15 |
| post-db | 5432 | postgres:15 |
| redis | 6379 | redis:7-alpine |

## 🔍 Troubleshooting

### Services won't start

1. **Check port availability:**
   ```bash
   netstat -ano | findstr :8000
   ```

2. **Check Docker logs:**
   ```bash
   docker-compose logs user-service
   ```

3. **Verify Docker is running:**
   ```bash
   docker version
   ```

### Database connection errors

1. **Check PostgreSQL is running:**
   ```bash
   docker-compose logs user-db
   ```

2. **Verify DATABASE_URL in `.env`**

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

### Redis connection errors

1. **Check Redis is running:**
   ```bash
   docker-compose logs redis
   ```

2. **Test Redis connection:**
   ```bash
   docker exec -it $(docker ps -q -f name=redis) redis-cli ping
   ```

### Authentication issues

1. **Check JWT_ALGORITHM in `.env`** (should be `HS256`)

2. **Verify SECRET_KEY is set** and consistent across services

3. **Check token expiration:** Tokens may have expired

### Inter-service communication

If services can't reach each other:

1. **Check service names** in docker-compose.yml
2. **Verify SERVICE_URL environment variables**
3. **Check Docker network:** `docker network ls`

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Redis Documentation](https://redis.io/documentation)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Created as a microservices architecture practice project.

---

**Last Updated:** 2024  
**Status:** Active Development