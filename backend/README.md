# CodeMentor Backend

## Overview
Backend API for the CodeMentor LLM Coding Tutor Platform built with Quart (async Flask).

## Technology Stack
- **Framework**: Quart (async Flask)
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+ with SQLAlchemy ORM
- **Cache**: Redis 7+
- **Authentication**: JWT with OAuth 2.0
- **API Docs**: OpenAPI/Swagger

## Project Structure
```
backend/
├── src/
│   ├── api/            # API route handlers
│   ├── models/         # Database models
│   ├── services/       # Business logic services
│   ├── middleware/     # Request/response middleware
│   └── utils/          # Utility functions
├── tests/              # Test suite
├── config/             # Configuration files
├── requirements.txt    # Python dependencies
└── app.py             # Application entry point
```

## Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Initialize Database
```bash
alembic upgrade head
```

### 5. Run Development Server
```bash
python app.py
```

## API Documentation
Once running, access API documentation at:
- Swagger UI: http://localhost:5000/docs
- OpenAPI Spec: http://localhost:5000/openapi.json

## Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Development

### Code Quality
```bash
# Format code
black src/

# Lint code
pylint src/

# Type checking
mypy src/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## License
Internal - All Rights Reserved
