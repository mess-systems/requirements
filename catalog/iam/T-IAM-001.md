---
id: T-IAM-001
title: Вход пользователей через корпоративный IdP по OpenID Connect
type: IAM
scope: iam
capability: sso
status: proposed
version: 1
owner: role-security-engineers
level: MUST
applies_to:
- corp
- product
params:
  revoke_minutes:
    type: integer
    default: 15
    unit: мин
    description: максимальное время до потери доступа после отключения у поставщика идентичностей
source:
- 'Разбор Tencent LoopForge v0.4.3: корпоративный пробел ENT-01'
basis:
- oidc-core
- rfc7636
- oidc-rp-logout
- oidc-backchannel-logout
realizations:
- keycloak
- zitadel
links:
  adr: []
  depends_on: []
  verified_by: []
---
# T-IAM-001: Вход пользователей через корпоративный IdP по OpenID Connect

## Требование
`req~T-IAM-001~1`

Система должна принимать интерактивный вход пользователей только через корпоративный поставщик идентичностей по OpenID Connect с потоком Authorization Code и PKCE.

Needs: impl, itest
Tags: sso

## Обоснование
Один поставщик идентичностей даёт одну точку для MFA, блокировки и отзыва доступа. Вход по заголовку от прокси или локальные пароли создают второй путь, который легко забыть закрыть.

## Критерии приёмки
- Вход без перенаправления к поставщику идентичностей невозможен, кроме аварийной учётной записи, описанной в ADR
- Запрос авторизации содержит `code_challenge` с методом `S256`
- Выход из системы завершает сессию и у поставщика идентичностей (RP-Initiated Logout)
- Пользователь, отключённый у поставщика идентичностей, теряет доступ не позже чем через `{revoke_minutes}` минут

## Параметры

| Параметр | По умолчанию | Смысл |
|---|---|---|
| `revoke_minutes` | 15 мин | максимальное время до потери доступа после отключения у поставщика идентичностей |
