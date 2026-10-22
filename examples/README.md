# Организация проектов

## Вариант A (рекомендуется): отдельное репо требований + репо реализации
```
org/
├── requirements/  # этот blueprint; все области (scopes) проекта
│   └── requirements/{x-platform,x-records}/X-*.md
├── x-records/  # код; теги [impl->req~X-...~1]
├── x-infra/     # IaC/манифесты; теги в комментариях
└── x-docs/ (опц.)
```
- Плюсы: один реестр на проект, независимые права, реестр не шумит в PR кода.
- CI репо реализации клонирует репо требований и запускает `oft trace requirements .` (см. `impl-repo/`).
- Несколько проектов: либо одно репо требований с несколькими корнями в `roots:` (`x: X`, `beta: BETA`), либо отдельное репо на проект с одинаковым blueprint.

## Вариант B: монорепо
```
monorepo/
├── reqs.config.yaml
├── requirements/<scope>/*.md
├── docs/adr/
├── services/api/...  # теги OFT рядом с кодом
└── scripts/ (validate, generate)
```
- Плюсы: требование и реализация в одном PR, покрытие считается в одном прогоне.
- Минус: нужны CODEOWNERS на `requirements/`, чтобы статусы менял только владелец.

## Отчёт о покрытии
```
make trace IMPL=examples/impl-repo     # или: oft trace -o html -f trace.html requirements ../x-records
```
`Needs: impl, itest` в требовании говорит OFT, какие покрытия ожидаются; недостающие попадут в отчёт как непокрытые.
