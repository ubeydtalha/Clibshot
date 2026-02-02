# Development Environment Setup

This guide will help you set up your development environment for ClipShot.

## Prerequisites

### Required Software

- **Node.js** 20+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/))
- **Rust** 1.70+ ([Install](https://rustup.rs/))
- **Git** ([Download](https://git-scm.com/))

### Optional Tools

- **Docker** & Docker Compose (for containerized development)
- **VS Code** (recommended IDE)
- **PostgreSQL** (if not using Docker)
- **Redis** (if not using Docker)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ubeydtalha/Clibshot.git
cd Clibshot
```

### 2. Backend Setup

```bash
cd apps/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the backend
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd apps/desktop

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Tauri Development

```bash
cd apps/desktop

# Install Tauri CLI
npm install -g @tauri-apps/cli

# Run Tauri in development mode
npm run tauri dev
```

## Docker Development

### Start all services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379
- Backend API on port 8000

### View logs

```bash
docker-compose logs -f
```

### Stop all services

```bash
docker-compose down
```

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Rust Analyzer
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- ESLint
- Prettier

Settings (`.vscode/settings.json`):
```json
{
  "editor.formatOnSave": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

## Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://clipshot:password@localhost:5432/clipshot

# Redis
REDIS_URL=redis://localhost:6379

# Environment
ENV=development
DEBUG=true

# Security
SECRET_KEY=your-secret-key-here

# AI Services (optional)
OPENAI_API_KEY=your-key-here
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

## Troubleshooting

### Port already in use

If you get "port already in use" errors:

```bash
# Find and kill process using port 8000
# On Unix/macOS:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Python virtual environment issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Rust compilation errors

```bash
# Update Rust
rustup update

# Clean build cache
cd apps/desktop/src-tauri
cargo clean
```

### Node modules issues

```bash
# Clean and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- [Contributing Guide](CONTRIBUTING.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Plugin Development](PLUGIN_DEVELOPMENT.md)
- [API Reference](../api/README.md)
