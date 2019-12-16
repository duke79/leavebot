# ref : https://github.com/slackapi/python-slackclient
import sys, os
import slack
# from src.py.core.config import Config
from commands import exec_command
import logging

# slack_token = Config()["slackbot"]["user_token"]
try:
    slack_token = os.environ["USER_TOKEN"]
except KeyError as e:
    logging.error("environment variable USER_TOKEN is not set")
    exit(1)

# authorized_users = Config()["slackbot"]["authorized_user_ids"]
client = slack.WebClient(slack_token)

console_out = sys.stdout


def print_local(arg):
    console_out.write(arg) #Not working
    pass


def users_list():
    response = client.users_list()
    return response.data["members"]


def send_message(recipient='#random', sender="Unnamed bot", message="Hello!", blocks=None):
    users = [user["id"] for user in users_list()]
    if recipient in users:  # Direct message to the user
        recipient = client.im_open(user=recipient)
        recipient = recipient.data["channel"]["id"]

    response = client.chat_postMessage(
        channel=recipient,
        # username=sender,
        text=message,
        blocks=blocks)

    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"


def run_bot():
    """
    Ref: https://api.slack.com/rtm
    :return:
    """

    import requests
    from websocket import WebSocketConnectionClosedException
    import json

    res = requests.post(url="https://slack.com/api/rtm.connect", data={"token": slack_token})
    data = res.json()
    ws_url = data["url"]

    def on_message(ws, message):
        message = json.loads(message)

        if "user" not in message:
            return

        if str(message["type"]) == "message":
            print_local("%s says: %s" % (message["user"], message["text"]))

            message, blocks = exec_command(message)
            send_message(recipient=message["user"],
                         sender="Leave Bot",
                        #  message=message["text"])
                         message=message,
                         blocks=blocks)

    def on_error(ws, error):
        print_local(error)

    def on_close(ws):
        print_local("### closed ###")

    def on_open(ws):
        print_local("### Bot started ###")

    import websocket

    while True:
        try:
            # websocket.enableTrace(True)
            ws = websocket.WebSocketApp(ws_url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.on_open = on_open
            ws.run_forever()
        except (WebSocketConnectionClosedException, KeyError) as e:
            print_local(e)


def main():
    print("Starting bot...")
    run_bot()


if __name__ == "__main__":
    main()