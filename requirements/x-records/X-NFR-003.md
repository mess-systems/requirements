---
id: X-NFR-003
title: Время хранится только в UTC с часовым поясом
type: NFR
status: verified
priority: P3
owner: role-x-records-engineers
scope: x-records
category: data-model
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr: []
  depends_on: []
  verified_by:
  - tests/test_timestamps.py::test_tz_columns
version: 1
---
# X-NFR-003: Время хранится только в UTC с часовым поясом

## Требование
`req~X-NFR-003~1`

Все отметки времени в БД хранятся как `timestamptz`, отображаются в часовом поясе пользователя.

Needs: impl, utest

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Линтер миграций запрещает TEXT/timestamp без зоны для времени
- Отображение учитывает часовой пояс профиля
