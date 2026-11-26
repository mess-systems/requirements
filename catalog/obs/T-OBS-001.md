---
id: T-OBS-001
title: Метрики работы в формате OpenMetrics
type: OBS
scope: obs
capability: metrics
status: proposed
version: 1
owner: role-sre
level: SHOULD
applies_to:
- corp
- product
source:
- 'Разбор Tencent LoopForge v0.4.3: корпоративный пробел ENT-19'
basis:
- openmetrics
realizations:
- prometheus
- opentelemetry
links:
  adr: []
  depends_on: []
  verified_by: []
---
# T-OBS-001: Метрики работы в формате OpenMetrics

## Требование
`req~T-OBS-001~1`

Система должна публиковать метрики своей работы в формате OpenMetrics.

Needs: impl, itest
Tags: metrics

## Обоснование
Проверка «живой или нет» не показывает очереди, ошибки и задержки, по которым видна деградация.

## Критерии приёмки
- Опубликованы метрики числа запросов, ошибок и задержек по каждому API
- Опубликованы метрики очередей и фоновых задач
- Доступ к метрикам ограничен сетью или аутентификацией
