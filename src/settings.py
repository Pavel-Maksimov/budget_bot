import os
import pathlib

from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / '.env'
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


BOT_ID = os.environ.get('BOT_ID')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

RECORD_TYPES = ["доход", "расход"]
START_KEYBOARD = '{"keyboard": [[{"text": "доход"}, {"text": "расход"}]],"resize_keyboard": true}'
INCOME_CATEGORIES = ["зарплата", "другое"]
OUTCOME_CATEGORIES = [
    "продукты",
    "общественный траспорт",
    "аптека",
    "кафе",
    "подписки",
    "развлечения",
    "бытовые расходы",
    "мобильная связь",
    "интернет",
    "животные",
    "дать в долг",
    "коммунальные",
    "книги",
    "налоги",
    "автомобиль"

]
CATEGORIES = {
    "доход": INCOME_CATEGORIES,
    "расход": OUTCOME_CATEGORIES
}

TABLES = {
            "доход": "incomes",
            "расход": "spends"
        }
