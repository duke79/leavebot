# import sqlite3
# conn = sqlite3.connect('leavebot.db')
import pickle, os


class DB:
    def __init__(self, slack_id):
        self._slack_id = str(slack_id)
        self._pickle_path = "data/" + self._slack_id + ".pkl"
        self._pickle_path = os.path.normpath(self._pickle_path)

        try:
            self.load()
        except Exception as e:
            self.greythr_user_id = None
            self.greythr_password = None

    def load(self):
        with open(self._pickle_path, 'rb') as f:
            obj = pickle.load(f)
            self.__dict__ = obj.__dict__

    def freeze(self):
        with open(self._pickle_path, 'wb+') as f:
            pickle.dump(self, f)
            # print(self.__dict__)
