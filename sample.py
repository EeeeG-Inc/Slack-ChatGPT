import os
import sys
import traceback
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
slack_app_token = os.getenv('SLACK_APP_TOKEN')

# ボットトークン・ソケットモードハンドラーを使ってアプリ初期化
app = App(token=slack_bot_token)

# 'hello' を含むメッセージをリッスンする例
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> clicked the button")

if __name__ == "__main__":
    try:
        # アプリ起動
        SocketModeHandler(app, slack_app_token).start()
    except:
        print(sys.exc_info())
        traceback.print_exc()
