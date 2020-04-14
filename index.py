#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:42:58 2020

@author: jamesyang
"""

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('1124HQQuoQ6e71WUM3lvNtpO7Dfrmyq01htVl+0otqfbauorgipE56qEHttm0LRWe3eqU0KEzgtkPoFEQIqXAGaKH7a5vMFMNEz1b+I82hZF9UigIW4t4ynOetcqsx/lkCj1mGkzGWaG1oBBAJUlda85QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3348e54316a9c373410d66657a265265215')


url = 'https://web.pcc.gov.tw/tps/pss/tender.do?searchMode=common&searchType=basic&method=search'

data = {'searchMethod': True,
'proctrgCode': 72,
'isSpdt': 'Y',
'searchTarget': 'TPAM',
'tenderStatusType': '4,5,21,29,9,22,23,30,34,10,24',
'tenderWay': '12,2,1,4,5,7,3,10,6',
'pmsProctrgCate': 2,
'dmsProctrgCode2': 72,
'tenderDateRadio': 'on',
'tenderStartDate': '109/04/05',
'tenderEndDate': '109/04/11',
'startDate': '109/04/05',
'endDate': '109/04/11'
}

r = requests.post(url, data)
soup = BeautifulSoup(r.text,"html.parser")
sel = soup.select("div#print_area table tr a")





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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


def getdata():
    a=[]
    b=[]
    headurl = "https://web.pcc.gov.tw/tps"
    for s in sel:
        link = s['href'].replace('..','')
        url = headurl + link
        title = s['title']

        content = '{}\n{}\n'.format(title, url)
        a.append(content)

    for i in range(len(a)):
        if i % 2 == 0:
            b.append(a[i])
    return b


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://example.com/item1.jpg',
                title='this is menu1',
                text='description1',
                actions=[
                    URIAction(
                        label='uri1',
                        uri='http://example.com/1'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    URIAction(
                        label='uri2',
                        uri='http://example.com/2'
                    )
                ]
            )
        ]
    )
)

    if(event.message.text == '1'):
        line_bot_api.reply_message(event.reply_token,carousel_template_message)
    if(event.message.text == '查看招標資料'):
        a = getdata()
        b = " ".join(a)
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=b),TextSendMessage(text="共%s筆資料"%len(a))])


if __name__ == "__main__":
    app.run()


