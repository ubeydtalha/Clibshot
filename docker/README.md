# Docker Development Environment for ClipShot

## Quick Start

Start all services:
```bash
docker-compose up -d
```

Stop all services:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

## Services

### PostgreSQL (port 5432)
- Database: `clipshot`
- User: `clipshot`
- Password: `clipshot_dev_password`

### Redis (port 6379)
- Default configuration
- Used for caching and session storage

### Backend (port 8000)
- FastAPI application
- Auto-reload enabled in development
- API docs: http://localhost:8000/docs

## Development

### Rebuild containers
```bash
docker-compose build
```

### Reset database
```bash
docker-compose down -v
docker-compose up -d
```

### Execute commands in containers
```bash
# Backend shell
docker-compose exec backend bash

# PostgreSQL shell
docker-compose exec postgres psql -U clipshot -d clipshot

# Redis CLI
docker-compose exec redis redis-cli
```

## Production

For production deployment, use environment-specific compose files:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
