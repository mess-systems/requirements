---
id: T-<DOM>-<NNN>
title: <Кратко, какое поведение должно быть верно>
type: <DOM>               # код домена naming-standard в верхнем регистре
scope: <dom>              # тот же код в нижнем регистре = каталог catalog/<dom>/
capability: <code>        # код возможности naming-standard в этом домене
status: draft
version: 1                # = ревизия OpenFastTrace ~N
owner: role-<group>
level: MUST               # сила формулировки: MUST, SHOULD или MAY (RFC 2119, RFC 8174)
applies_to: [corp, product]
params:
  <name>: {type: integer, default: 15, unit: мин, description: <что ограничивает>}
source:
- <откуда требование: разбор продукта, раздел blueprint, ADR>
basis: []                 # ключи sources.yaml
checks: []                # строки матриц проверок blueprints, например ai-enablement#M3
realizations: []          # карточки tech-radar, справочно
links: {adr: [], depends_on: [], verified_by: []}
---
# T-<DOM>-<NNN>: <Название>

## Требование
`req~T-<DOM>-<NNN>~1`

Система должна <одно проверяемое поведение без названий продуктов; порог через {name}>.

Needs: impl, itest
Tags: <code>

## Обоснование
<Какой риск закрывает требование и почему оно нужно любому решению этого класса.>

## Критерии приёмки
- <Проверяемый пункт>
- <Проверяемый пункт с порогом `{name}`>

## Параметры

| Параметр | По умолчанию | Смысл |
|---|---|---|
| `<name>` | 15 мин | <что ограничивает> |
