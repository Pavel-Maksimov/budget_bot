from db_connection import Database
from models import Record
import stages


class UserProcess:
    def __init__(self, bot, dispatcher, user_id, program: list[stages.Stage]):
        self.dispatcher = dispatcher
        self.bot = bot
        self.user_id = user_id
        self.record = Record(user_id=user_id)
        self.program = program
        self.stage_counter = 0
        self.stage = self.program[self.stage_counter](
            bot,
            user_id, self.record
        )

    def process_message(self, message):
        print(self.stage.__dict__)
        self.stage.get_response(message)
        self.change_stage()

    def change_stage(self):
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

    def save_record(self):
        Database().write_record(self.record)
        self.bot.send_reply(
            user_id=self.user_id,
            reply="Записано!"
        )

    def stop_process(self):
        self.dispatcher.delete_process(self.user_id)
