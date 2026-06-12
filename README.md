# Campaign Budget Tracker

A minimal full-stack campaign budget tracking tool built for the Brainlabs technical task.

The app lets account managers add campaigns and view their budget, spend, and current status in a simple single-page UI.

## Running with Docker

From the project root:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5173
```

The backend API is available at:

```text
http://localhost:8000/api/campaigns/
```

The backend container runs migrations automatically on startup.

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
  - `On track`: spend is below 90% of budget. This can be altered dependent on what the account team deems to be "risky"
  - `At risk`: spend is at least 90% of budget. As above for altering threshold based on domain experience. 
  - `Overspent`: spend is greater than budget

Status is derived from budget and spend rather than stored in the database, avoiding duplicated state that could become stale.


## Design notes

The brief asked for a minimal app, so the implementation intentionally avoids extra product features such as pacing, charts, ad platform integrations, authentication, or alerting.

A few possible future improvements:

- Campaign start/end dates and pacing calculations.
- Spend history snapshots and charts.
- Client/account manager user permissions.
- Alert Notifications when campaigns become at risk or overspent.
- Integration with ad platform APIs (Google Ads, Meta, TikTok etc).
- Expand on tests for model status rules and API validation.
- Month-on-month spend differences. 
- Year-on-year spend differences. 
- Client-specific trackers. i 
- Forecasting spend at specific rates. 
- Forecasting performance metrics from spends. 

## Development note

This project uses Django/DRF conventions: models for persisted data, serializers for validation/input-output shaping, and viewsets for CRUD endpoints. The frontend is a small Vue single-page app consuming the Django API.

