# Промпт: внедрить blueprint в новый проект
```
Внедри requirements-blueprint в проект <name>.
1. Скопируй blueprint в новое репо <name>-requirements (или каталог монорепо).
2. В reqs.config.yaml задай project, префикс (<PREFIX>), scopes под компоненты проекта, удали примеры x из requirements/ и docs/adr/.
3. Перенеси существующие требования (из <источник>) в формат шаблона, status: draft, источник в source.
4. Включи новые правила валидатора в режиме warn (docs/process/strictness-rollout.md), сделай отчёт violations.md.
5. Настрой CI (.github или .forgejo), branch protection, CODEOWNERS.
6. Добавь .cursor/rules/requirements.mdc и AGENTS.md в репо реализации, адаптировав префикс.
```
