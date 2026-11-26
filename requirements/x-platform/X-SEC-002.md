---
id: X-SEC-002
title: Секреты хранятся только в менеджере секретов
type: SEC
status: approved
priority: M
owner: role-security-engineers
scope: x-platform
category: secrets
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr:
  - ADR-001
  depends_on: []
  verified_by: []
version: 1
refines:
- T-IAM-008
---
# X-SEC-002: Секреты хранятся только в менеджере секретов

## Требование
`req~X-SEC-002~1`

Пароли, токены и ключи хранятся в менеджере секретов и доставляются в рантайм; в git и образах секретов нет.

Needs: impl, itest

Covers:
- req~T-IAM-008~1

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Сканер секретов в CI блокирует PR
- Приложения читают секреты при старте или через sidecar
- Ротация ключевых секретов не реже 90 дней
