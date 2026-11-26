# Каталог типовых требований

Типовое требование записывают один раз для класса решений, например для любого AI-шлюза или любого агентского delivery workspace. Проект его не переписывает, а подключает через `adoption.yaml`: принимает как есть, уточняет своим требованием или исключает с обоснованием. Как это делает проект, описано в [adoption.md](adoption.md).

## Чем типовое требование отличается от требования проекта

| | Типовое требование | Требование проекта |
|---|---|---|
| Для чего | Для класса решений | Для конкретного продукта или внедрения |
| Где | `catalog/<domain>/T-<DOM>-NNN.md` | `requirements/<scope>/<PREFIX>-<TYPE>-NNN.md` |
| Технологии | Не называет продукты. Открытые стандарты и интерфейсы, которые задают контракт (OIDC, SCIM, OTLP, OpenMetrics, MCP), допустимы. Продукты только в поле `realizations`, справочно | Может называть выбранную технологию, если решение записано в ADR |
| Пороги | Параметры со значением по умолчанию, в тексте `{name}` | Конкретные значения |
| Обязательность | Уровень: MUST, SHOULD или MAY. Это сила формулировки в смысле [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) и [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) | Приоритет по MoSCoW: M Must, S Should, C Could, W Won't |
| Статусы | `draft`, `proposed`, `approved`, `deprecated` | Весь цикл до `implemented` и `verified` |
| Проверка | Строки матриц проверок blueprints (`checks`) | Тесты и протоколы проекта, покрытие OpenFastTrace |

## Слои

```text
catalog/<domain>/        типовые требования, один файл на требование, домены naming-standard
catalog/ids.lock         журнал выданных ID (генерируется), номера не переиспользуются
profiles/sets/           сквозные наборы: ent-baseline, ai-usage-baseline, agent-exec-baseline
profiles/classes/        профили классов решений; имя профиля = папка blueprint
assessments/             оценки продуктов по наборам и профилям, справочно
sources.yaml             реестр источников для поля basis
CATALOG.md               сгенерированный реестр каталога и профилей
```

Требование лежит в каталоге один раз. Наборы и профили только ссылаются на него и при необходимости меняют уровень и значения параметров для своего класса.

## Идентификаторы

| Объект | Форма | Пример |
|---|---|---|
| Типовое требование | `T-<DOM>-<NNN>`, `DOM` — код домена naming-standard в верхнем регистре | `T-IAM-001`, `T-ADLC-002`, `T-INFRA-001` |
| Сквозной набор | kebab-case с суффиксом `-baseline` | `ent-baseline` |
| Профиль класса | имя папки blueprint | `ai-enablement`, `adlc-agent-delivery` |
| Ссылка на строку матрицы проверок | `<папка-blueprint>#M<n>` | `ai-enablement#M3` |
| Выпуск каталога | тег `catalog-vMAJOR.MINOR.PATCH` | `catalog-v0.1.0` |

Код возможности naming-standard пишется в поле `capability` и в строке `Tags:` OpenFastTrace. Если для требования нужен код, которого в стандарте нет, сначала готовится изменение стандарта, а код до его внесения перечисляется в `naming_standard.pending` в `reqs.config.yaml`. Валидатор предупреждает о таких кодах.

## Карточка

Шаблон: [`templates/typical-requirement.md`](../templates/typical-requirement.md). Поля сверх полей требования проекта:

| Поле | Обязательно | Смысл |
|---|---|---|
| `capability` | да | код возможности naming-standard в домене `scope` |
| `level` | да | MUST, SHOULD или MAY, уровень по умолчанию |
| `applies_to` | да | контуры naming-standard: `corp`, `product` |
| `version` | да | совпадает с ревизией OpenFastTrace `~N`, повышается при изменении смысла |
| `params` | нет | параметры: тип, значение по умолчанию, единица, смысл |
| `basis` | нет | ключи `sources.yaml`: стандарты, RFC, спецификации |
| `checks` | нет | строки матриц проверок blueprints |
| `realizations` | нет | карточки tech-radar, справочно |

