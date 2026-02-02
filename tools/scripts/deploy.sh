#!/bin/bash
# Deployment script for ClipShot

set -e

echo "🚀 Deploying ClipShot..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Environment (development, staging, production)
ENV=${1:-"development"}

echo -e "${BLUE}Environment: ${ENV}${NC}"

case $ENV in
  development)
    echo -e "${BLUE}📦 Deploying to development...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✓ Development environment started${NC}"
    echo "Backend: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    ;;
    
  staging)
    echo -e "${BLUE}📦 Deploying to staging...${NC}"
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
    echo -e "${GREEN}✓ Staging environment deployed${NC}"
    ;;
    
  production)
    echo -e "${YELLOW}⚠️  Production deployment${NC}"
    read -p "Are you sure you want to deploy to production? (yes/no) " -n 3 -r
    echo
    if [[ $REPLY =~ ^yes$ ]]; then
      docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
      echo -e "${GREEN}✓ Production environment deployed${NC}"
    else
      echo "Deployment cancelled"
      exit 1
    fi
    ;;
    
  *)
    echo -e "${RED}Unknown environment: ${ENV}${NC}"
    echo "Usage: ./deploy.sh [development|staging|production]"
    exit 1
    ;;
esac

# Health check
echo -e "${BLUE}🏥 Running health checks...${NC}"
sleep 5
if curl -f http://localhost:8000/health 2>/dev/null; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Backend health check failed${NC}"
fi

echo -e "${GREEN}✅ Deployment complete!${NC}"
