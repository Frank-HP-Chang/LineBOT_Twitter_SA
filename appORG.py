from flask import Flask, jsonify, request, abort, send_file
from linebot import (LineBotApi, WebhookParser)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage)
import requests
from bs4 import BeautifulSoup
# ======這裡是呼叫的檔案內容=====
from fsm import *
# ======python的函數庫==========
import tempfile
import os
import sys
import json
import datetime
import time
# ======python的函數庫==========

app = Flask(__name__, static_url_path='')
machines = {}
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('7QDAXmZ5UqZssltAy2CJNEY2B1YnVzM/qqckpRyLSPkbUITT5DUYI3NaDddD70rMDbMcnlFs5PT5js+Z0mWGC5TDCcXoFSkrfcXXwXtTzusGIj/QSVtMFZU0XKi4XxkeYxw9ZRU40AlZ+FpdSDajvQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
parser = WebhookParser('ff325141242f29a7c6b270be1e9f3dc3')

machine = TocMachine(
    states=["user", "main_menu", "movie_menu", "ptt_menu", "new_movie","input_area","input_movieId",
            "input_date","recommend_movie", "movie_time","ptt_gossiping", "ptt_nba", "ptt_baseball", "show_fsm"],
    transitions=[
        {"trigger": "advance", "source": "user", "dest": "main_menu",
            "conditions": "is_going_to_main_menu"},
        {"trigger": "advance", "source": "main_menu", "dest": "main_menu",
            "conditions": "is_going_to_main_menu"},
        {"trigger": "advance", "source": "main_menu",
            "dest": "movie_menu", "conditions": "is_going_to_movie_menu"},
        {"trigger": "advance", "source": "main_menu",
            "dest": "ptt_menu", "conditions": "is_going_to_ptt_menu"},
        {"trigger": "advance", "source": "movie_menu",
            "dest": "new_movie", "conditions": "is_going_to_new_movie"},
        {"trigger": "advance", "source": "movie_menu", "dest": "recommend_movie",
            "conditions": "is_going_to_recommend_movie"},
        {"trigger": "advance", "source": "ptt_menu", "dest": "ptt_gossiping",
            "conditions": "is_going_to_ptt_gossiping"},
        {"trigger": "advance", "source": "ptt_menu",
            "dest": "ptt_nba", "conditions": "is_going_to_ptt_nba"},
        {"trigger": "advance", "source": "ptt_menu", "dest": "ptt_baseball",
            "conditions": "is_going_to_ptt_baseball", },
        {"trigger": "advance", "source": "main_menu", "dest": "show_fsm",
            "conditions": "is_going_to_show_fsm", },
        {"trigger": "advance", "source": ["movie_menu", "ptt_menu", "show_fsm"],
            "dest": "main_menu","conditions": "is_going_back"},
        {"trigger": "advance", "source": ["new_movie", "recommend_movie","movie_time"],
            "dest": "movie_menu","conditions": "is_going_back"},
        {"trigger": "advance", "source": ["ptt_gossiping", "ptt_nba", "ptt_baseball"], 
            "dest": "ptt_menu","conditions": "is_going_back"},
        {"trigger": "advance", "source": "movie_menu",
            "dest": "movie_time", "conditions": "is_going_to_movie_time"},
        {"trigger": "advance", "source": "movie_time",
            "dest": "input_area", "conditions": "is_going_to_input_area"},
        {"trigger": "advance", "source": "input_area",
            "dest": "input_movieId", "conditions": "is_going_to_input_movieId"},
        {"trigger": "advance", "source": "input_movieId",
            "dest": "input_date", "conditions": "is_going_to_input_date"},
        {"trigger": "advance", "source": "input_date",
            "dest": "movie_menu", "conditions": "is_going_back"},
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if(machine.state=='movie_time' and event.message.text=='h'):
                message = TextSendMessage(text="Not !")
                line_bot_api.reply_message(event.reply_token, message)
            else:
                message = TextSendMessage(text="Not Entering any State!")
                line_bot_api.reply_message(event.reply_token, message)
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
