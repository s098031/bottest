import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("ku2iKmgJfguqdnJQirY4yW8m1YlzLRSPGgLy1C7s4lvsp4Mu42HWYcx3mgvo+77hRMRl7DbEFo6YiVwaoGdQKaFGTXtEqaQ95jRj1pYiwtZ9ux8zkS/JfGDD7WsDjVhl2mKQJA9FOEOQvsjJ/Sx/1wdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.environ.get("66a4797a094f8a6d313760f17081f97a"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
