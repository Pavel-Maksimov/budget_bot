import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import pathlib
import psycopg2
import re
import time

from bot import Telebot

from dotenv import load_dotenv


BASE_DIR = pathlib.Path(__file__).resolve().parent

dotenv_path = BASE_DIR / '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    BASE_DIR / 'bot_logs.log',
    maxBytes=1000000,
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)-12s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

BOT_ID = os.environ.get('BOT_ID')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

logger.info('Start')
time.sleep(15)

with open(BASE_DIR / 'offset.txt', 'r') as f:
    offset = f.read().strip()
if offset == '':
    offset = None
logger.info(f'offset = {offset}')
bot = Telebot(BOT_ID, offset)
messages = []
res = bot.check_updates()
count = 0
if res:
    try:
        conn = psycopg2.connect(f'dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}')
    except psycopg2.OperationalError as err:
        logger.error(err)
        raise
    cur = conn.cursor()
    for message in res['result']:
        m = message['message']['text']
        mon = re.search(r'[0-9]+(\.|,)?[0-9]*', m)
        if not mon:
            continue
        summ = mon.group().replace(',', '.')
        cat = re.search('[а-я]+', m)
        if cat:
            category = cat.group().lower().strip()
        else:
            category = 'не задано'
        user = message['message']['from']['id']
        date = datetime.datetime.fromtimestamp(message['message']['date'])
        if category in ('зп', 'зарплата'):
            cur.execute(
                'insert into incomes (user_id, amount, category, time)values(%s, %s, %s, %s);',
                (user, summ, category, date)
            )
        else:
            cur.execute(
                'insert into spends (user_id, amount, category, time)values(%s, %s, %s, %s);',
                (user, summ, category, date)
            )
        conn.commit()
        count += 1
    cur.close()
    conn.close()
    with open(BASE_DIR / 'offset.txt', 'w') as f:
        f.write(str(bot.offset))
    logger.info(f'inserted {count} records.')
