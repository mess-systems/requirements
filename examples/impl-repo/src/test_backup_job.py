from backup_job import RETENTION_DAYS


# [itest->req~X-OPS-001~1]
def test_retention_is_30_days():
    assert RETENTION_DAYS == 30
