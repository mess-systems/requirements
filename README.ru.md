[English](README.md) | **Русский** | [简体中文](README.zh-CN.md)

# mess.systems requirements: требования как код

Шаблон для ведения требований как кода: Markdown + YAML front matter в git, проверка в CI, автогенерируемый реестр, ADR, трассировка до кода через OpenFastTrace (OFT), сайт на MkDocs и готовые правила/промпты для ИИ-агентов. Примеры написаны для выдуманного продукта **x** компании mess.systems. Здесь же ведётся **каталог типовых требований** по классам решений: проект подключает их через `adoption.yaml`, а не переписывает (см. [docs/catalog.md](docs/catalog.md)).

## Зачем
- Требования версионируются и ревьюятся как код, через PR с одобрением человеком.
- Каждое требование проверяемо (критерии приёмки) и прослеживаемо до кода и тестов.
- Агенты (Cursor и др.) работают по тем же правилам, что люди, и не повышают статусы сами.

## Quick start за 15 минут
```bash
# 1. Скопировать шаблон в новое репо
cp -r requirements-blueprint my-requirements && cd my-requirements && git init
# 2. Зависимости
python3 -m pip install -r requirements-dev.txt
# 3. Настроить проект: префикс, типы, области
$EDITOR reqs.config.yaml        # roots: {requirements: MYP}, scopes: [myp-api, ...]
# 4. Проверить примеры, затем заменить их своими
make check                      # validate + актуальность REGISTER.md
# 5. Первое требование
cp templates/requirement.md requirements/myp-api/MYP-NFR-001.md && $EDITOR $_
make register && make check
# 6. CI: оставить .github/workflows или .forgejo/workflows; включить branch protection
# 7. (опц.) Трассировка и сайт
make trace IMPL=../my-service   # нужен oft (OpenFastTrace 4.11) или java 21 и jar; TRACE_STRICT=1 валит сборку
python3 -m pip install -r requirements-docs.txt && make site
```

## Принципы
1. **Один файл, одно требование**, имя файла = ID, каталог = scope.
2. **Конфиг, а не код**: префиксы, типы, области, статусы задаются в `reqs.config.yaml`.
3. **Проверяемость**: обязательные «Критерии приёмки» и маркер `req~ID~N`.
4. **Трассировка**: `[impl->req~ID~1]` в коде, `[utest|itest->req~ID~1]` в тестах.
5. **Реестр генерируется**, руками не правится; CI проверяет актуальность.
6. **Человек решает**: статусы approved и verified ставятся только через одобренный PR.
7. **Строгость поэтапно**: warn, затем fix, затем error.
8. **Без чувствительного**: никаких секретов, ПДн, ФИО, внутренних адресов.
9. **Типовое один раз**: требование для класса решений лежит в каталоге, проект принимает, уточняет или исключает его с обоснованием.
10. **Приоритет по MoSCoW** (M, S, C, W) в проекте; MUST, SHOULD и MAY в каталоге означают силу формулировки.

## Состав
| Путь | Что |
|---|---|
| `reqs.config.yaml` | префиксы, типы, области, режимы строгости |
| `schema/requirement.schema.json` | JSON Schema front matter |
| `schema/profile.schema.json`, `schema/adoption.schema.json` | схемы профилей и `adoption.yaml` |
| `schema/radar-names.txt` | снимок карточек tech-radar для проверки нейтральности |
| `templates/` | шаблоны требования и ADR |
| `requirements/<scope>/` | 14 требований выдуманного продукта x |
| `requirements/_catalog/` | сгенерированные копии типовых требований, которые принял продукт x |
| `adoption.yaml` | какие типовые требования принимает продукт x и как |
| `catalog/<domain>/` | каталог типовых требований `T-<DOM>-NNN` |
| `profiles/sets/`, `profiles/classes/` | сквозные наборы и профили классов решений |
| `assessments/` | оценки продуктов по наборам, справочно |
| `sources.yaml` | реестр источников каталога |
| `CATALOG.md` | сгенерированный реестр каталога и профилей |
| `scripts/validate.py`, `generate.py`, `reqlib.py` | валидатор, генератор реестров и копий принятых типовых требований |
| `REGISTER.md`, `register.json` | сгенерированный реестр |
| `docs/adr/` | 2 примера ADR |
| `docs/process/` | статусы, поэтапная строгость, процесс изменений |
| `docs/prompts/` | 10 готовых промптов для агентов |
| `docs/catalog.md`, `docs/adoption.md` | каталог типовых требований и как проект их принимает |
| `docs/naming-standard.md` | связь со стандартом именования v2.5 |
| `.cursor/rules/`, `AGENTS.md` | правила для агентов |
| `.github/workflows/`, `.forgejo/workflows/` | CI |
| `examples/` | организация проектов, репо реализации с тегами OFT |
| `mkdocs.yml`, `Makefile` | сайт и команды |

