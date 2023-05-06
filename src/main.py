import time

from bot import Telebot
from dispatcher import Dispatcher
import settings
from db_connection import Database


if __name__ == "__main__":
    database = Database()
    offset = database.read_offset()
    bot = Telebot(settings.BOT_ID, offset)
    dispatcher = Dispatcher()
    while True:
        res = bot.check_updates()
        if res and res["ok"]:
            for message in res['result']:
                dispatcher.get_message(bot, message["message"])
            database.write_offset(bot.offset)
        time.sleep(2)
