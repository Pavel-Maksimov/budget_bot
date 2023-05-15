from abc import ABC, abstractmethod

import settings
from utilities import create_keyboard
from models import Record
from bot import Telebot


class Stage(ABC):
    """
    Base class for all stages of user dialog with bot 
      for saving records.
    """
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
    """
    Stage to save the amount of record.
    """
    keyboard = create_keyboard(1, [])
    message = "Введите сумму"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        response = response.replace(',', '.')
        self.record.amount = float(response)


class IncomeCategoryStage(Stage):
    """
    Stage to save the category of income record.
    """
    keyboard = create_keyboard(4, settings.INCOME_CATEGORIES)
    message = "Выберите категорию"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        self.record.category = response


class OutcomeCategoryStage(Stage):
    """
    Stage to save the category of outcome record.
    """
    keyboard = create_keyboard(4, settings.OUTCOME_CATEGORIES)
    message = "Выберите категорию"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        self.record.category = response


class CategoryStage(Stage):
    """
    General stage to save the category of record
    according to type of the record.
    """
    categories = {
        "доход": IncomeCategoryStage,
        "расход": OutcomeCategoryStage
    }

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        self.category = self.categories[record.type](bot, user_id, record)

    def get_response(self, response: str):
        self.category.get_response(response)


class TypeStage(Stage):
    """
    Stage to save the the type of record.
    """
    keyboard = create_keyboard(2, settings.RECORD_TYPES)
    message = "Выберите тип записи"

    def __init__(self, bot: Telebot, user_id: int, record: Record):
        super().__init__(bot, user_id, record)

    def get_response(self, response: str):
        self.record.type = response
