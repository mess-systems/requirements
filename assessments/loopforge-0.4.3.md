# Оценка: Tencent LoopForge 0.4.3 по сквозным наборам

Справочный документ, не требование. Показывает, какие типовые требования наборов `ent-baseline`, `ai-usage-baseline` и `agent-exec-baseline` закрывает [LoopForge](https://github.com/Tencent/LoopForge) версии [0.4.3](https://github.com/Tencent/LoopForge/releases/tag/v0.4.3). Это self-hosted рабочее пространство поставки ПО с coding-агентами, кандидат на реализацию профиля [`adlc-agent-delivery`](../profiles/classes/adlc-agent-delivery.yaml). Код распространяется по лицензии MIT, сторонние компоненты сохраняют свои лицензии.

Оценка сделана по документации, API-описаниям и исходному коду тега `v0.4.3` на 26.11.2026. Работа функций в развёрнутой системе не проверялась.

Статусы:

- `есть`: функция описана в документации или найдена в коде;
- `частично`: есть с существенными ограничениями, они указаны;
- `нет`: в документации прямо сказано, что функции нет, или она описана только как предложение;
- `не найдено`: в документации, API-описаниях и коде упоминаний не найдено. Это не доказательство отсутствия.

## ent-baseline

| Требование | Статус | Что есть в 0.4.3 | Источник |
|---|---|---|---|
| T-IAM-001 Вход через корпоративный IdP по OpenID Connect | нет | Нативного OIDC нет. Есть вход по доверенному заголовку личности от прокси аутентификации: заголовок принимается только с общим секретом. Работа связки с поставщиком идентичностей не проверялась | [deployment.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md#L95-L98) |
| T-IAM-002 Второй фактор для каждого входа | нет | Локальные учётные записи только с паролем. Второй фактор возможен только у внешнего поставщика идентичностей за прокси | [deployment.md, Accounts](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md#accounts) |
| T-IAM-003 Роли и членство из групп IdP | нет | Членство в проектах ведётся вручную | [deployment.md, Accounts](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md#accounts) |
| T-IAM-004 Изоляция чтения между проектами | нет | Модель доверенной команды: вошедшие пользователи видят все проекты, требования и прогоны. Документация предупреждает, что одна установка не должна разделять группы, которые не доверяют друг другу | [deployment.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md#L226) |
| T-IAM-005 Настраиваемые роли | нет | Фиксированный набор ролей: администратор, владелец, мейнтейнер, участник, наблюдатель | [release-readiness.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/release-readiness.md) |
| T-IAM-006 Автоматическое заведение и отключение учётных записей | нет | Учётные записи создаются вручную или утилитой командной строки | [deployment.md, Accounts](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md#accounts) |
| T-IAM-007 Фоновые задачи от сервисной учётной записи | нет | Задача по расписанию выполняется с личностью и правами последнего, кто её сохранил | [ai-scheduled-task-capabilities.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/ai-scheduled-task-capabilities.md); [sync-schedule.js](https://github.com/Tencent/LoopForge/blob/v0.4.3/web/app/sync-schedule.js#L514) |
| T-IAM-008 Секреты из внешнего хранилища | нет | Секреты хранятся в базе данных, зашифрованные мастер-ключом из файла окружения. Политика безопасности рекомендует внешний менеджер секретов, интеграции нет | [SECURITY.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/SECURITY.md#L21) |
| T-GOV-001 Журнал аудита | не найдено | Есть история операций по требованию, акт приёмки и отметка того, кто подтвердил шаг в канале. Сквозного журнала аудита в документации нет | [bot-sop-controls.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/bot-sop-controls.md) |
| T-SEC-001 Выгрузка журнала аудита в SIEM | не найдено | Выгрузки нет, потому что нет сквозного журнала | [bot-sop-controls.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/bot-sop-controls.md) |
| T-GOV-002 Сроки хранения данных | не найдено | Сроки хранения настраиваются только для данных ботов в мессенджерах | [deployment.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md) |
| T-INFRA-001 Отказоустойчивое развёртывание в Kubernetes | не найдено | Есть развёртывание через Compose и разделение API и обработчиков с общей базой данных | [deployment.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md); [compose.yaml](https://github.com/Tencent/LoopForge/blob/v0.4.3/compose.yaml) |
| T-OBS-001 Метрики в формате OpenMetrics | не найдено | Только проверка работоспособности | [API README](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/api/README.md) |
| T-OBS-002 Правила оповещения | не найдено | Нет метрик, на которые можно опереть правила | [API README](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/api/README.md) |

## ai-usage-baseline

| Требование | Статус | Что есть в 0.4.3 | Источник |
|---|---|---|---|
| T-AI-001 Вызовы моделей только через AI-шлюз | нет | Адрес API и ключ задаются для каждого CLI в личных настройках пользователя, поэтому каждый может указать шлюз сам. Централизованной настройки нет | [deployment.md, Choosing an executor](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md#choosing-an-executor) |
| T-AI-002 Атрибуция вызова человеку и прогону | не найдено | Ответственный за вызов известен внутри платформы, но по документации не передаётся в запросах к модели | — |
| T-AI-003 Экспорт трассировок по OTLP | нет | Есть только внутренний приёмник OTLP на loopback и собственная телеметрия прогонов | [API README](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/api/README.md) |
| T-AI-004 Бюджеты с блокировкой | нет | Только учёт токенов и стоимости. Ограничено лишь число одновременных прогонов на машину | [token-pricing.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/token-pricing.md); [runners.js](https://github.com/Tencent/LoopForge/blob/v0.4.3/web/app/runners.js#L45-L48) |
| T-AI-005 Собственный прайс и валюта | нет | Публичные прайсы, расчёт в юанях с фиксированным курсом к доллару | [token-pricing.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/token-pricing.md) |
| T-AI-006 Фильтры защиты данных | нет | Маскируются только собственные токены пользователя в беседе | [conversation-workspaces.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/conversation-workspaces.md) |

## agent-exec-baseline

| Требование | Статус | Что есть в 0.4.3 | Источник |
|---|---|---|---|
| T-ADLC-001 Ограничение сетевого выхода | нет | Есть лимиты CPU, памяти и числа процессов. Документация прямо пишет, что изоляции сетевого выхода для команд CLI нет | [evolution.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/api/evolution.md#L12) |
| T-ADLC-002 Исполнение без доступа к управлению контейнерами хоста | нет | Сокет контейнерного движка хоста монтируется в контейнер платформы | [compose.yaml](https://github.com/Tencent/LoopForge/blob/v0.4.3/compose.yaml#L94) |
| T-ADLC-003 Конфигурация и хуки из репозитория без человека | нет | Только предупреждение в документации | [deployment.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/deployment.md) |

## Итог

| Набор | Требований | есть | частично | нет | не найдено |
|---|---|---|---|---|---|
| ent-baseline | 14 | 0 | 0 | 8 | 6 |
| ai-usage-baseline | 6 | 0 | 0 | 5 | 1 |
| agent-exec-baseline | 3 | 0 | 0 | 3 | 0 |

Сильные стороны LoopForge лежат в возможностях класса: процессы поставки, шаги одобрения человеком, исполнители, песочницы с лимитами ресурсов, учёт стоимости. Их оценка появится, когда возможности класса будут перенесены в профиль `adlc-agent-delivery`. Сквозной корпоративный контур продукт в версии 0.4.3 не закрывает: его нужно достраивать вокруг продукта (прокси аутентификации, шлюз моделей, изолированные среды исполнения) или в форке.

## Расхождения документации и кода

| Пункт разбора | Что расходится | Источник |
|---|---|---|
| DEP-05, сетевые настройки по умолчанию | Одна страница документации говорит, что установщик слушает только localhost. В коде и шаблоне развёртывания сервис по умолчанию слушает все сетевые интерфейсы | [release-readiness.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/release-readiness.md#L9); [compose.yaml](https://github.com/Tencent/LoopForge/blob/v0.4.3/compose.yaml#L45); [configure.sh](https://github.com/Tencent/LoopForge/blob/v0.4.3/scripts/configure.sh#L65) |
| ENT-25, каталог навыков | Корпоративной витрины навыков нет, но в коде есть прокси к публичному каталогу навыков с поиском и установкой в проект, установленные файлы только для чтения | [skillhub_client.go](https://github.com/Tencent/LoopForge/blob/v0.4.3/internal/httpapi/skillhub_client.go#L22-L23); [openapi.yaml](https://github.com/Tencent/LoopForge/blob/v0.4.3/docs/api/openapi.yaml#L2849-L2854) |
| RUN-08, одновременные прогоны | Лимит задаётся на каждую машину и может быть пустым («без ограничения»). Ёмкость, которую сообщает раннер, сервер ограничивает диапазоном 1–32. Фиксированного общего лимита в коде нет | [runners.js](https://github.com/Tencent/LoopForge/blob/v0.4.3/web/app/runners.js#L45-L73); [runners.go](https://github.com/Tencent/LoopForge/blob/v0.4.3/internal/httpapi/runners.go#L822-L833) |
| HITL-03, режимы прав агента | Три режима: запрос подтверждения у человека, решение AI-ревьюера, полные права. В коде они названы по-китайски; английский интерфейс переводит второй как Approve for me, английские названия двух других не сверены | [assistant_workspace_mode.go](https://github.com/Tencent/LoopForge/blob/v0.4.3/internal/httpapi/assistant_workspace_mode.go#L21); [CHANGELOG.md](https://github.com/Tencent/LoopForge/blob/v0.4.3/CHANGELOG.md#L50) |
