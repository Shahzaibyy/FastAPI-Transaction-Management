# 🚀 FastAPI Transaction Management System

Production-ready FastAPI backend with JWT authentication, PostgreSQL, and Docker.

## ✨ Features

- ✅ JWT Authentication (Access + Refresh tokens)
- ✅ User Registration & Login
- ✅ Transaction CRUD with advanced filtering
- ✅ Financial Analytics
- ✅ PostgreSQL + SQLAlchemy 2.x
- ✅ Alembic Migrations
- ✅ Docker + Docker Compose
- ✅ Rate Limiting
- ✅ 100% Type Hints
- ✅ Comprehensive Tests
- ✅ SOLID Principles
- ✅ OpenAPI/Swagger Docs

## 🏗️ Architecture

```
project/
├── app/
│   ├── core/          # Config, security, dependencies
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── repositories/  # Data access layer
│   ├── routers/       # API routes
│   └── main.py
├── alembic/           # Database migrations
├── tests/             # Test suite
├── Dockerfile         # Docker container definition
├── docker-compose.yml # Multi-container orchestration
├── .dockerignore      # Docker build exclusions
└── requirements.txt
```

## 🐳 Docker Setup & Configuration

### Docker Files Structure

This project includes two Docker configuration files:

#### 1. **Dockerfile** - Application Container

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Features:**
- Based on Python 3.11 slim image for minimal size
- Installs PostgreSQL client for database operations
- Caches dependencies layer for faster rebuilds
- Exposes port 8000 for the FastAPI application
- Uses uvicorn as the ASGI server

#### 2. **docker-compose.yml** - Multi-Container Orchestration

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: transaction_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: transaction_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Redis Cache (optional)
  redis:
    image: redis:7-alpine
    container_name: transaction_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # FastAPI Application
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: transaction_api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/transaction_db
      SECRET_KEY: 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
      ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 15
      DEBUG: "True"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local

networks:
  app-network:
    driver: bridge
```

**Services Breakdown:**

1. **db (PostgreSQL)**
   - Image: `postgres:15-alpine` (lightweight)
   - Port: 5432
   - Health checks every 10 seconds
   - Persistent volume for data storage

2. **redis (Optional Cache)**
   - Image: `redis:7-alpine`
   - Port: 6379
   - Used for rate limiting and caching

3. **api (FastAPI Application)**
   - Built from local Dockerfile
   - Port: 8000
   - Auto-reloads on code changes
   - Waits for database health check
   - Environment variables configured

#### 3. **.dockerignore** - Optimize Build

```dockerignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Database
*.db
*.sqlite
*.sqlite3

# Docker
.dockerignore
Dockerfile
docker-compose.yml

# Git
.git/
.gitignore

# Documentation
README.md
docs/

# Logs
*.log
```

## 🚀 Quick Start with Docker

### Option 1: Docker Compose (Recommended - Full Stack)

```bash
# 1. Clone the repository
git clone <repo-url>
cd transaction-api

# 2. Create environment file
cp .env.example .env

# 3. Start all services (PostgreSQL + Redis + API)
docker-compose up -d

# 4. Check service status
docker-compose ps

# 5. View logs
docker-compose logs -f api

# 6. Access the application
# API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Option 2: Docker Only (API Container)

```bash
# 1. Build the image
docker build -t transaction-api:latest .

# 2. Run the container (with SQLite)
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./transaction_db.db \
  -e SECRET_KEY=your-secret-key \
  --name transaction-api \
  transaction-api:latest

# 3. View logs
docker logs -f transaction-api

# 4. Stop container
docker stop transaction-api

# 5. Remove container
docker rm transaction-api
```

### Option 3: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Initialize database
alembic upgrade head

# Run server
uvicorn app.main:app --reload
```

## 🛠️ Docker Commands Reference

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v

# Rebuild containers
docker-compose up -d --build

# View logs
docker-compose logs -f [service_name]

# Execute commands in container
docker-compose exec api bash
docker-compose exec db psql -U postgres -d transaction_db
```

### Database Operations

```bash
# Run migrations in container
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d transaction_db

# Backup database
docker-compose exec db pg_dump -U postgres transaction_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres transaction_db < backup.sql
```

### Testing in Docker

```bash
# Run tests in container
docker-compose exec api pytest

# Run tests with coverage
docker-compose exec api pytest --cov=app tests/

# Run specific test file
docker-compose exec api pytest tests/test_auth.py -v
```

### Container Management

