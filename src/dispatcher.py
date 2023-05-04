from process import UserProcess


class Dispatcher:
    started_processes = {}

    def get_message(self, bot, message):
        user_id = message["from"]["id"]
        if user_id not in self.started_processes:
            user_id = message["from"]["id"]
            process = UserProcess(bot, self, user_id)
            self.started_processes[user_id] = process
        else:
            self.started_processes[user_id].process_message(message["text"])

    def delete_process(self, user_id):
        self.started_processes.pop(user_id)
