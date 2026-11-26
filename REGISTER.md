# Реестр требований

*Сгенерирован `scripts/generate.py`, не редактировать вручную.*

Всего требований проекта: **14**. По статусам: approved 7, draft 1, implemented 2, proposed 3, verified 1

Приоритет по MoSCoW: M Must, S Should, C Could, W Won't.

| Область | Тип | Кол-во |
|---|---|---|
| x-platform | BR | 1 |
| x-platform | OPS | 4 |
| x-platform | SEC | 3 |
| x-records | FR | 1 |
| x-records | INT | 1 |
| x-records | NFR | 3 |
| x-records | SEC | 1 |

| ID | Название | Тип | Статус | Приоритет | Владелец | Область | Уточняет | ADR |
|---|---|---|---|---|---|---|---|---|
| [X-BR-001](requirements/x-platform/X-BR-001.md) | Мультиарендность с изоляцией данных клиентов | BR | approved | M | role-x-product-owners | x-platform |  |  |
| [X-FR-001](requirements/x-records/X-FR-001.md) | Экспорт записей клиента в CSV | FR | draft | C | role-x-records-engineers | x-records |  |  |
| [X-INT-001](requirements/x-records/X-INT-001.md) | Публикация событий записи через outbox | INT | approved | S | role-x-records-engineers | x-records |  |  |
| [X-NFR-001](requirements/x-records/X-NFR-001.md) | Доступность публичного API не ниже 99,9 % в месяц | NFR | approved | M | role-sre | x-records |  | ADR-001 |
| [X-NFR-002](requirements/x-records/X-NFR-002.md) | Время ответа API p95 ≤ 300 мс при 200 RPS | NFR | approved | S | role-x-records-engineers | x-records |  |  |
| [X-NFR-003](requirements/x-records/X-NFR-003.md) | Время хранится только в UTC с часовым поясом | NFR | verified | C | role-x-records-engineers | x-records |  |  |
| [X-OPS-001](requirements/x-platform/X-OPS-001.md) | Резервное копирование БД с RPO ≤ 15 минут | OPS | approved | M | role-platform-engineers | x-platform |  | ADR-002 |
| [X-OPS-002](requirements/x-platform/X-OPS-002.md) | Ежеквартальное учение по восстановлению с RTO ≤ 4 часа | OPS | proposed | S | role-platform-engineers | x-platform |  | ADR-002 |
| [X-OPS-003](requirements/x-platform/X-OPS-003.md) | Централизованное логирование со сроком хранения 30 дней | OPS | approved | S | role-sre | x-platform |  |  |
| [X-OPS-004](requirements/x-platform/X-OPS-004.md) | Обязательный CI-гейт перед слиянием в main | OPS | implemented | M | role-platform-engineers | x-platform |  |  |
| [X-SEC-001](requirements/x-platform/X-SEC-001.md) | Вход сотрудников только через SSO с MFA | SEC | implemented | M | role-security-engineers | x-platform | T-IAM-001, T-IAM-002 |  |
| [X-SEC-002](requirements/x-platform/X-SEC-002.md) | Секреты хранятся только в менеджере секретов | SEC | approved | M | role-security-engineers | x-platform | T-IAM-008 | ADR-001 |
| [X-SEC-003](requirements/x-records/X-SEC-003.md) | Персональные данные хранятся не дольше установленного срока | SEC | proposed | M | role-data-protection | x-records |  |  |
| [X-SEC-004](requirements/x-platform/X-SEC-004.md) | Сканирование образов и блокировка критических уязвимостей | SEC | proposed | S | role-security-engineers | x-platform |  |  |

## Принятые типовые требования

Каталог: выпуск 0.1.0, профили: ent-baseline. Подробности в `adoption.yaml`.

| ID | Название | Режим | Приоритет | Уровень | Чем уточнено, причина исключения |
|---|---|---|---|---|---|
| [T-IAM-001](requirements/_catalog/T-IAM-001.md) | Вход пользователей через корпоративный IdP по OpenID Connect | refine | M | MUST | X-SEC-001 |
| [T-IAM-002](requirements/_catalog/T-IAM-002.md) | Второй фактор для каждого интерактивного входа | refine | M | MUST | X-SEC-001 |
| [T-IAM-003](requirements/_catalog/T-IAM-003.md) | Роли и членство из групп поставщика идентичностей | inherit | M | MUST |  |
| [T-IAM-004](requirements/_catalog/T-IAM-004.md) | Изоляция чтения между проектами | inherit | M | MUST |  |
| [T-IAM-008](requirements/_catalog/T-IAM-008.md) | Секреты из внешнего хранилища секретов | refine | M | MUST | X-SEC-002 |
| [T-GOV-001](requirements/_catalog/T-GOV-001.md) | Журнал аудита действий пользователей и агентов | inherit | M | MUST |  |
| T-SEC-001 | Выгрузка журнала аудита в SIEM | waive |  | MUST | журнал аудита на первом этапе уходит в центральное логирование платформы, подключение SIEM запланировано на второй этап (до 2027-06-30, role-security-engineers) |
| [T-OBS-001](requirements/_catalog/T-OBS-001.md) | Метрики работы в формате OpenMetrics | inherit | S | SHOULD |  |
