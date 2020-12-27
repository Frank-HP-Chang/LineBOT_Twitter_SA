# 這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from transitions.extensions import GraphMachine
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import pygraphviz
import tweepy
import numpy as np      
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
from identification import *  
from sentiment_analysis import *

mean = 0
fav_max = 0
rt_max = 0
fav = "NA"
rt = "NA"
global tweets
data = pd.DataFrame()

def twitter_menu():
    message = TemplateSendMessage(
        alt_text='Twitter選單',
        template=ButtonsTemplate(
            title='Twitter選單',
            text='若要返回上一層,請輸入:back',
            thumbnail_image_url='https://i.imgur.com/QRIa5Dz.jpg',
            actions=[
                MessageTemplateAction(
                    label='情緒分析',
                    text='情緒分析'
                ),
                MessageTemplateAction(
                    label='最多Like',
                    text='最多Like'
                ),
                MessageTemplateAction(
                    label='最多Re',
                    text='最多Re'
                ),
                MessageTemplateAction(
                    label='back',
                    text='back'
                )
            ]
        )
    ) 
    return message


def twitter_user(screen_name):
    extractor = twitter_setup()
    # We create a tweet list as follows:
    tweets = extractor.user_timeline(screen_name, count=100)
    print("Number of tweets extracted: {}.\n".format(len(tweets)))
    # We print the most recent 5 tweets:
    print("5 recent tweets:\n")
    for tweet in tweets[:5]:
        #print(tweet.text)
        print()    
    #global data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    global data
    data['Tweets'] = np.array([tweet.text for tweet in tweets])
    data['len']  = np.array([len(tweet.text) for tweet in tweets])
    data['ID']   = np.array([tweet.id for tweet in tweets])
    data['Date'] = np.array([tweet.created_at for tweet in tweets])
    data['Source'] = np.array([tweet.source for tweet in tweets])
    data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
    data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
    
    mean = np.mean(data['len'])

    fav_max = np.max(data['Likes'])
    rt_max  = np.max(data['RTs'])
    global fav
    fav = data[data.Likes == fav_max].index[0]
    global rt
    rt = data[data.RTs == rt_max].index[0]
    

line_bot_api = LineBotApi('7QDAXmZ5UqZssltAy2CJNEY2B1YnVzM/qqckpRyLSPkbUITT5DUYI3NaDddD70rMDbMcnlFs5PT5js+Z0mWGC5TDCcXoFSkrfcXXwXtTzusGIj/QSVtMFZU0XKi4XxkeYxw9ZRU40AlZ+FpdSDajvQdB04t89/1O/w1cDnyilFU=')
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)              
    #conditions
    def is_going_to_main_menu(self, event):
        text = event.message.text
        return text == '主選單'
    def is_going_to_input_user(self,event):
        text=event.message.text
        if(text=='Twitter'):
            return True
    def is_going_to_twitter_menu(self,event):
        #global user_id
        text = event.message.text
        #print(text)
        twitter_user(text)
        """
        if text.lower().isnumeric():
            user_id = text
            return True
        """
        return True
    def is_going_to_SA(self,event):
        text=event.message.text
        return text=='情緒分析'
    def is_going_to_mostLike(self,event):
        text=event.message.text
        return text=='最多Like'
    def is_going_to_mostRe(self,event):
        text=event.message.text
        return text == '最多Re'
    def is_going_to_show_fsm(self,event):
        text=event.message.text
        return text=='FSM'
    def is_going_back(self,event):
        text=event.message.text.lower()
        return text=='back'
        
    #states
    def on_enter_main_menu(self, event):
        message = main_menu()
        line_bot_api.reply_message(event.reply_token, message) 
    def on_enter_twitter_menu(self, event):
        #print("GOING DARK")
        message = twitter_menu()
        line_bot_api.reply_message(event.reply_token, message)
    def on_enter_new_movie(self,event):
        reply_arr=[]
        content = new_movie()
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    def on_enter_input_user(self,event):
        content='請輸入欲查詢Twitter ID:'+'\n'+"======================"+'\n'
        #content+=online_movie()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content)) 
    def on_enter_SA(self, event):
        print("來了")
        reply_arr = []
        content=""
        i=1
        for i in range(10):
            #content+=(map(str,data['SA'][i]))
            if (data['SA'][i] > 0):
                judge = "[正向] "
            elif (data['SA'][i] < 0):
                judge = "[負向] "
            else:
                judge = "[中性] "          
            content += (judge + data['Tweets'][i] + "\n")
        #print(type(content))
        #content = "Hello There"
        #print(type(content))
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    def on_enter_mostLike(self, event):
        reply_arr = []
        content = data['Tweets'][fav]
        print(type(content))
        #content = "Hello There"
        print(type(content))
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    def on_enter_mostRe(self, event):
        reply_arr = []
        content = data['Tweets'][rt]
        print(type(content))
        #content = "Hello There"
        print(type(content))
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr) 
    def on_enter_show_fsm(self,event):
        reply_arr=[]
        reply_arr.append(ImageSendMessage(original_content_url='https://i.imgur.com/Ii07SRo.png',preview_image_url='https://i.imgur.com/Ii07SRo.png'))
        message = TemplateSendMessage(
            alt_text='返回主選單',
            template=ButtonsTemplate(
                title=' ',
                text=' ',
                actions=[
                    MessageTemplateAction(
                        label='返回主選單',
                        text='back'
                    )
                ]
            )
        )
        reply_arr.append(message)
        line_bot_api.reply_message(event.reply_token, reply_arr)



def back_movie_button():
    message = TemplateSendMessage(
        alt_text='返回主選單',
        template=ButtonsTemplate(
            title=' ',
            text=' ',
            #thumbnail_image_url='https://i.imgur.com/QRIa5Dz.jpg',
            actions=[
                MessageTemplateAction(
                    label='返回Twitter選單',
                    text='back'
                )
            ]
        )
    )
    return message


def main_menu():
    message = TemplateSendMessage(
        alt_text='主選單',
        template=ButtonsTemplate(
            title='主選單',
            text='若要返回上一層,請輸入:back',
            thumbnail_image_url='https://i.imgur.com/QRIa5Dz.jpg',
            actions=[
                MessageTemplateAction(
                    label='Twitter',
                    text='Twitter'
                ),
                MessageTemplateAction(
                    label='FSM',
                    text='FSM'
                )
            ]
        )
    )
    return message