## Формат требования
```yaml
---
id: X-OPS-001
title: Резервное копирование БД с RPO ≤ 15 минут
type: OPS            # из reqs.config.yaml
status: approved     # draft, proposed, approved, implemented, verified или deprecated
priority: M            # MoSCoW: M, S, C или W
owner: role-platform-engineers # роль, не ФИО
scope: x-platform # = каталог
source: [ ... ]
links: { adr: [ADR-002], depends_on: [], verified_by: [] }
version: 1
---
```
Тело: `## Требование` (с `req~ID~1` и `Needs: impl, itest`), `## Обоснование`, `## Критерии приёмки`.

## Типовые требования

Каталог `catalog/` хранит требования для классов решений, например для любого AI-шлюза или агентского delivery workspace. ID `T-<DOM>-NNN`, где `DOM` — код домена naming-standard, код возможности в поле `capability`. Формулировки не называют продукты, пороги вынесены в параметры, проверки ссылаются на строки матриц blueprints (`checks`), варианты реализации — на карточки tech-radar (`realizations`).

Первые сквозные наборы: `ent-baseline` (вход, роли, учётные записи, секреты, аудит, хранение, метрики), `ai-usage-baseline` (AI-шлюз, атрибуция, трассировки, бюджеты, фильтры), `agent-exec-baseline` (изоляция сред исполнения агентов). Профили классов: `ai-enablement`, `adlc-agent-delivery`. Реестр: [CATALOG.md](CATALOG.md).

Проект перечисляет профили в `adoption.yaml` и для каждого требования выбирает `inherit`, `refine` или `waive`. Требования уровня MUST должны быть покрыты все, у исключения есть причина, владелец и срок пересмотра. Подробно: [docs/catalog.md](docs/catalog.md), [docs/adoption.md](docs/adoption.md).

## Расширения
- Экспорт в ReqIF для обмена с внешними системами (например, через StrictDoc).
- Сайт за SSO; фильтры реестра по статусу/области.

## Связь с другими репозиториями mess.systems

| Репозиторий | Что берётся |
|---|---|
| [naming-standard](https://github.com/mess-systems/naming-standard) | имена продуктов, доменов, окружений, владельцев и ресурсов в критериях приёмки, см. [docs/naming-standard.md](docs/naming-standard.md) |
| [tech-radar](https://github.com/mess-systems/tech-radar) | инструменты пакета: OpenFastTrace, MkDocs Material, GitHub Actions и Forgejo Actions ([Forgejo](https://github.com/mess-systems/tech-radar/blob/main/technologies/forgejo.md)); карточки радара указываются в поле `realizations` типовых требований и не входят в их формулировки |
| [blueprints](https://github.com/mess-systems/blueprints) | профиль класса решений называется как папка blueprint; строки матриц проверок служат сценариями приёмки типовых требований (`checks`) |

## Лицензия

Тексты (документация, требования, каталог типовых требований, профили, оценки, ADR, промпты) распространяются по [CC BY 4.0](LICENSE). Код (`scripts/`, `schema/`, `Makefile`, CI, `examples/impl-repo/`) распространяется по [Apache-2.0](LICENSE-CODE). Атрибуция: «mess.systems requirements (https://github.com/mess-systems/requirements), CC BY 4.0».
