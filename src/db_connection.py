from typing import Optional
from datetime import datetime

import psycopg2

from models import Record
import settings


class Database:
    """
    Represent a database interface and is a singleton.
    Contain database connection.
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            (f'dbname={settings.DB_NAME} '
             f'user={settings.DB_USER} '
             f'password={settings.DB_PASSWORD}')
        )

    def read_offset(self) -> Optional[str]:
        cur = self.connection.cursor()
        cur.execute('SELECT "offset" FROM bot_offset;')
        return cur.fetchone()[0]

    def write_offset(self, value: str) -> None:
        cur = self.connection.cursor()
        cur.execute(
            'UPDATE bot_offset SET "offset" = %s;',
            (value,)
        )
        self.connection.commit()
        cur.close()

    def write_record(self, record: Record) -> None:
        time = datetime.now()
        cur = self.connection.cursor()
        if record.type == 'доход':
            cur.execute(
                ('INSERT INTO incomes (user_id, amount, category, time)'
                 ' VALUES (%s, %s, %s, %s);'),
                (record.user_id,
                 record.amount,
                 record.category,
                 time)
            )
        else:
            cur.execute(
                ('INSERT INTO spends (user_id, amount, category, time)'
                 ' VALUES (%s, %s, %s, %s);'),
                (record.user_id,
                 record.amount,
                 record.category,
                 time)
            )
        self.connection.commit()
        cur.close()
