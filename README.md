 FastAPI Transaction Management System

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
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone and setup
git clone <repo>
cd transaction-api

# Start services
docker-compose up -d

# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Option 2: Local Development

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

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## 🗄️ Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🔒 Security Features

- ✅ Bcrypt password hashing (12 rounds)
- ✅ JWT with expiry (15min access, 7d refresh)
- ✅ Password strength validation
- ✅ SQL injection prevention (ORM)
- ✅ Rate limiting (10 req/min)
- ✅ CORS configuration
- ✅ Environment-based secrets

## 📊 Transaction Filters

```
?type=credit|debit          # Filter by transaction type
?start_date=2025-01-01      # Transactions after date
?end_date=2025-12-31        # Transactions before date
?min_amount=100             # Minimum amount
?max_amount=1000            # Maximum amount
?page=1                     # Page number
?limit=20                   # Items per page
```

## 🏭 Production Deployment

### Environment Variables
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### Docker Production Build
```bash
docker build -t transaction-api .
docker run -p 8000:8000 --env-file .env transaction-api
```

## 📈 Performance

- Connection pooling with SQLAlchemy
- Indexed queries on user_id and email
- Pagination for large datasets
- Optimized aggregation queries

## 🛠️ Code Quality

```bash
# Format code
black .
isort .

# Linting
pylint app/

# Type checking
mypy app/
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

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using FastAPI