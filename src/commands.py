from src.driver import apply
from src.db import DB
import asyncio


def exec_command(message):
    args = message['text']
    user = message['user']

    if ' ' in args:
        cmd, args = tuple(args.split(' ', 1))
    else:
        cmd = args

    return exec(f'''Commands(user).{cmd}(args)''')


class Commands:
    def __init__(self, user):
        self._user = user

    def run(self, cmd, args, user):
        slack_id = user
        db = DB(slack_id)

        print("\n")
        print(cmd)
        print("\n")
        print(args)
        if cmd == "help":
            ret = "\n".join(("Available commands:",
                             "help: Prints the list of available commands",
                             "login: User login, required before any other action",
                             "apply: Apply for leave",
                             ))
            return ret
        elif cmd == "login":
            print(args)
            user_id, user_pass = args.split(' ')
            # print('setting user details')
            db.greythr_user_id = user_id
            db.greythr_password = user_pass
            db.freeze()
            return "Login successful!", None
        elif cmd == "apply":
            print('here')
            start, end = args.split(' ')
            start = f'{start} Dec 2019'
            end = f'{end} Dec 2019'
            print(start)
            print(end)
            print(db.greythr_user_id)
            print(db.greythr_password)
            # userid, passwd = 'T12546', '@123456789'
            # userid, passwd = 'S12667', 'Dynamic@@123'

            # login T12546 @123456789
            # apply ‘18 Dec 2019’ ‘19 Dec 2019’
            # res = asyncio.run(apply(db.greythr_user_id, db.greythr_password, start, end))
            res = asyncio.run(apply('T12546', '@123456789', start, end))
            return res, [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "dsf"
                }
            }]

        else:
            ret = "Command not available!"
            return ret

    def apply(self, args):
        print(self._user)
        print(args)


if __name__ == "__main__":
    exec_command({
        "text": "apply is the text.",
        "user": "duke79"
    })
