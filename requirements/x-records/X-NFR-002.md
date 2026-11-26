---
id: X-NFR-002
title: Время ответа API p95 ≤ 300 мс при 200 RPS
type: NFR
status: approved
priority: S
owner: role-x-records-engineers
scope: x-records
category: performance
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr: []
  depends_on:
  - X-NFR-001
  verified_by: []
version: 1
---
# X-NFR-002: Время ответа API p95 ≤ 300 мс при 200 RPS

## Требование
`req~X-NFR-002~1`

Чтение каталога отвечает за p95 ≤ 300 мс и p99 ≤ 800 мс при нагрузке 200 RPS.

Needs: impl, itest

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Нагрузочный тест в CI в окружении `stg` перед релизом
- Регресс > 10 % блокирует релиз
- Метрики латентности в дашборде
