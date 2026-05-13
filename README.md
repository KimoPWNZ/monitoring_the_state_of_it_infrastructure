# Мониторинг состояния ИТ‑инфраструктуры

Веб‑ориентированная система мониторинга на **FastAPI** с хранением в **SQLite**, планировщиком проверок, журналом инцидентов и отчётностью.

## Возможности
- Реестр объектов мониторинга (узлы/сервисы)
- Периодические проверки с интервалом для каждого объекта
- Определение статуса (normal / warning / critical)
- Журнал инцидентов и уведомлений
- Отчёты за выбранный период + экспорт (CSV/PDF)
- REST API
- Базовая аутентификация
- Docker и docker-compose

---

# ✅ Быстрый запуск (Linux/macOS/Windows)

## 1) Клонировать репозиторий
```bash
git clone https://github.com/KimoPWNZ/monitoring_the_state_of_it_infrastructure.git
cd monitoring_the_state_of_it_infrastructure
```

## 2) Создать и активировать виртуальное окружение
**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3) Установить зависимости
```bash
pip install -r requirements.txt
```

## 4) Запустить приложение
```bash
uvicorn app.main:app --reload
```

## 5) Открыть интерфейс в браузере
```
http://127.0.0.1:8000
```

---

# 🚀 Запуск через Docker

```bash
docker compose up --build
```

Открыть:
```
http://127.0.0.1:8000
```

---

# ⚙️ Конфигурация (через .env)

Создайте файл `.env` в корне (необязательно):

```env
APP_HOST=127.0.0.1
APP_PORT=8000
DB_PATH=monitoring.db

DEFAULT_CHECK_INTERVAL=60
REQUEST_TIMEOUT=5
WARNING_RESPONSE_TIME=1000
CRITICAL_RESPONSE_TIME=3000

AUTH_ENABLED=false
AUTH_USERNAME=admin
AUTH_PASSWORD=admin

EMAIL_NOTIFICATIONS=false
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=login
SMTP_PASSWORD=password
SMTP_FROM=monitor@example.com
SMTP_TO=admin@example.com
```

---

# 📌 REST API

- `GET /api/objects`
- `POST /api/objects`
- `DELETE /api/objects/{id}`
- `GET /api/incidents`
- `GET /api/reports?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`
- `GET /api/metrics/incidents?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`
- `GET /api/reports/export?format=csv|pdf&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`

---

# 🧪 Тесты

```bash
pip install -r requirements-dev.txt
pytest -q
```

---

# 🗃️ Миграции (Alembic)

```bash
alembic upgrade head
```

---

# Примечания
- Проверки выполняются HTTP GET запросами.
- Для не‑HTTP объектов проверки будут считаться недоступными.
- Отчёты строятся по сохранённым данным (истории наблюдений).
