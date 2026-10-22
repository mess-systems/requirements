---
id: X-SEC-001
title: Вход сотрудников только через SSO с MFA
type: SEC
status: implemented
priority: P1
owner: role-security-engineers
scope: x-platform
category: access
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr: []
  depends_on: []
  verified_by: []
version: 1
---
# X-SEC-001: Вход сотрудников только через SSO с MFA

## Требование
`req~X-SEC-001~1`

Все внутренние веб-интерфейсы и консоли доступны только после входа через корпоративный IdP (OIDC/SAML) с MFA.

Needs: impl, itest

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Локальные учётки отключены, кроме break-glass
- MFA обязательна для всех групп
- Отзыв доступа в IdP закрывает сессии ≤ 15 мин
