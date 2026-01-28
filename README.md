# 🧠 Browser Agent (LLM + Playwright)

Интерактивный браузерный агент, который использует LLM для анализа страниц и управляет браузером через Playwright: кликает, вводит текст, навигирует и пошагово логирует свои действия.

Проект демонстрирует:
- архитектуру LLM-агента с инструментами (tools)
- работу с реальным браузером (Playwright)
- безопасную работу с API-ключами
- production-подобный CI/CD (lint, types, tests)

---

## ✨ Возможности

- 🌐 Управление **реальным браузером** (Chromium)
- 🧩 LLM-агент с **ограниченным набором инструментов**
- 👀 Снятие DOM-снапшотов и анализ кликабельных элементов
- 🧭 Пошаговое выполнение задач (`STEP 1`, `STEP 2`, …)
- 📝 Подробное логирование действий агента (как в UI)
- 🔐 Поддержка **persistent browser session** (авторизация сохраняется)
- ✅ CI с линтингом, типами и тестами

---

## 🏗 Архитектура

```text
src/
├── main.py        # Точка входа
├── agent.py       # LLM-агент (orchestration)
├── browser.py     # Обёртка над Playwright
├── tools.py       # Декларация доступных инструментов
├── prompt.py      # System / Developer промпты
└── safety.py      # Ограничения и guardrails

tests/
└── test_api.py    # Sanity / integration tests (без утечки секретов)
```

## Установка зависимостей

```bash
python -m venv venv
source venv\Scripts\activate

pip install -r requirements.txt
playwright install
```

## Настройка окружения 

```python
OPENAI_API_KEY=sk-xxxxxxxx
```

## Запуск агента

```bash
python -m src.main
```
---

```text
✅ Browser started (persistent session enabled).
Если нужно — залогинься вручную в открытом браузере.

Введите задачу агенту:
Открой https://playwright.dev/docs/auth
```

Агент будет:

- открывать браузер

- анализировать страницу

- логировать каждый шаг

- выполнять действия через tools

## 🧪 Тестирование

```bash
pytest -q
```

## 🧹 Линтинг и типы

```bash
ruff check . --fix
ruff format .
mypy src
```

## 🤖 CI / CD

GitHub Actions pipeline:

- ✅ Ruff (lint + format)

- ✅ MyPy (types)

- ✅ Pytest

- 🔐 Guardrails: .env и ключи не коммитятся

CI падает, если:

- нарушен стиль

- есть типовые ошибки

- тесты ломаются

## 🔐 Безопасность

- .env добавлен в .gitignore

- тесты не требуют ключей по умолчанию

- интеграционные проверки изолированы

- LLM не имеет прямого доступа к Playwright API

## 🧭 Цель проекта

Проект создавался как:

- демонстрация архитектурного мышления

- пример безопасной интеграции LLM + automation

- основа для расширяемых browser-агентов

Подходит для:

- тестовых заданий

- портфолио

- экспериментов с agent-based подходами


## 🧑‍💻 Автор

**Климентий Юдин**

GitHub: https://github.com/klimatroniks