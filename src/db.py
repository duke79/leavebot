# import sqlite3
# conn = sqlite3.connect('leavebot.db')
import pickle, os

class DB:
    def __init__(self, slack_id):
        # print('here')
        # print(type(slack_id))
        # print(slack_id)
        self._slack_id = str(slack_id)
        # print(self._slack_id)
        # print('here')
        self._pickle_path = self._slack_id + ".pkl"
        self._pickle_path = os.path.normpath(self._pickle_path)

        try:
            self.load()
        except Exception as e:
            print('exception')
            print(e)
            self.greythr_user_id = None
            self.greythr_password = None

        print(self)

    # def __setattr__(self, name, value):
    #     self.__dict__[name] = value
    #     pickle.dump(self, self._pickle_path)

    def load(self):
        with open(self._pickle_path, 'rb') as f:
            obj = pickle.load(f)
            self.__dict__ = obj.__dict__

    def freeze(self):
        with open(self._pickle_path, 'wb+') as f:
            pickle.dump(self, f)
            print(self.__dict__)
