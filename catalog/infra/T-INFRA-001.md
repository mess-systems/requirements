---
id: T-INFRA-001
title: Отказоустойчивое развёртывание в Kubernetes
type: INFRA
scope: infra
capability: k8s
status: proposed
version: 1
owner: role-platform-engineers
level: SHOULD
applies_to:
- corp
- product
params:
  failover_seconds:
    type: integer
    default: 60
    unit: с
    description: допустимый перерыв при отказе узла
source:
- 'Разбор Tencent LoopForge v0.4.3: корпоративный пробел ENT-18'
basis:
- k8s-disruptions
realizations:
- kubernetes
- k3s
links:
  adr: []
  depends_on: []
  verified_by: []
---
# T-INFRA-001: Отказоустойчивое развёртывание в Kubernetes

## Требование
`req~T-INFRA-001~1`

Система должна разворачиваться в кластере Kubernetes в несколько экземпляров каждого компонента, обрабатывающего запросы, без единой точки отказа на уровне приложения.

Needs: impl, itest
Tags: k8s

## Обоснование
Развёртывание одним контейнером на одной машине останавливает работу команд при обновлении или сбое узла.

## Критерии приёмки
- Манифесты или пакет развёртывания поставляются вместе с релизом
- Отказ одного узла кластера не прерывает обработку запросов дольше `{failover_seconds}` секунд
- Обновление версии выполняется без остановки обслуживания

## Параметры

| Параметр | По умолчанию | Смысл |
|---|---|---|
| `failover_seconds` | 60 с | допустимый перерыв при отказе узла |
