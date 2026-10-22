# Промпт: проверить покрытие
```
Запусти make trace IMPL=<путь к репо реализации> (или oft trace requirements <пути>).
Сведи в таблицу: требование, статус, есть ли impl, utest, itest.
Выдели: approved без impl; implemented без тестов при Needs: utest/itest; устаревшие теги ~1 при version 2.
Предложи план, не меняя статусы самостоятельно.
```
