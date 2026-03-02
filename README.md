# Mariane API

[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

[![Coverage](https://codecov.io/gh/i-defranca/mariane-api/graph/badge.svg?token=LNC0J557JV)](https://codecov.io/gh/i-defranca/mariane-api)

A Django REST API for tracking menstrual cycles and daily metrics, aiming to provide personalized insights and predictions.

## Tech Stack
- Python 3.12.2 (with pyenv)

##  Requirements
- Python 3.12.2 (with pyenv)

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
```

## Roadmap
- Add Docker
- Add Django
- Add GitHub CI workflow
- Add tests and coverage
- Add JWT auth
- Add API docs
- Add black/ruff to CI workflow
- Add slow query/request logging
- Add caching
- Add anomaly detection (eg. large cycle variance)
