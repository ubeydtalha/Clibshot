# ClipShot Backend

Backend API for ClipShot platform.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# Development server
uvicorn src.main:app --reload --port 8000

# Or use Python directly
python src/main.py
```

## API Documentation

Visit http://localhost:8000/api/docs for interactive API documentation.
