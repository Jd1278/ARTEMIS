"""Short-lived TLS connections, compatible with Supabase transaction pooling."""
import os
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row

@contextmanager
def connection(*, admin=False):
    key = 'DATABASE_ADMIN_URL' if admin else 'DATABASE_URL'
    url = os.environ.get(key)
    if not url:
        raise RuntimeError(f'{key} is not configured')
    with psycopg.connect(url, sslmode='require', connect_timeout=10,
                         prepare_threshold=None, row_factory=dict_row) as conn:
        yield conn
