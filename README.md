# Campaign Budget Tracker

A minimal full-stack campaign budget tracking tool built for the Brainlabs technical task.

The app lets account managers add campaigns and view their budget, spend, and current status in a simple single-page UI.

## Tech stack

- Backend: Django + Django REST Framework
- Frontend: Vue 3 + Vite
- Database: SQLite
- Containerisation: Docker Compose

## Features

- Add campaigns with name, budget, and spend
- View campaigns in a table
- Edit or delete campaigns
- Automatically calculated status:
  - `On track`: spend is below 90% of budget
  - `At risk`: spend is at least 90% of budget
  - `Overspent`: spend is greater than budget

Status is derived from budget and spend rather than stored in the database, avoiding duplicated state that could become stale.

## Running with Docker

Prerequisite: Docker Desktop or Docker Engine with Docker Compose.

From the project root:

```bash
docker compose up --build
```

If your Docker installation uses the older Compose command, run:

```bash
docker-compose up --build
```

Then open:

```text
http://localhost:5173
```

The backend API is available at:

```text
http://localhost:8000/api/campaigns/
```

The backend container runs migrations automatically on startup, then serves the Django API with Gunicorn.

Campaign data is stored in a Docker-managed SQLite volume, so data survives container restarts/rebuilds unless the volume is removed.

## Running locally without Docker

### Backend

Install Python dependencies with uv:

```bash
uv sync
```

Run migrations:

```bash
uv run python manage.py migrate
```

Start Django:

```bash
uv run python manage.py runserver
```

### Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, usually:

```text
http://localhost:5173
```

The frontend proxies `/api` requests to Django at `http://127.0.0.1:8000` during local development.

## Running tests

From the project root:

```bash
uv run python manage.py test campaigns
```

## API endpoints

Using Django REST Framework viewsets:

```text
GET     /api/campaigns/       List campaigns
POST    /api/campaigns/       Create campaign
GET     /api/campaigns/{id}/  Retrieve campaign
PATCH   /api/campaigns/{id}/  Partially update campaign
PUT     /api/campaigns/{id}/  Fully update campaign
DELETE  /api/campaigns/{id}/  Delete campaign
```

Example create request:

```bash
curl -X POST "http://127.0.0.1:8000/api/campaigns/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Google Ads","budget":"1000.00","spend":"950.00"}'
```

Example response:

```json
{
  "id": 1,
  "name": "Google Ads",
  "budget": "1000.00",
  "spend": "950.00",
  "status": "warning",
  "created_at": "2026-06-11T21:57:28.458034Z"
}
```

## Design notes

The brief asked for a minimal app, so the implementation intentionally avoids extra product features such as pacing, charts, ad platform integrations, authentication, or alerting.

A few possible future improvements:

- Campaign start/end dates and pacing calculations
- Spend history snapshots and charts
- Client/account manager user permissions
- Alerts when campaigns become at risk or overspent
- Integration with ad platform APIs
- Broader API and frontend test coverage

## Development note

This project uses Django/DRF conventions: models for persisted data, serializers for validation/input-output shaping, and viewsets for CRUD endpoints. The frontend is a small Vue single-page app consuming the Django API.
# spend_tracker