`priority` в каталоге нет: приоритет задаёт проект.

## Качество формулировок

Проверки опираются на характеристики отдельного требования из ISO/IEC/IEEE 29148:2018, раздел 5.2.5: необходимое, соответствующее уровню, однозначное, полное, единичное, выполнимое, проверяемое, корректное, соответствующее шаблону. Валидатор подсказывает по двум из них:

- единичное: в разделе «Требование» не больше одного «должна»;
- проверяемое: в нормативном тексте нет размытых слов из `quality.vague_words`.

## Версии

- Ревизия требования (`version`, `~N`) меняется, когда меняется смысл. Правки текста без изменения смысла ревизию не меняют. Старые теги `~1` в коде проектов OpenFastTrace покажет как устаревшие.
- Выпуск каталога (`catalog_release`, тег `catalog-vX.Y.Z`): MAJOR, когда удалено или ужесточено требование уровня MUST в любом профиле; MINOR, когда добавлены требования или профили; PATCH, когда исправлен текст без изменения смысла.
- Профиль имеет свою версию. Включение `includes: [ent-baseline@0.1]` фиксирует MAJOR.MINOR.
- Требования не удаляют: их переводят в `deprecated` и указывают замену. Журнал `catalog/ids.lock` не даёт выдать номер повторно.

## Проверки

`make check` и CI запускают `scripts/validate.py` и `scripts/generate.py --check`.

| Правило | Что проверяет | Уровень |
|---|---|---|
| `schema`, `config`, `filename`, `duplicate`, `prefix`, `type`, `scope_dir` | front matter, словари корня, имя файла, ID | error |
| `acceptance_section`, `oft_marker` | раздел «Критерии приёмки», маркер и ревизия OpenFastTrace | error |
| `capability` | код возможности есть в домене naming-standard | error |
| `capability_pending`, `naming_snapshot` | код предложен, но не внесён; снимок кодов расходится со стандартом (`NAMING=...`) | warn |
| `basis` | ключи есть в `sources.yaml` | error |
| `blueprint_check` | строки матриц существуют в blueprints (`BLUEPRINTS=...`) | warn |
| `realizations` | карточки есть в `schema/radar-names.txt` | error |
| `neutrality` | в нормативном тексте нет названий карточек tech-radar, кроме `neutrality.allow` | warn |
| `quality_singular`, `quality_vague` | подсказки по 29148 | warn |
| `params_declared` | параметры в тексте и в `params` совпадают | warn |
| `id_reuse` | выданный ID не потерял файл | error |
| `profile` | профили: схема, пункты существуют и не `deprecated`, параметры объявлены, включения разрешаются | error |
| `adoption`, `adoption_coverage`, `waiver_expired` | см. [adoption.md](adoption.md) | error |
| `privacy` | IP-адреса, имена хостов во внутренних зонах, символ параграфа, адреса почты | error |

Строгость меняется в `reqs.config.yaml` по правилу, см. [strictness-rollout.md](process/strictness-rollout.md).

## Как добавить типовое требование

1. Выберите домен и код возможности naming-standard. Номер — следующий свободный по `catalog/ids.lock`.
2. Скопируйте `templates/typical-requirement.md` в `catalog/<domain>/T-<DOM>-NNN.md`, статус `draft`.
3. Пишите поведение, а не продукт. Пороги вынесите в параметры.
4. Добавьте требование в набор или профиль класса.
5. `make register && make check`, затем PR. Статус `approved` ставит владелец домена каталога.

## Что дальше

- Возможности класса из разбора LoopForge в профиль `adlc-agent-delivery`.
- Требования из разделов blueprint `ai-enablement` в профиль `ai-enablement` (список в `backlog` профиля).
- Профиль каталога навыков после внесения кода `skills` в naming-standard.
- Чтение каталога из отдельного клона выпуска для проектов, которые не хранят каталог у себя.
- Колонка «Требования» в матрицах проверок blueprints, шаблон: [`templates/blueprint-check-matrix.md`](../templates/blueprint-check-matrix.md).
