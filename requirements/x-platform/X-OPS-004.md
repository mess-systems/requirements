---
id: X-OPS-004
title: Обязательный CI-гейт перед слиянием в main
type: OPS
status: implemented
priority: M
owner: role-platform-engineers
scope: x-platform
category: ci
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr: []
  depends_on: []
  verified_by: []
version: 1
---
# X-OPS-004: Обязательный CI-гейт перед слиянием в main

## Требование
`req~X-OPS-004~1`

Слияние в main возможно только после зелёного CI (сборка, тесты, линтеры, проверка требований) и одобрения человеком.

Needs: impl

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Branch protection: required checks + 1 approve
- Прямой push в main запрещён
- Статус проверок виден в PR
