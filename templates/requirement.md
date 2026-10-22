---
id: <PREFIX>-<TYPE>-<NNN>
title: <Кратко, что должно быть верно>
type: FR
status: draft
priority: P3
owner: role-x-records-engineers
scope: x-records
category: export
source:
- Типовой пример blueprint (выдуманный продукт x компании mess.systems)
links:
  adr: []
  depends_on: []
  verified_by: []
version: 1
---
# <PREFIX>-<TYPE>-<NNN>: Экспорт записей клиента в CSV

## Требование
`req~<PREFIX>-<TYPE>-<NNN>~1`

Пользователь с ролью клиента может выгрузить свои записи за период в CSV (UTF-8, разделитель `;`).

Needs: impl, utest

## Обоснование
Типовое требование для старта; адаптируйте пороги под свой проект.

## Критерии приёмки
- Период не больше 1 года
- В выгрузке только данные своего клиента
- Выгрузка > 10 000 строк выполняется асинхронно
