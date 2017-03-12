import os
import time
from datetime import datetime

from slackclient import SlackClient


slack_token = os.environ["SLACK_API_TOKEN"]
SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')
sc = SlackClient(slack_token)

# [{'type': 'message',
# 'channel': 'C4H2ZJVUK',
# 'user': 'U4HRBK2QP', 'text': 'hello test bot',
# 'ts': '1489331005.529033', 'source_team': 'T4H2ZJVA7', 'team': 'T4H2ZJVA7'}]


# [{'text': 'Testing :tada:', 'username': 'Slack API Tester',
# 'bot_id': 'B4H33G00K', 'type': 'message', 'subtype': 'bot_message',
# 'team': 'T4H2ZJVA7', 'channel': 'C4H2ZJVUK', 'event_ts': '1489330956.526758', 'ts': '1489330956.526758'}]


def rtm_loop(start_time):
    while True:
        events = sc.rtm_read()
        for e in events:
            print(e)
            e_type = e.get('type')
            is_bot = bool(e.get('bot_id'))
            new_message = e.get('ts') and float(e['ts']) > start_time
            e_text = e.get('text')
            parrot_rmt_messages(e_text, e_type, is_bot, new_message)
        time.sleep(1)


def parrot_rmt_messages(text, e_type, is_bot, new_message):
    if e_type and e_type == 'message' and not is_bot and new_message:
        # posts as bot?
        resp = sc.api_call('chat.postMessage', channel='#general', text=text)
        if not resp['ok']:
            print(resp)
            # posts as user requesting?
            # sc.rtm_send_message("general", e['text'], username='testbot)


def list_channels():
    channels_call = sc.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None



def main():
    print(sc.api_call("auth.test"))
    sc.api_call(
        "chat.postMessage",
        channel="#general",
        text="Testing, bot has been started :tada:",
        username='testbot'
    )
    if sc.rtm_connect():
        start_time = time.time()
        rtm_loop(start_time)
    else:
        print('Connection failed')


if __name__ == "__main__":
    main()



