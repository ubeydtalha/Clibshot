# Deployment Guide

This guide covers deploying ClipShot in various environments.

## Deployment Options

1. **Desktop Application** - Distributed as installers
2. **Backend Service** - Deployed as API server
3. **Full Stack** - Desktop app + Backend service

## Desktop Application

### Building Installers

#### Windows

```bash
cd apps/desktop
npm run tauri build

# Output: src-tauri/target/release/bundle/msi/ClipShot_*.msi
```

System Requirements:
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB disk space

#### macOS

```bash
cd apps/desktop
npm run tauri build

# Output: src-tauri/target/release/bundle/dmg/ClipShot_*.dmg
```

System Requirements:
- macOS 10.15+ (Catalina or later)
- 4GB RAM minimum
- 500MB disk space

#### Linux

```bash
cd apps/desktop
npm run tauri build

# Outputs:
# - AppImage: src-tauri/target/release/bundle/appimage/
# - deb: src-tauri/target/release/bundle/deb/
```

System Requirements:
- Ubuntu 20.04+ or equivalent
- 4GB RAM minimum
- 500MB disk space

### Code Signing

#### Windows
```bash
# Using signtool
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com ClipShot.msi
```

#### macOS
```bash
# Sign the app
codesign --force --deep --sign "Developer ID Application: Your Name" ClipShot.app

# Create signed DMG
hdiutil create -volname "ClipShot" -srcfolder ClipShot.app -ov -format UDZO ClipShot.dmg
codesign --force --sign "Developer ID Application: Your Name" ClipShot.dmg
```

## Backend Service

### Docker Deployment

#### Single Container

```bash
# Build image
docker build -f docker/backend.Dockerfile -t clipshot-backend .

# Run container
docker run -d \
  --name clipshot-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/clipshot \
  -e REDIS_URL=redis://redis:6379 \
  -v /data/clipshot:/data \
  clipshot-backend
```

#### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale backend=3
```

### Production Configuration

#### Environment Variables

```env
# Production settings
ENV=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@db.example.com:5432/clipshot
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://redis.example.com:6379
REDIS_PREFIX=clipshot:

# Security
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=api.clipshot.com,clipshot.com
CORS_ORIGINS=https://clipshot.com

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=https://your-sentry-dsn

# File Storage
STORAGE_PATH=/data/clips
MAX_CLIP_SIZE_MB=500

# AI Services
OPENAI_API_KEY=your-key
AI_MODEL=gpt-4
```

#### Nginx Configuration

```nginx
upstream clipshot_backend {
    server localhost:8000;
    # Add more servers for load balancing
    # server localhost:8001;
    # server localhost:8002;
}

server {
    listen 80;
    server_name api.clipshot.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.clipshot.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.clipshot.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.clipshot.com/privkey.pem;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Proxy to backend
    location / {
        proxy_pass http://clipshot_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Static files
    location /static/ {
        alias /var/www/clipshot/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Large file uploads
    client_max_body_size 500M;
}
```

### Database Setup

#### PostgreSQL

```bash
# Create database
createdb clipshot

# Create user
createuser clipshot

# Grant privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE clipshot TO clipshot;"

# Run migrations
cd apps/backend
alembic upgrade head
```

#### Backup Strategy

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/clipshot"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
pg_dump clipshot > "$BACKUP_DIR/db_$DATE.sql"

# Compress
gzip "$BACKUP_DIR/db_$DATE.sql"

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### Monitoring

#### Health Checks

```python
# apps/backend/main.py

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health/db")
async def db_health():
    try:
        # Test database connection
        await database.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

#### Logging

```python
# Configure logging
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/clipshot/app.log')
    ]
)
```

### Scaling

#### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  backend:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

#### Load Balancing

Use nginx or a dedicated load balancer (HAProxy, AWS ELB, etc.)

### Security Checklist

- [ ] Enable HTTPS/TLS
- [ ] Set secure headers
- [ ] Use strong secrets
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Regular security updates
- [ ] Implement authentication
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Use least privilege access

### Maintenance

#### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Restart services
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

#### Monitoring Commands

```bash
# View container status
docker-compose ps

# View resource usage
docker stats

# View logs
docker-compose logs -f backend

# Database queries
docker-compose exec postgres psql -U clipshot

# Redis monitoring
docker-compose exec redis redis-cli monitor
```

## Cloud Platforms

### AWS

- **EC2** for compute
- **RDS** for PostgreSQL
- **ElastiCache** for Redis
- **S3** for clip storage
- **CloudFront** for CDN

### Google Cloud

- **Compute Engine** for VMs
- **Cloud SQL** for PostgreSQL
- **Memorystore** for Redis
- **Cloud Storage** for clips
- **Cloud CDN** for delivery

### Azure

- **Virtual Machines** for compute
- **Azure Database** for PostgreSQL
- **Azure Cache** for Redis
- **Blob Storage** for clips
- **Azure CDN** for delivery

## Troubleshooting

### Common Issues

**Issue**: High memory usage
```bash
# Check memory
docker stats

# Adjust limits
docker update --memory 2g clipshot-backend
```

**Issue**: Database connection errors
```bash
# Check connectivity
docker-compose exec backend nc -zv postgres 5432

# View logs
docker-compose logs postgres
```

**Issue**: Slow response times
```bash
# Check database queries
docker-compose exec postgres psql -c "SELECT * FROM pg_stat_activity;"

# Check Redis
docker-compose exec redis redis-cli INFO stats
```

## Support

For deployment issues:
- GitHub Issues: https://github.com/ubeydtalha/Clibshot/issues
- Discussions: https://github.com/ubeydtalha/Clibshot/discussions
- Discord: https://discord.gg/clipshot
