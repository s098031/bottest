import os
from datetime import datetime
#============================================================
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
#============================================================
from Index import *
from Animation import *
from FlexMessage import *
import Globals
#============================================================

# https://github.com/line/line-bot-sdk-python

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

Globals

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
#=============================================================
# echo
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
#=============================================================
# welcome
@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "我來到一個新世界了嗎\n這個世界應該不再充斥著背叛了吧?\n對不起學姊\n這次，我...\n是永遠屬於各位騎士君的那個優衣呦\n*人家目前不支援簡體中文呦~*"
    message = Log(event)
    line_bot_api.reply_message(event.reply_token,[TextMessage(text=newcoming_text),message])
#=============================================================
# follow 
@handler.add(FollowEvent)
def handle_Follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    Follow_text = profile.display_name + "騎士君歡迎！\n\n車車、圖圖、meme為這個世界帶來希望與和平，也可以把人家拉入群組\n頭貼圖源: twitter@nohhun144"
    message = Log(event)
    line_bot_api.reply_message(event.reply_token,[TextMessage(text=Follow_text),message])
#=============================================================
# handle message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_message = event.message.text
    user = event.source.user_id
    try:
        group = event.source.group_id
    except:
        pass

    JUD = Index_Judgment()
    JUD.Judgment (line_bot_api,input_message,event)
#=============================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug= True)
#=============================================================
