# Мониторинг состояния ИТ‑инфраструктуры

Веб‑ориентированная система мониторинга на **FastAPI** с хранением в **SQLite**, планировщиком проверок, журналом инцидентов и расширенной поддержкой множества типов проверок.

**Язык:** Python 76.9% • HTML 15.3% • CSS 7.2% • Dockerfile 0.6%

## 🎯 Возможности

### ✅ Реализовано
- **Реестр объектов мониторинга** (узлы/сервисы)
- **HTTP-проверки** с измерением времени ответа
- **Ресурсные метрики** (CPU, RAM, диск)
- **Определение статуса** (normal / warning / critical)
- **Журнал инцидентов и уведомлений**
- **Отчёты** за выбранный период + экспорт (CSV/PDF)
- **REST API** для интеграции
- **Базовая аутентификация** (HTTP Basic)
- **Docker и docker-compose**

### 📋 Типы проверок (в разработке)

| Тип | Описание | Метрики | Статус |
|-----|---------|---------|--------|
| `http` | HTTP GET запросы | Доступность, время ответа | ✅ |
| `icmp` | ICMP Ping | Доступность, время отклика | 🔄 |
| `tcp` | TCP Port Check | Доступность порта | 🔄 |
| `snmp` | SNMP Polling | Переменные OID | 🔄 |
| `local` | Локальный агент | CPU, RAM, диск | 🔄 |
| `http_extended` | HTTP + ресурсы | HTTP + CPU, RAM, диск | 🔄 |

**Легенда:** ✅ Реализовано • 🔄 В разработке

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

Создайте файл `.env` в корне (все параметры необязательны):

```env
# Приложение
APP_HOST=127.0.0.1
APP_PORT=8000
DB_PATH=monitoring.db

# Проверки
DEFAULT_CHECK_INTERVAL=60
REQUEST_TIMEOUT=5

# HTTP-проверки (пороги времени ответа в мс)
WARNING_RESPONSE_TIME=1000
CRITICAL_RESPONSE_TIME=3000

# Ресурсные метрики (пороги в %)
WARNING_CPU_LOAD=70
CRITICAL_CPU_LOAD=90

WARNING_RAM_USAGE=80
CRITICAL_RAM_USAGE=95

WARNING_DISK_USAGE=80
CRITICAL_DISK_USAGE=95

# Аутентификация
AUTH_ENABLED=false
AUTH_USERNAME=admin
AUTH_PASSWORD=admin

# Email-уведомления
EMAIL_NOTIFICATIONS=false
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=login
SMTP_PASSWORD=password
SMTP_FROM=monitor@example.com
SMTP_TO=admin@example.com

# SNMP (опционально)
SNMP_VERSION=2c
SNMP_COMMUNITY=public
SNMP_TIMEOUT=5
```

---

# 📌 REST API

### Объекты мониторинга
```
GET    /api/objects              — Список объектов
POST   /api/objects              — Создать объект
DELETE /api/objects/{id}         — Удалить объект
```

### Инциденты
```
GET    /api/incidents            — История инцидентов
```

### Отчёты
```
GET    /api/reports?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
GET    /api/metrics/incidents?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
GET    /api/reports/export?format=csv|pdf&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
```

### Примеры запросов

**Создать HTTP-проверку:**
```bash
curl -X POST http://127.0.0.1:8000/api/objects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Google DNS",
    "object_type": "http",
    "address": "https://8.8.8.8",
    "check_interval": 60,
    "warning_threshold": 1000,
    "critical_threshold": 3000
  }'
```

**Создать локальную проверку ресурсов:**
```bash
curl -X POST http://127.0.0.1:8000/api/objects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Local Server",
    "object_type": "local",
    "address": "localhost",
    "check_interval": 30
  }'
```

**Получить отчёт за месяц:**
```bash
curl "http://127.0.0.1:8000/api/reports/export?format=pdf&date_from=2025-01-01&date_to=2025-02-01" \
  -o report.pdf
```

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

