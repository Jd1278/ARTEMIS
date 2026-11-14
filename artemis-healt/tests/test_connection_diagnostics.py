from artemis_health.database.connection import connection_failure_category


def test_connection_categories_do_not_return_driver_messages_or_credentials():
    for message, expected in (
        ("password authentication failed for user private-user", "authentication"),
        ("Network is unreachable", "network_unreachable"),
        ("Tenant or user not found", "pooler_user"),
        ('invalid connection option "DATABASE_URL"', "connection_format"),
        ("private connection details", "RuntimeError"),
    ):
        assert connection_failure_category(RuntimeError(message)) == expected
