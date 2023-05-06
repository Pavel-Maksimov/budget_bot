from db_connection import Database
from models import Record
from stages import Stage


class UserProcess:
    def __init__(self, bot, dispatcher, user_id):
        self.dispatcher = dispatcher
        self.bot = bot
        self.user_id = user_id

    def start_program(self, program: list[Stage]):
        self.record = Record(user_id=self.user_id)
        self.program = program
        self.stage_counter = 0
        self.stage = self.program[self.stage_counter](
            self.bot,
            self.user_id,
            self.record
        )

    def process_message(self, message):
        if message == "⇦":
            self.go_previous_stage()
        else:
            self.stage.get_response(message)
            self.go_next_stage()

    def go_next_stage(self):
        if self.stage_counter < (len(self.program) - 1):
            self.stage_counter += 1
            self.stage = self.program[self.stage_counter](
                bot=self.bot,
                user_id=self.user_id,
                record=self.record
            )
        else:
            self.save_record()
            self.stop_process()

    def go_previous_stage(self):
        if self.stage_counter > 0:
            self.stage_counter -= 1
        self.stage = self.program[self.stage_counter](
            bot=self.bot,
            user_id=self.user_id,
            record=self.record
        )

    def save_record(self):
        Database().write_record(self.record)
        self.bot.send_reply(
            user_id=self.user_id,
            reply="Записано!"
        )

    def stop_process(self):
        self.dispatcher.delete_process(self.user_id)
