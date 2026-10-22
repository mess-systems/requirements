[English](README.md) | **Русский** | [简体中文](README.zh-CN.md)

# mess.systems requirements: требования как код

Шаблон для ведения требований как кода: Markdown + YAML front matter в git, проверка в CI, автогенерируемый реестр, ADR, трассировка до кода через OpenFastTrace (OFT), сайт на MkDocs и готовые правила/промпты для ИИ-агентов. Примеры написаны для выдуманного продукта **x** компании mess.systems.

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

## Состав
| Путь | Что |
|---|---|
| `reqs.config.yaml` | префиксы, типы, области, режимы строгости |
| `schema/requirement.schema.json` | JSON Schema front matter |
| `templates/` | шаблоны требования и ADR |
| `requirements/<scope>/` | 14 типовых требований продукта x |
| `scripts/validate.py`, `generate.py`, `reqlib.py` | валидатор и генератор реестра |
| `REGISTER.md`, `register.json` | сгенерированный реестр |
| `docs/adr/` | 2 примера ADR |
| `docs/process/` | статусы, поэтапная строгость, процесс изменений |
| `docs/prompts/` | 8 готовых промптов для агентов |
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
priority: P1
owner: role-platform-engineers # роль, не ФИО
scope: x-platform # = каталог
source: [ ... ]
links: { adr: [ADR-002], depends_on: [], verified_by: [] }
version: 1
---
```
Тело: `## Требование` (с `req~ID~1` и `Needs: impl, itest`), `## Обоснование`, `## Критерии приёмки`.

## Расширения
- Экспорт в ReqIF для обмена с внешними системами (например, через StrictDoc).
- Сайт за SSO; фильтры реестра по статусу/области.

## Связь с другими репозиториями mess.systems

| Репозиторий | Что берётся |
|---|---|
| [naming-standard](https://github.com/mess-systems/naming-standard) | имена продуктов, доменов, окружений, владельцев и ресурсов в критериях приёмки, см. [docs/naming-standard.md](docs/naming-standard.md) |
| [tech-radar](https://github.com/mess-systems/tech-radar) | инструменты пакета: OpenFastTrace, MkDocs Material, GitHub Actions и Forgejo Actions ([Forgejo](https://github.com/mess-systems/tech-radar/blob/main/technologies/forgejo.md)) |
| [blueprints](https://github.com/mess-systems/blueprints) | типовые архитектуры; требования к ним можно вести этим пакетом |

## Лицензия

Тексты (документация, требования, ADR, промпты) распространяются по [CC BY 4.0](LICENSE). Код (`scripts/`, `schema/`, `Makefile`, CI, `examples/impl-repo/`) распространяется по [Apache-2.0](LICENSE-CODE). Атрибуция: «mess.systems requirements (https://github.com/mess-systems/requirements), CC BY 4.0».
