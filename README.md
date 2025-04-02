# Тестируем веб-сервисы на Python

Данный проект содержит веб-сервис на Python (FastAPI), покрытый тестами (unit, integration, e2e). Сервис представляет собой простой калькулятор с функцией кэширования результатов в БД.

Проект служит примером для статьи про тестирование веб-сервисов на Python.

Поддерживаемая версия Python – 3.11.

## Установка зависимостей

```shell
poetry env use 3.11
poetry install
```

## Конфигурация

```ini
# src/.env

DB_HOST=localhost
DB_PORT=5432
DB_NAME=calculator
DB_USER=<username>
DB_PASS=<password>
```

## Активация виртуального окружения

```shell
$(poetry env activate)
```

## Применение миграций

> Из директории *src*

```shell
alembic upgrade head
```

## Запуск приложения

> Из директории *src*

Для разработки:

```shell
fastapi dev
```

или в production-режиме:

```shell
fastapi run
```

## Запуск тестов

> Из корневой директории проекта

```shell
pytest
```

Отчет о покрытии тестами появится в директории `htmlcov`
