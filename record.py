from dataclasses import dataclass
import datetime

import psycopg2

import settings


@dataclass
class Record:
    user_id: int
    type: str = None
    category: str = None
    amount: float = None

    def save(self):
        conn = psycopg2.connect(
            (f'dbname={settings.DB_NAME} '
             f'user={settings.DB_USER} '
             f'password={settings.DB_PASSWORD}')
        )
        cur = conn.cursor()
        time = datetime.datetime.now()
        if self.type == "доход":
            cur.execute(
                'insert into incomes (user_id, amount, category, time)values(%s, %s, %s, %s);',
                (self.user_id, self.amount, self.category, time)
            )
        else:
            cur.execute(
                'insert into spends (user_id, amount, category, time)values(%s, %s, %s, %s);',
                (self.user_id, self.amount, self.category, time)
            )
        conn.commit()
        cur.close()
        conn.close()