# 📂 Структура проекта

```
monitoring_the_state_of_it_infrastructure/
├── app/
│   ├── models.py                # SQLAlchemy ORM модели
│   ├── schemas.py               # Pydantic схемы
│   ├── config.py                # Конфигурация из .env
│   ├── auth.py                  # HTTP Basic аутентификация
│   ├── database.py              # Подключение к БД
│   ├── main.py                  # FastAPI приложение
│   ├── routes/                  # API endpoints
│   │   ├── objects.py           # CRUD объектов
│   │   ├── incidents.py         # Работа с инцидентами
│   │   ├── reports.py           # Отчёты и экспорт
│   │   └── api.py               # REST API
│   ├── services/                # Бизнес-логика
│   │   ├── scheduler.py         # Планировщик проверок (APScheduler)
│   │   ├── monitoring.py        # Основной цикл мониторинга
│   │   ├── check_service.py     # Координация проверок
│   │   ├── checks/              # Модули проверок
│   │   │   ├── http_check.py    # HTTP-проверки
│   │   │   ├── icmp_check.py    # ICMP/Ping
│   │   │   ├── tcp_check.py     # TCP порты
│   │   │   ├── snmp_check.py    # SNMP
│   │   │   └── resource_check.py # CPU, RAM, диск
│   │   ├── status_service.py    # Определение статуса
│   │   ├── incident_service.py  # Управление инцидентами
│   │   ├── notification_service.py # Уведомления
│   │   ├── report_service.py    # Построение отчётов
│   │   └── export_service.py    # CSV/PDF экспорт
│   ├── static/                  # CSS, JavaScript
│   └── templates/               # HTML шаблоны
├── tests/                       # Unit-тесты
├── alembic/                     # Миграции БД
├── requirements.txt             # Python зависимости
├── requirements-dev.txt         # Dev зависимости
├── Dockerfile                   # Docker образ
├── docker-compose.yml           # Docker Compose
└── README.md                    # Этот файл
```

---

# 🔧 Зависимости

### Основные
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **Pydantic** — валидация данных
- **APScheduler** — планировщик задач
- **Requests** — HTTP клиент
- **psutil** — ресурсные метрики (CPU, RAM, диск)

### Дополнительные (в разработке)
- **icmplib** или **ping3** — ICMP/Ping
- **pysnmp** — SNMP
- **fpdf** — PDF экспорт

### Development
- **pytest** — тестирование
- **black** — форматирование кода

---

# 📝 Примечания

### Определение статуса
- **normal** — все метрики в норме
- **warning** — хотя бы одна метрика превышает warning threshold
- **critical** — хотя бы одна метрика превышает critical threshold

### Периодичность проверок
- Проверки выполняются в фоновом процессе с интервалом, указанным для каждого объекта
- По умолчанию интервал = 60 секунд
- Минимальный интервал = 10 секунд

### Для не-HTTP объектов (в разработке)
- ICMP: требуется права root для отправки ping-пакетов
- TCP: проверяется доступность порта (соединение)
- SNMP: требуется конфигурация агента на целевой машине
- Local: работает на машине, где запущено приложение

### История и отчёты
- Все проверки сохраняются в БД
- Отчёты строятся по исторических данных
- Можно выгрузить CSV или PDF за любой период

---

# 🤝 Контрибьютинг

Вклады приветствуются! Пожалуйста:
1. Fork репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменений (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

# 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле `LICENSE`.

---

# ℹ️ Справка

**Автор:** [KimoPWNZ](https://github.com/KimoPWNZ)  
**Репозиторий:** [monitoring_the_state_of_it_infrastructure](https://github.com/KimoPWNZ/monitoring_the_state_of_it_infrastructure)  
**Версия:** 1.1.0  
**Статус:** Активная разработка (🔄 добавляются новые типы проверок)
