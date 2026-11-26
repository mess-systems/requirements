---
id: T-SEC-001
title: Выгрузка журнала аудита в SIEM
type: SEC
scope: sec
capability: siem
status: proposed
version: 1
owner: role-security-engineers
level: MUST
applies_to:
- corp
- product
params:
  export_delay_minutes:
    type: integer
    default: 5
    unit: мин
    description: максимальная задержка доставки записи в SIEM
source:
- 'Разбор Tencent LoopForge v0.4.3: корпоративный пробел ENT-07'
basis:
- rfc5424
- nist-800-92
realizations:
- wazuh
links:
  adr: []
  depends_on: []
  verified_by: []
---
# T-SEC-001: Выгрузка журнала аудита в SIEM

## Требование
`req~T-SEC-001~1`

Система должна передавать записи журнала аудита в корпоративную SIEM в машиночитаемом формате.

Needs: impl, itest
Tags: siem

## Обоснование
Журнал, который читают только внутри системы, не участвует в корреляции событий и не переживает компрометацию самой системы.

## Критерии приёмки
- Записи уходят в SIEM потоком или пакетами с задержкой не больше `{export_delay_minutes}` минут
- Формат описан в документации, поля совпадают с полями журнала аудита
- Сбой доставки виден в метриках и не приводит к потере записей

## Параметры

| Параметр | По умолчанию | Смысл |
|---|---|---|
| `export_delay_minutes` | 5 мин | максимальная задержка доставки записи в SIEM |
