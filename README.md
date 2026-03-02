# Mariane API

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

[![Coverage](https://codecov.io/gh/i-defranca/mariane-api/graph/badge.svg?token=LNC0J557JV)](https://codecov.io/gh/i-defranca/mariane-api)

A Django REST API for tracking menstrual cycles and daily metrics, aiming to provide personalized insights and predictions.

## Tech Stack
- Python 3.12.2 (with pyenv)
- Django
- MySQL (Dockerized)
- Docker / Docker Compose v2
- kool.dev (optional)

## Architecture
- Django app managed with pyenv and venv
- MySQL running inside a Docker container
- Environment variables loaded from `.env` file

##  Requirements
- Python 3.12.2 (with pyenv)
- Docker
- Docker Compose v2

## Setup Instructions

### 1) Clone the repository
```bash
git clone https://github.com/i-defranca/COM200 karte
# go the the project directory
cd karte
```

### 2) Python Setup
```bash
pyenv install 3.12.2
pyenv local 3.12.2

python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### 3) Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```
> Fill .env with database credentials.

### 4) Database Container Setup
Start the container:
```bash
docker compose up --build
# or
kool start -b
```

To stop the container:
```bash
docker compose down
# or
kool stop
```

To check container status:
```bash
docker compose ps
# or
kool status
```
> The database will be available according to the variables set in your .env file.

### 5) Run the Application
```bash
python manage.py migrate
python manage.py runserver
```
> The development server will start on http://localhost:8000/

## Development Workflow
- Start the database container
- Activate the virtual environment
- Run migrations
- Start the development server

## Roadmap
- Add GitHub CI workflow
- Add tests and coverage
- Add JWT auth
- Add API docs
- Add black/ruff to CI workflow
- Add slow query/request logging
- Add caching
- Add anomaly detection (eg. large cycle variance)
