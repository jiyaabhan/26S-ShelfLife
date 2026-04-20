"""MySQL helpers for ShelfLife API blueprints."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

import pymysql
from pymysql.cursors import DictCursor


def _db_config() -> dict[str, Any]:
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "shelflife_db"),
        "cursorclass": DictCursor,
        "autocommit": False,
    }


@contextmanager
def get_cursor() -> Generator[DictCursor, None, None]:
    conn = pymysql.connect(**_db_config())
    try:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            cursor.close()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
