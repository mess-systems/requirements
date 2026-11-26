---
id: T-OBS-001
title: Метрики работы в формате OpenMetrics
type: OBS
status: proposed
owner: role-sre
scope: obs
capability: metrics
level: SHOULD
source:
- 'catalog-v0.1.0: catalog/obs/T-OBS-001.md'
version: 1
adoption:
  mode: inherit
  catalog_release: 0.1.0
  priority: S
---
<!-- Сгенерировано scripts/generate.py из каталога по adoption.yaml. Не редактировать. -->
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
