# Профили

- `sets/`: сквозные наборы, которые входят во многие классы решений (`ent-baseline`, `ai-usage-baseline`, `agent-exec-baseline`).
- `classes/`: профили классов решений. Имя профиля совпадает с папкой blueprint (`ai-enablement`, `adlc-agent-delivery`).

Профиль ссылается на требования каталога и может задать им уровень, этап и параметры. Схема: [schema/profile.schema.json](../schema/profile.schema.json), шаблон: [templates/profile.yaml](../templates/profile.yaml).
