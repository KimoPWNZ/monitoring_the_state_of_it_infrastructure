# Monitoring the State of IT Infrastructure

A compact web-based monitoring system built with **FastAPI**, **SQLite**, and a lightweight scheduler. The application monitors HTTP endpoints, stores check results, registers incidents, sends notifications, and builds summary reports.

## Features
- Object registry (nodes/services)
- Periodic checks with per-object intervals
- Status evaluation (normal / warning / critical)
- Incident journal and notification log
- Summary reports for a date range
- Simple web UI

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- APScheduler
- Jinja2

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000

## Configuration
You can override defaults with environment variables:

- `APP_HOST` (default: 127.0.0.1)
- `APP_PORT` (default: 8000)
- `DB_PATH` (default: monitoring.db)
- `DEFAULT_CHECK_INTERVAL` (default: 60)
- `REQUEST_TIMEOUT` (default: 5)
- `WARNING_RESPONSE_TIME` (default: 1000)
- `CRITICAL_RESPONSE_TIME` (default: 3000)
- `EMAIL_NOTIFICATIONS` (default: false)
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM`, `SMTP_TO`

## Notes
- Checks are HTTP GET requests. For non-HTTP endpoints you can still store objects, but checks will be marked as unavailable.
- Reports are generated on demand from stored data.
