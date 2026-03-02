# Music Streaming GraphQL API (Restructured)

A high-performance, asynchronous GraphQL API for music streaming services, built with FastAPI, Strawberry, and SQLAlchemy.

## 📄 Documentation
For detailed architectural info, schema details, and API examples, see [DOCUMENTATION.md](./DOCUMENTATION.md).

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.12+
- PostgreSQL running locally

### 2. Setup
```bash
# Install dependencies
python3 -m venv music_streaming_v2/venv
./music_streaming_v2/venv/bin/pip install -r music_streaming_v2/requirements.txt

# Create database and run migrations
createdb music_db
export PYTHONPATH=$PYTHONPATH:.
./music_streaming_v2/venv/bin/alembic -c music_streaming_v2/alembic.ini upgrade head

# Seed initial data
./music_streaming_v2/venv/bin/python3 music_streaming_v2/seed.py
```

### 3. Run
```bash
./music_streaming_v2/venv/bin/uvicorn music_streaming_v2.main:app --reload
```
Open **[http://localhost:8000/graphql](http://localhost:8000/graphql)** to explore the API.
