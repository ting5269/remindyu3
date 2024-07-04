from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import schedule
import time
from threading import Thread, Timer

app = Flask(__name__)

line_bot_api = LineBotApi('A8ISwhsCwJuQrPe03vd+6xngj59R4nah0V4If0GKJjiSg4EIogYRCWzwE+0XA4Avkc2mBfZHLHCSQxWhkgmuykstCywsHIBXr1jn08CwQutNBrcrg5gzgIQIMDFF/LiYErXmttwdoHlegvBCRgRuYgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d969ac6229fcb01a73b29792667ec7b1')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 如果接收到的訊息是 "1"，回覆 "你好"
    if event.message.text == "1":
        reply_text = "4.0"
    else:
        reply_text = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))

def send_reminder(reminder_count):
    if reminder_count > 0:
        line_bot_api.broadcast(TextSendMessage(text='這是你的提醒！'))
        Timer(60, send_reminder, [reminder_count - 1]).start()

def start_reminders():
    # 設置初始提醒
    Timer(0, send_reminder, [4]).start()

# 設定每天的提醒時間
schedule.every().day.at("03:00").do(start_reminders)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # 啟動 scheduler 的線程
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

    # 啟動 Flask 伺服器
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
