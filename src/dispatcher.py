from process import UserProcess
from stages import TypeStage, CategoryStage, AmountStage


class Dispatcher:
    """
    Dispatch messages to started user process or
     create one of not exists.
    Delete process from started_processes when correcponding
    process finishes, for this Observer pattern is used.
    """
    started_processes = {}

    def get_message(self, bot, message):
        user_id = message["from"]["id"]
        if user_id not in self.started_processes:
            program = [TypeStage, CategoryStage, AmountStage]
            process = UserProcess(bot, self, user_id)
            process.start_program(program)
            self.started_processes[user_id] = process
        else:
            self.started_processes[user_id].process_message(message["text"])

    def delete_process(self, user_id):
        self.started_processes.pop(user_id)
