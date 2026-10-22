# Реестр требований

*Сгенерирован `scripts/generate.py`, не редактировать вручную.*

Всего: **14**. По статусам: approved 7, draft 1, implemented 2, proposed 3, verified 1

| Область | Тип | Кол-во |
|---|---|---|
| x-platform | BR | 1 |
| x-platform | OPS | 4 |
| x-platform | SEC | 3 |
| x-records | FR | 1 |
| x-records | INT | 1 |
| x-records | NFR | 3 |
| x-records | SEC | 1 |

| ID | Название | Тип | Статус | Приоритет | Владелец | Область | ADR |
|---|---|---|---|---|---|---|---|
| [X-BR-001](requirements/x-platform/X-BR-001.md) | Мультиарендность с изоляцией данных клиентов | BR | approved | P1 | role-x-product-owners | x-platform |  |
| [X-FR-001](requirements/x-records/X-FR-001.md) | Экспорт записей клиента в CSV | FR | draft | P3 | role-x-records-engineers | x-records |  |
| [X-INT-001](requirements/x-records/X-INT-001.md) | Публикация событий записи через outbox | INT | approved | P2 | role-x-records-engineers | x-records |  |
| [X-NFR-001](requirements/x-records/X-NFR-001.md) | Доступность публичного API не ниже 99,9 % в месяц | NFR | approved | P1 | role-sre | x-records | ADR-001 |
| [X-NFR-002](requirements/x-records/X-NFR-002.md) | Время ответа API p95 ≤ 300 мс при 200 RPS | NFR | approved | P2 | role-x-records-engineers | x-records |  |
| [X-NFR-003](requirements/x-records/X-NFR-003.md) | Время хранится только в UTC с часовым поясом | NFR | verified | P3 | role-x-records-engineers | x-records |  |
| [X-OPS-001](requirements/x-platform/X-OPS-001.md) | Резервное копирование БД с RPO ≤ 15 минут | OPS | approved | P1 | role-platform-engineers | x-platform | ADR-002 |
| [X-OPS-002](requirements/x-platform/X-OPS-002.md) | Ежеквартальное учение по восстановлению с RTO ≤ 4 часа | OPS | proposed | P2 | role-platform-engineers | x-platform | ADR-002 |
| [X-OPS-003](requirements/x-platform/X-OPS-003.md) | Централизованное логирование со сроком хранения 30 дней | OPS | approved | P2 | role-sre | x-platform |  |
| [X-OPS-004](requirements/x-platform/X-OPS-004.md) | Обязательный CI-гейт перед слиянием в main | OPS | implemented | P1 | role-platform-engineers | x-platform |  |
| [X-SEC-001](requirements/x-platform/X-SEC-001.md) | Вход сотрудников только через SSO с MFA | SEC | implemented | P1 | role-security-engineers | x-platform |  |
| [X-SEC-002](requirements/x-platform/X-SEC-002.md) | Секреты хранятся только в менеджере секретов | SEC | approved | P1 | role-security-engineers | x-platform | ADR-001 |
| [X-SEC-003](requirements/x-records/X-SEC-003.md) | Персональные данные хранятся не дольше установленного срока | SEC | proposed | P1 | role-data-protection | x-records |  |
| [X-SEC-004](requirements/x-platform/X-SEC-004.md) | Сканирование образов и блокировка критических уязвимостей | SEC | proposed | P2 | role-security-engineers | x-platform |  |
