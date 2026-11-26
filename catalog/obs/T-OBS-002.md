---
id: T-OBS-002
title: Правила оповещения для типовых отказов
type: OBS
scope: obs
capability: alerts
status: proposed
version: 1
owner: role-sre
level: SHOULD
applies_to:
- corp
- product
params:
  alert_minutes:
    type: integer
    default: 5
    unit: мин
    description: время до оповещения о недоступности
source:
- 'Разбор Tencent LoopForge v0.4.3: корпоративный пробел ENT-19'
basis:
- openmetrics
realizations:
- alertmanager
- grafana
links:
  adr: []
  depends_on: []
  verified_by: []
---
# T-OBS-002: Правила оповещения для типовых отказов

## Требование
`req~T-OBS-002~1`

Система должна поставляться с правилами оповещения о недоступности, росте ошибок и переполнении очередей.

Needs: impl, itest
Tags: alerts

## Обоснование
Без готовых правил каждая команда пишет их заново и узнаёт об отказе от пользователей.

## Критерии приёмки
- Правила оповещения входят в релиз и ссылаются на метрики из T-OBS-001
- Недоступность сервиса вызывает оповещение не позже чем через `{alert_minutes}` минут
- Для каждого правила есть описание действий дежурного

## Параметры

| Параметр | По умолчанию | Смысл |
|---|---|---|
| `alert_minutes` | 5 мин | время до оповещения о недоступности |
