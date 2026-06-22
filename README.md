# Мониторинг состояния ИТ‑инфраструктуры

Веб‑приложение для мониторинга ИТ‑инфраструктуры на **FastAPI** с хранением данных в **SQLite**. Проект включает реестр объектов мониторинга, планировщик проверок, журнал инцидентов, уведомления и отчёты.

**Стек:** Python • FastAPI • SQLAlchemy • SQLite • Jinja2 • APScheduler • Docker

## Возможности

### Уже реализовано
- реестр объектов мониторинга (узлы, сервисы)
- HTTP‑проверки с измерением времени ответа
- мониторинг ресурсных метрик: CPU, RAM, диск
- определение статуса: `normal`, `warning`, `critical`
- журнал инцидентов и уведомлений
- отчёты за выбранный период
- экспорт отчётов в `CSV` и `PDF`
- REST API для интеграции
- базовая HTTP‑аутентификация
- запуск через Docker / Docker Compose

### Типы проверок
- `http` — HTTP GET запросы
- `icmp` — ICMP Ping
- `tcp` — проверка TCP‑порта
- `snmp` — опрос SNMP
- `local` — локальный агент с метриками системы
- `http_extended` — HTTP + системные метрики

## Быстрый запуск

### Вариант 1. Через Docker
```bash
docker compose up --build
```

После запуска приложение будет доступно в браузере:

```text
http://127.0.0.1:8000
```

### Вариант 2. Локально
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Откройте в браузере:
   ```text
   http://127.0.0.1:8000
   ```

## Запуск одной командой

Если Docker уже установлен, достаточно одной команды:

```bash
docker compose up --build
```

Если нужен локальный запуск одной командой, используйте:

```bash
pip install -r requirements.txt && uvicorn app.main:app --reload
```

## API

### Объекты мониторинга
- `GET /api/objects` — список объектов
- `POST /api/objects` — создать объект
- `DELETE /api/objects/{id}` — удалить объект

### Инциденты
- `GET /api/incidents` — история инцидентов

### Уведомления
- `GET /api/notifications` — список уведомлений

### Отчёты
- `GET /api/reports?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`
- `GET /api/reports?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD&object_id=1`

## Конфигурация

При необходимости можно создать файл `.env` в корне проекта. Основные параметры:

- `DB_PATH` — путь к SQLite‑базе данных
- `AUTH_ENABLED` — включить HTTP Basic аутентификацию
- `AUTH_USERNAME` — имя пользователя
- `AUTH_PASSWORD` — пароль
- `DEFAULT_CHECK_INTERVAL` — интервал проверок по умолчанию
- `REQUEST_TIMEOUT` — таймаут HTTP‑проверок
- `WARNING_RESPONSE_TIME` — порог предупреждения для HTTP‑проверок
- `CRITICAL_RESPONSE_TIME` — критический порог для HTTP‑проверок

## Структура проекта

- `app/` — основное приложение FastAPI
- `app/routes/` — страницы и API‑маршруты
- `app/static/` — статические файлы
- `app/templates/` — HTML‑шаблоны
- `alembic/` — миграции базы данных
- `requirements.txt` — зависимости Python
- `Dockerfile` — контейнеризация приложения
- `docker-compose.yml` — запуск через Docker Compose

## Лицензия

Проект распространяется под лицензией MIT.
