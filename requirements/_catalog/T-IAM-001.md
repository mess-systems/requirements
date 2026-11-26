---
id: T-IAM-001
title: Вход пользователей через корпоративный IdP по OpenID Connect
type: IAM
status: proposed
owner: role-security-engineers
scope: iam
capability: sso
level: MUST
source:
- 'catalog-v0.1.0: catalog/iam/T-IAM-001.md'
version: 1
adoption:
  mode: refine
  catalog_release: 0.1.0
  priority: M
  params:
    revoke_minutes: 15
  by:
  - X-SEC-001
---
<!-- Сгенерировано scripts/generate.py из каталога по adoption.yaml. Не редактировать. -->
# T-IAM-001: Вход пользователей через корпоративный IdP по OpenID Connect

## Требование
`req~T-IAM-001~1`

Система должна принимать интерактивный вход пользователей только через корпоративный поставщик идентичностей по OpenID Connect с потоком Authorization Code и PKCE.

Needs: req
Tags: sso

## Обоснование
Один поставщик идентичностей даёт одну точку для MFA, блокировки и отзыва доступа. Вход по заголовку от прокси или локальные пароли создают второй путь, который легко забыть закрыть.

## Критерии приёмки
- Вход без перенаправления к поставщику идентичностей невозможен, кроме аварийной учётной записи, описанной в ADR
- Запрос авторизации содержит `code_challenge` с методом `S256`
- Выход из системы завершает сессию и у поставщика идентичностей (RP-Initiated Logout)
- Пользователь, отключённый у поставщика идентичностей, теряет доступ не позже чем через `15` минут
