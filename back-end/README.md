## Prerequisites

- Python 3.12+
- bash
- make
- Docker and Docker Compose (recommended)

## Quick Start

Use either of the following local or Docker instructions.

### Docker (recommended)

#### Setup

- Run `make docker-init` to build the container
- Run `make docker-dev` to start the containers (app + PostgreSQL)

In another terminal:

- Run `make docker-reset-db` to set up the database
- Run `make docker-seed-db` to seed the database

#### Run

- Access the app at `http://localhost:9000`
  - there is a health check route at `http://localhost:9000/health_checks`
  - to view available routes run `docker compose run --rm app flask routes`

#### Test

- `make docker-test`

### Local

#### Setup

- Ensure PostgreSQL is running on `localhost:5432` (or use Docker: `docker compose up db`)
- `python3.12 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `cp .env.example .env`
- `make reset-db`
- `make seed-db`

#### Run

- Run `make dev` to start the app server
- Access the app at `http://localhost:9000`

#### Test

- `make test`

## API Routes

| Method | Path | Description |
|---|---|---|
| GET | `/health_checks` | Health check |
| POST | `/checkouts` | Create a checkout |
| GET | `/checkouts/<id>` | Get a checkout |
| POST | `/checkout_items` | Add an item to a checkout |
| PUT | `/checkout_items/<id>` | Update a checkout item |
| POST | `/checkouts/<id>/discount` | Apply a discount code |
| DELETE | `/checkouts/<id>/discount` | Remove a discount (not yet implemented) |
