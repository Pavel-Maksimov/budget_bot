from abc import ABC, abstractmethod

import settings
from utilities import create_keyboard
from models import Record
from bot import Telebot


class Stage(ABC):
    def __init__(self, bot: Telebot, user_id: int, record: Record):
        self.record = record
        bot.send_reply(
            user_id,
            self.message,
            self.keyboard
        )

    @abstractmethod
    def get_response(self, response: str):
        pass


class AmountStage(Stage):
    keyboard = None
    message = "Введите сумму"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        response = response.replace(',', '.')
        self.record.amount = float(response)


class IncomeCategoryStage(Stage):
    keyboard = create_keyboard(4, settings.INCOME_CATEGORIES)
    message = "Выберите категорию"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        self.record.category = response


class OutcomeCategoryStage(Stage):
    keyboard = create_keyboard(4, settings.OUTCOME_CATEGORIES)
    message = "Выберите категорию"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        self.record.category = response


class CategoryStage(Stage):
    categories = {
        "доход": IncomeCategoryStage,
        "расход": OutcomeCategoryStage
    }

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        self.category = self.categories[record.type](bot, user_id, record)

    def get_response(self, response: str):
        self.category.get_response(response)


class TypeStage(Stage):
    keyboard = create_keyboard(2, settings.RECORD_TYPES)
    message = "Выберите тип записи"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        print(self)
        self.record.type = response
