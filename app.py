import os
import sys
import traceback
import re
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai

load_dotenv()

slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
slack_app_token = os.getenv('SLACK_APP_TOKEN')
openai.api_key = os.getenv('OPENAI_API_KEY')

app = App(token=slack_bot_token)

@app.message(re.compile(r".*"))
def chatgpt(message, say):
    try:
        res = __chatgpt(message['text'])
        answer = res["choices"][0]["message"]["content"]
        __res_to_slack(answer, say)

    except:
        print(sys.exc_info())
        traceback.print_exc()

def __chatgpt(message):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message},
        ]
    )

def __res_to_slack(answer, say):
    say(
        text=f"{answer}"
    )

if __name__ == "__main__":
    try:
        # アプリ起動
        SocketModeHandler(app, slack_app_token).start()
    except:
        print(sys.exc_info())
        traceback.print_exc()
