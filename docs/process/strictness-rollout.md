# Поэтапное включение строгой проверки (warn, затем fix, затем error)

Добавляя новое правило в существующий реестр, не ломайте main одним PR.

1. **Warn.** В `reqs.config.yaml` задать `strictness.rules.<rule>: warn`. CI запускает `validate.py --report violations.md` и прикладывает отчёт как артефакт. Ничего не падает.
2. **Fix.** Отдельный PR (можно поручить агенту, промпт 07) исправляет файлы по отчёту. Без смены правил в том же PR.
3. **Error.** Когда отчёт пуст, переключите правило на `error` маленьким PR.

Правила валидатора: `schema, config, filename, duplicate, prefix, type, scope_dir, acceptance_section, oft_marker, adr_exists, verified_needs_evidence, depends_on`.
Быстрый прогон всего в мягком режиме: `make validate-warn`.
