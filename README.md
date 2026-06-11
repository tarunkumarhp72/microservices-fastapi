# Social Media Feed System - Microservices Architecture

A scalable microservices-based social media platform built with **FastAPI**, featuring user management, post creation, follower relationships, and personalized feed generation with Redis caching.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Services](#services)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Database Migrations](#database-migrations)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)

## 🎯 Project Overview

This project demonstrates a modern microservices architecture for a social media platform. Each service is independently deployable, scalable, and manages its own database. The system features:

- **User Authentication & Management** - Secure user registration and profile management
- **Post Management** - Create, retrieve, and manage user posts
- **Social Relationships** - Follow/unfollow other users
- **Personalized Feed** - Aggregated feed of posts from followed users
- **Caching Layer** - Redis integration for performance optimization

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  API Gateway                         │
│            (Routing & Load Balancing)                │
└─────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬────────────┐
        │                │                │            │
        ▼                ▼                ▼            ▼
    ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌─────────┐
    │  User   │   │  Post   │   │ Follower │   │  Feed   │
    │ Service │   │ Service │   │ Service  │   │ Service │
    └─────────┘   └─────────┘   └──────────┘   └─────────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌──────────┐
    │ User DB │   │ Post DB │   │Follow DB │   │  Redis   │
    │(Postgres)  │(Postgres)  │(Postgres)  │   │ Cache    │
    └─────────┘   └─────────┘   └──────────┘   └──────────┘
```

## 🔧 Services

### 1. **User Service** (Port 8000)
Manages user accounts, authentication, and profiles.

**Key Features:**
- User registration and login
- JWT-based authentication
- User profile management
- Password hashing with bcrypt

**Database:** `userdb` (PostgreSQL)

### 2. **Post Service** (Port 8001)
Handles post creation, retrieval, and caching.

**Key Features:**
- Create and retrieve posts
- Post caching with Redis
- User validation via User Service
- Post metadata and timestamps

**Database:** `postdb` (PostgreSQL)

### 3. **Follower Service**
Manages user follow relationships.

**Key Features:**
- Follow/unfollow users
- Retrieve follower lists
- Check follow status

**Database:** PostgreSQL (shared or dedicated)

### 4. **Feed Service** (Port 8002)
Generates personalized feeds for users.

**Key Features:**
- Aggregate posts from followed users
- Cached feed results
- Real-time feed updates

**Dependencies:** User Service, Post Service, Redis

### 5. **API Gateway**
Single entry point for all client requests.

**Features:**
- Request routing
- Service discovery
- Health checks

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI |
| **ASGI Server** | Uvicorn |
| **ORM** | SQLAlchemy |
| **Database** | PostgreSQL 15 |
| **Cache** | Redis 7 |
| **Authentication** | JWT + Passlib |
| **Migrations** | Alembic |
| **Containerization** | Docker & Docker Compose |
| **Language** | Python 3.9+ |

## 📦 Prerequisites

- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
- OR
- **Python** 3.9+
- **PostgreSQL** 15
- **Redis** 7

## 🚀 Getting Started

### Option 1: Using Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd d:\Amandeep\self practise projects\social_media_feed_system\microservices-fastapi
   ```

2. **Create environment file** (`.env`):
   ```bash
   copy .env.example .env
   ```
   Or manually create `.env`:
   ```
   SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   ```

3. **Start all services:**
   ```bash
   docker-compose up -d
   ```

4. **Verify services are running:**
   ```bash
   docker-compose ps
   ```

5. **Access the services:**
   - User Service: http://localhost:8000
   - Post Service: http://localhost:8001
   - Feed Service: http://localhost:8002
   - API Gateway: http://localhost:3000 (if configured)

### Option 2: Local Development

1. **Install Python dependencies** for each service:
   ```bash
   # User Service
   cd services/user-services
   pip install -r requirements.txt

   # Post Service
   cd ../post-microservices
   pip install -r requirements.txt

   # Follower Service
   cd ../follower-microservice
   pip install -r requirements.txt

   # Feed Service
   cd ../feed-microservices
   pip install -r requirements.txt

   # Gateway
   cd ../../gateway
   pip install -r requirements.txt
   ```

2. **Start local PostgreSQL and Redis:**
   ```bash
   # Using Docker for just databases
   docker run -d --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   ```

3. **Run migrations:**
   ```bash
   cd services/user-services
   alembic upgrade head

   cd ../post-microservices
   alembic upgrade head

   cd ../follower-microservice
   alembic upgrade head
   ```

4. **Start each service** in separate terminals:
   ```bash
   # Terminal 1 - User Service
   cd services/user-services
   uvicorn app.main:app --reload --port 8000

   # Terminal 2 - Post Service
   cd services/post-microservices
   uvicorn app.main:app --reload --port 8001

   # Terminal 3 - Follower Service
   cd services/follower-microservice
   uvicorn app.main:app --reload --port 8002

   # Terminal 4 - Feed Service
   cd services/feed-microservices
   uvicorn app.main:app --reload --port 8002
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Authentication
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/userdb

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Service URLs
USER_SERVICE_URL=http://localhost:8000
POST_SERVICE_URL=http://localhost:8001
FEED_SERVICE_URL=http://localhost:8002
```

### Service Configuration Files

Each service has a `config.py` file for service-specific settings:

- `gateway/app/config.py` - API Gateway routing configuration
- `services/user-services/app/config.py` - User service settings
- `services/post-microservices/app/config.py` - Post service settings

## 📡 API Endpoints

### User Service

```
POST   /users/register          - Register new user
POST   /users/login             - Login user (returns JWT)
GET    /users/{user_id}         - Get user profile
PUT    /users/{user_id}         - Update user profile
GET    /health                  - Health check
```

### Post Service

```
POST   /posts                   - Create new post
GET    /posts/{post_id}         - Get post by ID
GET    /posts/user/{user_id}    - Get user's posts
DELETE /posts/{post_id}         - Delete post
GET    /health                  - Health check
```

### Follower Service

```
POST   /follow/{user_id}        - Follow a user
DELETE /follow/{user_id}        - Unfollow a user
GET    /followers/{user_id}     - Get user's followers
GET    /following/{user_id}     - Get users this user follows
GET    /health                  - Health check
```

### Feed Service

```
GET    /feed                    - Get personalized feed
GET    /feed/trending           - Get trending posts
GET    /health                  - Health check
```

**Note:** Detailed API documentation available at:
- User Service: http://localhost:8000/docs
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