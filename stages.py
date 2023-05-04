import json

import settings
from utilities import create_keyboard
from record import Record


class Stage:
    keyboard = None

    def __init__(self, bot, user_id):
        bot.send_reply(
            user_id,
            self.message,
            self.keyboard
        )

    def get_response(self, message, record):
        pass


class TypeStage(Stage):
    keyboard = json.dumps(
        create_keyboard(2, settings.RECORD_TYPES),
        ensure_ascii=True
    )
    message = "Выберите тип записи"
    next = Stage

    def get_response(self, response, record: Record):
        record.type = response
        if record.type == "доход":
            self.next = IncomeCategoryStage
        elif record.type == "расход":
            self.next = OutcomeCategoryStage


class AmountStage(Stage):
    keyboard = None
    message = "Введите сумму"
    next = None

    def get_response(self, response: str, record: Record):
        response = response.replace(',', '.')
        record.amount = float(response)


class IncomeCategoryStage(Stage):
    keyboard = json.dumps(
        create_keyboard(4, settings.INCOME_CATEGORIES),
        ensure_ascii=True
    )
    message = "Выберите тип записи"
    next = AmountStage

    def get_response(self, response, record: Record):
        record.category = response


class OutcomeCategoryStage(Stage):
    keyboard = json.dumps(
        create_keyboard(4, settings.OUTCOME_CATEGORIES),
        ensure_ascii=True
    )
    message = "Выберите тип записи"
    next = AmountStage

    def get_response(self, response, record: Record):
        record.category = response
