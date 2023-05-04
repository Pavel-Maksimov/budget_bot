import time

from bot import Telebot
from dispatcher import Dispatcher
import settings


if __name__ == "__main__":
    time.sleep(1)

    with open(settings.BASE_DIR / 'offset.txt', 'r') as f:
        offset = f.read().strip() or None
    bot = Telebot(settings.BOT_ID, offset)
    dispatcher = Dispatcher()
    while True:
        res = bot.check_updates()
        if res and res["ok"]:
            for message in res['result']:
                dispatcher.get_message(bot, message["message"])
            with open(settings.BASE_DIR / 'offset.txt', 'w') as f:
                f.write(str(bot.offset))
        time.sleep(2)
