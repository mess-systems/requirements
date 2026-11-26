# Связь со стандартом именования

Пакет опирается на [стандарт именования mess.systems](https://github.com/mess-systems/naming-standard/blob/main/README.ru.md), версия v2.5. Ниже указано, что взято из стандарта, а что является собственным соглашением пакета. Если правило здесь расходится со стандартом, верен стандарт.

## Что берётся из стандарта

| Что | Правило стандарта | Где в стандарте |
|---|---|---|
| Символы | `a-z 0-9 -`, только нижний регистр, многословный токен через дефис; `_` только там, где дефис запрещён | [01, раздел 1](https://github.com/mess-systems/naming-standard/blob/main/01-naming-conventions.md#1-character-rules-apply-to-every-family) |
| Продукт, домен, сервис | Имя сервиса продукта `<service>.<domain>.<product>`, сервис уникален в продукте; технология (`implementation`) только в метаданных | [07, раздел 2](https://github.com/mess-systems/naming-standard/blob/main/07-deployment-and-tenants.md#2-product-domain-service-implementation) |
| Окружения | Коды `dev tst stg prd`, в продуктовом контуре ещё `sbx`; классы `prd`, `nonprod`, `sandbox` для ресурсов, которые обслуживают несколько окружений | [01, раздел 4.4](https://github.com/mess-systems/naming-standard/blob/main/01-naming-conventions.md#44-environments-and-sites), [07, разделы 3 и 12.1](https://github.com/mess-systems/naming-standard/blob/main/07-deployment-and-tenants.md#121-environment-class) |
| Один объект, один код окружения | Namespace, приложение GitOps, учётка, путь секрета и бакет одного развёртывания пишут один и тот же код; алиас `stage`/`test` допустим только в публичном DNS | [07, разделы 12.2 и 12.10](https://github.com/mess-systems/naming-standard/blob/main/07-deployment-and-tenants.md#1210-one-object-one-env-code) |
| Владельцы | `owner` всегда группа, никогда человек: `role-platform-engineers` | [04, раздел 5](https://github.com/mess-systems/naming-standard/blob/main/04-identity-conventions.md#5-owners) |
| Имена ресурсов в критериях приёмки | Формы из таблицы объектов: namespace `<product>-<env>`, бакет `<product>-<domain>-<service>-<env-or-class>`, база `<product>_<domain>_<service>_<env>`, хост `<site>-<plane-or-product>-<domain>-<service>-<env>-<NN>` | [01, раздел 5](https://github.com/mess-systems/naming-standard/blob/main/01-naming-conventions.md#5-object-forms), [07, раздел 12](https://github.com/mess-systems/naming-standard/blob/main/07-deployment-and-tenants.md#12-infrastructure-objects-of-a-product-v25) |
| Метки | `mess.systems/<key>`; обязательные метки продукта `cost-center`, `owner`, `env`, `product`, `domain`, `service` | [05](https://github.com/mess-systems/naming-standard/blob/main/05-labels-and-tags.md), [07, раздел 7](https://github.com/mess-systems/naming-standard/blob/main/07-deployment-and-tenants.md#7-governance-labels) |
| Секреты | Значений и путей секретов в требованиях нет; правила хранения в стандарте секретов | [03](https://github.com/mess-systems/naming-standard/blob/main/03-secrets-conventions.md) |

В критериях приёмки можно писать имя ресурса, но не адрес, IP или путь к секрету.

## Собственные соглашения пакета

Стандарт не задаёт имена требований и ADR. Эти правила действуют только внутри пакета и меняются в `reqs.config.yaml` и `schema/`.

| Что | Соглашение пакета |
|---|---|
| ID требования | `<PREFIX>-<TYPE>-<NNN>`: префикс 1–10 заглавных (в примерах `X`, код продукта x в верхнем регистре), тип из словаря `reqs.config.yaml`, номер трёхзначный и не переиспользуется |
| Область (`scope` в front matter) | `<product>-<domain>`, совпадает с каталогом: `x-records`, `x-platform` |
| ADR | `ADR-NNN-<kebab-slug>.md`; при нескольких доменах `ADR-<DOM>-NNN` |
| ID типового требования | `T-<DOM>-<NNN>`: `T` — каталог, `DOM` — код домена стандарта в верхнем регистре (`IAM`, `ADLC`, `INFRA`), номер внутри домена не переиспользуется (`catalog/ids.lock`) |
| Каталог типового требования | `catalog/<domain>/`, где `<domain>` — код домена стандарта; поле `scope` = код домена |
| Сквозной набор | kebab-case с суффиксом `-baseline`: `ent-baseline` |
| Профиль класса решений | имя папки blueprint: `ai-enablement`, `adlc-agent-delivery` |

Поле `scope` пакета означает область требований. В стандарте ключ `scope` корпоративного контура означает другое: самое высокое окружение, для которого сертифицирован объект. Не переносите поле `scope` требования в метки ресурсов.

## Словарь каталога типовых требований

Каталог берёт из стандарта коды доменов ([01, раздел 4.2](https://github.com/mess-systems/naming-standard/blob/main/01-naming-conventions.md#42-domains)) и коды возможностей ([01, раздел 4.3](https://github.com/mess-systems/naming-standard/blob/main/01-naming-conventions.md#43-capability-codes-unique-across-all-domains)). Снимок словаря версии v2.7 лежит в `reqs.config.yaml` (`naming_standard.capabilities`); с клоном стандарта рядом (`NAMING=../naming-standard`) валидатор сверяет снимок с текстом стандарта. Коды, предложенные к внесению, перечислены в `naming_standard.pending`: сейчас это `skills` и `delivery` в домене `adlc`. Требования с такими кодами проходят проверку с предупреждением, пока код не внесён в стандарт. Контуры `corp` и `product` в поле `applies_to` взяты из `catalog/contours.yaml` стандарта.

Если в вашей организации свой стандарт, поменяйте `reqs.config.yaml` и шаблон ID в `schema/`: скрипты от префиксов не зависят.
