"""Пример репо реализации с тегами OpenFastTrace."""

# [impl->req~X-OPS-001~1]
WAL_ARCHIVE_MAX_LAG_SECONDS = 300
FULL_BACKUP_CRON = "0 2 * * *"
RETENTION_DAYS = 30


# [impl->req~X-SEC-003~1]
def purge_expired_pii(db, now):
    """Удаляет или обезличивает ПДн с истёкшим сроком хранения."""
    for table, column, days in db.pii_registry():
        db.anonymize_older_than(table, column, days, now)
