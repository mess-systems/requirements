# Каталог типовых требований

*Сгенерирован `scripts/generate.py`, не редактировать вручную.*

Выпуск каталога: **0.1.0**. Типовых требований: **23**. Профилей: **5**.

Уровень (MUST, SHOULD, MAY) — сила формулировки по RFC 2119 и RFC 8174. Приоритет по MoSCoW задаёт проект в `adoption.yaml`.

## Профили

| Профиль | Вид | Версия | Статус | Blueprint | Включает | Пунктов (с включёнными) |
|---|---|---|---|---|---|---|
| [adlc-agent-delivery](profiles/classes/adlc-agent-delivery.yaml) | class | 0.1.0 | draft | adlc-agent-delivery | ent-baseline@0.1, ai-usage-baseline@0.1, agent-exec-baseline@0.1 | 0 (23) |
| [agent-exec-baseline](profiles/sets/agent-exec-baseline.yaml) | set | 0.1.0 | proposed |  |  | 3 (3) |
| [ai-enablement](profiles/classes/ai-enablement.yaml) | class | 0.1.0 | draft | ai-enablement | ent-baseline@0.1, ai-usage-baseline@0.1, agent-exec-baseline@0.1 | 0 (23) |
| [ai-usage-baseline](profiles/sets/ai-usage-baseline.yaml) | set | 0.1.0 | proposed |  |  | 6 (6) |
| [ent-baseline](profiles/sets/ent-baseline.yaml) | set | 0.1.0 | proposed |  |  | 14 (14) |

## Требования по доменам naming-standard

### adlc

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-ADLC-001](catalog/adlc/T-ADLC-001.md) | Ограничение сетевого выхода сред исполнения агентов | sandbox | MUST | proposed | agent-exec-baseline (MUST) | ai-enablement#M17, ai-enablement#M18 |
| [T-ADLC-002](catalog/adlc/T-ADLC-002.md) | Исполнение агентов без доступа к управлению контейнерами хоста | sandbox | MUST | proposed | agent-exec-baseline (MUST) | ai-enablement#M25 |
| [T-ADLC-003](catalog/adlc/T-ADLC-003.md) | Конфигурация и хуки из репозитория в прогонах без человека | sandbox | SHOULD | proposed | agent-exec-baseline (SHOULD) |  |

### ai

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-AI-001](catalog/ai/T-AI-001.md) | Вызовы моделей только через корпоративный AI-шлюз | gateway | MUST | proposed | ai-usage-baseline (MUST) | ai-enablement#M4, ai-enablement#M5 |
| [T-AI-002](catalog/ai/T-AI-002.md) | Атрибуция вызова модели человеку и прогону | gateway | MUST | proposed | ai-usage-baseline (MUST) | ai-enablement#M12 |
| [T-AI-003](catalog/ai/T-AI-003.md) | Экспорт трассировок вызовов моделей по OTLP | llm-traces | SHOULD | proposed | ai-usage-baseline (SHOULD) |  |
| [T-AI-004](catalog/ai/T-AI-004.md) | Бюджеты расходов на модели с блокировкой | gateway | MUST | proposed | ai-usage-baseline (MUST) | ai-enablement#M6 |
| [T-AI-005](catalog/ai/T-AI-005.md) | Собственный прайс моделей и валюта расчётов | gateway | SHOULD | proposed | ai-usage-baseline (SHOULD) |  |
| [T-AI-006](catalog/ai/T-AI-006.md) | Фильтры защиты данных для запросов и ответов моделей | guard | MUST | proposed | ai-usage-baseline (MUST) | ai-enablement#M7, ai-enablement#M8, ai-enablement#M9 |

### gov

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-GOV-001](catalog/gov/T-GOV-001.md) | Журнал аудита действий пользователей и агентов | audit | MUST | proposed | ent-baseline (MUST) |  |
| [T-GOV-002](catalog/gov/T-GOV-002.md) | Сроки хранения всех видов данных | policy | SHOULD | proposed | ent-baseline (SHOULD) |  |

