from record import Record
import stages


class UserProcess:
    def __init__(self, bot, dispatcher, user_id):
        self.dispatcher = dispatcher
        self.bot = bot
        self.user_id = user_id
        self.record = Record(user_id=user_id)
        self.state = stages.TypeStage(bot, user_id)

    def process_message(self, message):
        self.state.get_response(message, self.record)
        self.change_state()

    def change_state(self):
        if self.state.next:
            self.state = self.state.next(self.bot, self.user_id)
        else:
            self.save_record()
            self.stop_process()

    def save_record(self):
        self.record.save()
        self.bot.send_reply(
            user_id=self.user_id,
            reply="Записано!"
        )

    def stop_process(self):
        self.dispatcher.delete_process(self.user_id)