```bash
# View running containers
docker-compose ps

# View container resource usage
docker stats

# Inspect container
docker inspect transaction_api

# Remove unused images and containers
docker system prune -a

# View container logs (last 100 lines)
docker-compose logs --tail=100 api
```

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/transaction_db
# For SQLite: DATABASE_URL=sqlite:///./transaction_db.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
APP_NAME=Transaction Management API
DEBUG=True
ALLOWED_HOSTS=*

# Logging
LOG_LEVEL=INFO

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 API Examples

### 1. Register User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login?email=user@example.com&password=SecurePass123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create Transaction
```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 250.50,
    "type": "credit",
    "description": "Salary deposit",
    "timestamp": "2025-01-15T10:30:00"
  }'
```

### 4. List Transactions (with filters)
```bash
curl "http://localhost:8000/transactions?type=credit&min_amount=100&page=1&limit=20" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Summary
```bash
curl "http://localhost:8000/transactions/summary" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "total_credits": 12500.50,
  "total_debits": 8500.25,
  "current_balance": 4000.25,
  "transaction_count": 45,
  "avg_transaction": 245.67
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v

# In Docker
docker-compose exec api pytest -v
```

## 🗄️ Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# In Docker
docker-compose exec api alembic upgrade head
```

## 🔒 Security Features

- ✅ Bcrypt password hashing (12 rounds)
- ✅ JWT with expiry (15min access, 7d refresh)
- ✅ Password strength validation (8+ chars, 1 uppercase, 1 number)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Rate limiting (10 requests/minute per IP)
- ✅ CORS configuration
- ✅ Environment-based secrets
- ✅ HTTPOnly cookies support
- ✅ Input validation with Pydantic V2

## 📊 Transaction Filters

```
?type=credit|debit          # Filter by transaction type
?start_date=2025-01-01      # Transactions after date
?end_date=2025-12-31        # Transactions before date
?min_amount=100             # Minimum amount
?max_amount=1000            # Maximum amount
?page=1                     # Page number (default: 1)
?limit=20                   # Items per page (default: 20, max: 100)
```

## 🏭 Production Deployment

### Docker Production Build

```bash
# Build production image
docker build -t transaction-api:prod -f Dockerfile .

# Run with production settings
docker run -d \
  -p 8000:8000 \
  --env-file .env.production \
  --restart unless-stopped \
  --name transaction-api-prod \
  transaction-api:prod

# Or with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Production Environment Variables
```env
DATABASE_URL=postgresql://user:password@production-host:5432/transaction_db
SECRET_KEY=super-secure-secret-key-minimum-32-characters-long
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
LOG_LEVEL=WARNING
```

### Docker Compose Production (docker-compose.prod.yml)

```yaml
version: '3.8'

services:
  api:
    image: transaction-api:prod
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: "False"
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Health Checks & Monitoring

```bash
# Health check endpoint
curl http://localhost:8000/health

# Docker health status
docker-compose ps

# Container resource usage
docker stats transaction_api

# View application logs
docker-compose logs -f --tail=100 api
```

## 📈 Performance Optimization

- ✅ Connection pooling with SQLAlchemy
- ✅ Database indexes on user_id and email
- ✅ Pagination for large datasets
- ✅ Optimized aggregation queries
- ✅ Redis caching (optional)
- ✅ Async endpoints where applicable
- ✅ Docker multi-stage builds (optional)
- ✅ Efficient query filtering

## 🛠️ Code Quality

```bash
# Format code
black .
isort .

# Linting
pylint app/

# Type checking
mypy app/

# Security scanning
bandit -r app/
```

## 🐛 Troubleshooting

### Common Issues

**1. Port 8000 already in use**
```bash
# Find process using port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"
```

**2. Database connection error**
```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

**3. Permission denied errors**
```bash
# Fix volume permissions
sudo chown -R $USER:$USER .

# Or run with sudo
sudo docker-compose up -d
```

**4. Container keeps restarting**
```bash
# View container logs
docker-compose logs api

# Check container status
docker-compose ps

# Inspect container
docker inspect transaction_api
```

**5. Clean slate restart**
```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild and start
docker-compose up -d --build
```

## 📝 License

MIT License - feel free to use in your projects!

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📧 Support

For issues or questions:
- Open a GitHub issue
- Check existing documentation
- Review Docker logs: `docker-compose logs -f`

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

Built with ❤️ using FastAPI, Docker, and PostgreSQL

**Version**: 1.0.0  
**Last Updated**: December 2024
