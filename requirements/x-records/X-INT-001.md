---
id: X-INT-001
title: Публикация событий записи через outbox
type: INT
status: approved
priority: P2
owner: role-x-records-engineers
scope: x-records
category: integration
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr: []
  depends_on: []
  verified_by: []
version: 1
---
# X-INT-001: Публикация событий записи через outbox

## Требование
`req~X-INT-001~1`

Изменения записи публикуются в шину событий через transactional outbox; потребитель получает событие не позже чем через 10 с.

Needs: impl, itest

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Схема события версионирована
- Повторная доставка идемпотентна
- Метрика задержки outbox
