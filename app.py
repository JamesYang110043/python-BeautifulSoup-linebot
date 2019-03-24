# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 01:33:10 2019

@author: James
"""

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Xt+cjXVnFxaWuIy0InCeUyV/PFS0fcfEAgd7EjYjjXOQ4suqwNCmtwNzz0CwbkEGjb8LLZCA+sSOVixLbuhWjvwLjx1nrxlA7Ndo0W9VYodzRTBoEPBJlSLkP/0OZMg2o5TAYJ7F0YTWfg+Ft8OeOgdB04t89/1O/w1cDnyilFU=
')
# Channel Secret
handler = WebhookHandler('ecfc24ef961f042c382db24e1397b9a9
')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text='hi hi')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)