### iam

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-IAM-001](catalog/iam/T-IAM-001.md) | Вход пользователей через корпоративный IdP по OpenID Connect | sso | MUST | proposed | ent-baseline (MUST) |  |
| [T-IAM-002](catalog/iam/T-IAM-002.md) | Второй фактор для каждого интерактивного входа | sso | MUST | proposed | ent-baseline (MUST) | ai-enablement#M3 |
| [T-IAM-003](catalog/iam/T-IAM-003.md) | Роли и членство из групп поставщика идентичностей | sso | MUST | proposed | ent-baseline (MUST) |  |
| [T-IAM-004](catalog/iam/T-IAM-004.md) | Изоляция чтения между проектами | sso | MUST | proposed | ent-baseline (MUST) |  |
| [T-IAM-005](catalog/iam/T-IAM-005.md) | Настраиваемые роли и права | sso | SHOULD | proposed | ent-baseline (SHOULD) |  |
| [T-IAM-006](catalog/iam/T-IAM-006.md) | Автоматическое заведение и отключение учётных записей | directory | SHOULD | proposed | ent-baseline (SHOULD) |  |
| [T-IAM-007](catalog/iam/T-IAM-007.md) | Фоновые задачи от сервисной учётной записи | directory | SHOULD | proposed | ent-baseline (SHOULD) |  |
| [T-IAM-008](catalog/iam/T-IAM-008.md) | Секреты из внешнего хранилища секретов | secrets | MUST | proposed | ent-baseline (MUST) |  |

### infra

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-INFRA-001](catalog/infra/T-INFRA-001.md) | Отказоустойчивое развёртывание в Kubernetes | k8s | SHOULD | proposed | ent-baseline (SHOULD) |  |

### obs

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-OBS-001](catalog/obs/T-OBS-001.md) | Метрики работы в формате OpenMetrics | metrics | SHOULD | proposed | ent-baseline (SHOULD) |  |
| [T-OBS-002](catalog/obs/T-OBS-002.md) | Правила оповещения для типовых отказов | alerts | SHOULD | proposed | ent-baseline (SHOULD) |  |

### sec

| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |
|---|---|---|---|---|---|---|
| [T-SEC-001](catalog/sec/T-SEC-001.md) | Выгрузка журнала аудита в SIEM | siem | MUST | proposed | ent-baseline (MUST) |  |

## Источники и где они используются

| Ключ | Источник | Используется в |
|---|---|---|
| `iso-29148` | [ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering](https://www.iso.org/standard/72089.html) | — |
| `k8s-disruptions` | [Kubernetes: Disruptions and PodDisruptionBudget](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) | T-INFRA-001 |
| `loopforge-0.4.3` | [Tencent LoopForge v0.4.3, релиз](https://github.com/Tencent/LoopForge/releases/tag/v0.4.3) | — |
| `nist-800-63b` | [NIST SP 800-63B: Digital Identity Guidelines, Authentication and Authenticator Management](https://pages.nist.gov/800-63-4/sp800-63b.html) | T-IAM-002 |
| `nist-800-92` | [NIST SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/pubs/sp/800/92/final) | T-GOV-001, T-SEC-001 |
| `oidc-backchannel-logout` | [OpenID Connect Back-Channel Logout 1.0](https://openid.net/specs/openid-connect-backchannel-1_0.html) | T-IAM-001 |
| `oidc-core` | [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html) | T-IAM-001, T-IAM-003 |
| `oidc-rp-logout` | [OpenID Connect RP-Initiated Logout 1.0](https://openid.net/specs/openid-connect-rpinitiated-1_0.html) | T-IAM-001 |
| `openmetrics` | [OpenMetrics specification](https://prometheus.io/docs/specs/om/open_metrics_spec/) | T-OBS-001, T-OBS-002 |
| `otel-genai` | [OpenTelemetry semantic conventions for generative AI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | T-AI-002, T-AI-003 |
| `otlp` | [OpenTelemetry Protocol (OTLP) specification](https://opentelemetry.io/docs/specs/otlp/) | T-AI-003 |
| `owasp-llm-top10` | [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | T-ADLC-001, T-ADLC-003, T-AI-006 |
| `rfc2119` | [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119) | — |
| `rfc5424` | [RFC 5424: The Syslog Protocol](https://www.rfc-editor.org/rfc/rfc5424) | T-SEC-001 |
| `rfc7636` | [RFC 7636: Proof Key for Code Exchange by OAuth Public Clients (PKCE)](https://www.rfc-editor.org/rfc/rfc7636) | T-IAM-001 |
| `rfc7643` | [RFC 7643: System for Cross-domain Identity Management (SCIM): Core Schema](https://www.rfc-editor.org/rfc/rfc7643) | T-IAM-006 |
| `rfc7644` | [RFC 7644: System for Cross-domain Identity Management (SCIM): Protocol](https://www.rfc-editor.org/rfc/rfc7644) | T-IAM-006 |
| `rfc8174` | [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174) | — |
