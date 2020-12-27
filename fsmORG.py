# 這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from bs4 import BeautifulSoup
from transitions.extensions import GraphMachine
import requests
import re
#import pygraphviz

line_bot_api = LineBotApi('7QDAXmZ5UqZssltAy2CJNEY2B1YnVzM/qqckpRyLSPkbUITT5DUYI3NaDddD70rMDbMcnlFs5PT5js+Z0mWGC5TDCcXoFSkrfcXXwXtTzusGIj/QSVtMFZU0XKi4XxkeYxw9ZRU40AlZ+FpdSDajvQdB04t89/1O/w1cDnyilFU=')
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)              
    #conditions
    def is_going_to_main_menu(self, event):
        text = event.message.text
        return text == 'menu'
    def is_going_to_movie_menu(self,event):
        text=event.message.text
        if(text=='movie'):
            return True
    def is_going_to_new_movie(self,event):
        text=event.message.text
        return text=='本周新片'
    def is_going_to_recommend_movie(self,event):
        text=event.message.text
        return text=='近期上映電影'
    def is_going_to_ptt_menu(self,event):
        text=event.message.text
        return text=='PTT'
    def is_going_to_ptt_gossiping(self,event):
        text=event.message.text
        return text=='八卦'
    def is_going_to_ptt_nba(self,event):
        text=event.message.text
        return text=='NBA'
    def is_going_to_ptt_baseball(self,event):
        text=event.message.text
        return text=='棒球'
    def is_going_to_show_fsm(self,event):
        text=event.message.text
        return text=='FSM'
    def is_going_back(self,event):
        text=event.message.text.lower()
        return text=='back'
    def is_going_to_movie_time(self,event):
        text=event.message.text
        return text=='電影時刻查詢'
    def is_going_to_input_area(self,event):
        global area_id
        text = event.message.text
        if text.lower().isnumeric():
            area_id = int(text)
            return True
        return False
    def is_going_to_input_movieId(self,event):
        global movie_id
        text = event.message.text
        if text.lower().isnumeric():
            movie_id = int(text)
            return True
        return False
    def is_going_to_input_date(self,event):
        global date
        date = event.message.text
        return True
        
    #states
    def on_enter_main_menu(self, event):
        message = main_menu()
        line_bot_api.reply_message(event.reply_token, message) 
    def on_enter_movie_menu(self,event):
        message = movie_menu()
        line_bot_api.reply_message(event.reply_token, message)
    def on_enter_new_movie(self,event):
        reply_arr=[]
        content = new_movie()
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr) 
    def on_enter_recommend_movie(self,event):
        reply_arr=[]
        content = recommend_movie()
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr) 
    def on_enter_movie_time(self,event):
        content='請輸入欲查詢地區之代號:'+'\n'+"======================"+'\n'+'放映地區: 台北, 代號: 28'+'\n'+'放映地區: 新北, 代號: 8' +'\n'+'放映地區: 桃園, 代號: 16'+'\n'+'放映地區: 新竹, 代號: 20'+'\n'+'放映地區: 台中, 代號: 2'+'\n'+'放映地區: 嘉義, 代號: 21'+'\n'+'放映地區: 台南, 代號: 10'+'\n'+'放映地區: 高雄, 代號: 17'+'\n'+'放映地區: 屏東, 代號: 14'+'\n'+'放映地區: 花蓮, 代號: 12'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content)) 
    def on_enter_input_area(self,event):
        content='請輸入欲查詢電影之代號:'+'\n'+"======================"+'\n'
        content+=online_movie()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content)) 
    def on_enter_input_movieId(self,event):
        global movie_id,area_id
        content='從下列日期中選擇欲查詢日期:'+'\n'+"======================"+"\n"
        url = 'https://movies.yahoo.com.tw/movietime_result.html'
        payload = {'movie_id':str(movie_id), 'area_id':str(area_id)}
        resp = requests.get(url, params=payload)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        movie_date = soup.find_all("label", attrs={'for':re.compile("date_[\d]")})
        for date in movie_date:
            content+=date.p.string+" "+date.h3.string+"\n"

        content+="如要查詢2020 十二月 23"+'\n'+"請輸入『2020-12-23』"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content)) 
    def on_enter_input_date(self,event):
        global area_id,movie_id,date
        reply_arr=[]
        content=find_movietime(movie_id,area_id,date)
        reply_arr.append(TextSendMessage(text=content))
        content1=back_movie_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr)  
    def on_enter_ptt_menu(self,event):
        message = ptt_menu()
        line_bot_api.reply_message(event.reply_token, message)
    def on_enter_ptt_gossiping(self,event):
        reply_arr=[]
        content = crawl_ptt('Gossiping')
        reply_arr.append(TextSendMessage(text=content))
        content1=back_ptt_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr)   
    def on_enter_ptt_nba(self,event):
        reply_arr=[]
        content = crawl_ptt('NBA')
        reply_arr.append(TextSendMessage(text=content))
        content1=back_ptt_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr) 
    def on_enter_ptt_baseball(self,event):
        reply_arr=[]
        content = crawl_ptt('Baseball')
        reply_arr.append(TextSendMessage(text=content))
        content1=back_ptt_button()
        reply_arr.append(content1)
        line_bot_api.reply_message(event.reply_token, reply_arr)
    def on_enter_show_fsm(self,event):
        reply_arr=[]
        reply_arr.append(ImageSendMessage(original_content_url='https://i.imgur.com/MrKfdWn.png',preview_image_url='https://i.imgur.com/2WtSoHI.png'))
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

def online_movie():
    # 搜尋目前上映那些電影，擷取出其ID資訊
    url = 'https://movies.yahoo.com.tw/'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    movie_html = soup.find("select", attrs={'name': 'movie_id'})
    movie_item = movie_html.find_all("option", attrs={'data-name': re.compile('.*')})
    content=''
    # 因為moite_item 是一個bs4的元素集合，我們要用遍歷去探索它:
    for info in movie_item:
        content+=info["value"]+": "+info["data-name"]+"\n"
    return content

def find_movietime(movie_id,area_id,date):
    url = "https://movies.yahoo.com.tw/ajax/pc/get_schedule_by_movie"
    payload = {'movie_id': str(movie_id),'date': date,'area_id': str(area_id),'theater_id': '','datetime': '','movie_type_id': ''}
    resp = requests.get(url, params=payload)
    json_data = resp.json()
    content=''
    try:
        soup = BeautifulSoup(json_data['view'], 'html.parser')
    except:
        return content=='查無此電影場次'
    html_elem = soup.find_all("ul", attrs={'data-theater_name': re.compile(".*")})
    # 每個the就是一間戲院
    for the in html_elem:
        theater = the.find("li", attrs={"class": "adds"})
    # info裡面分別包含每一間戲院的場次資訊
        info = the.find_all(class_="gabtn")
        content+="======================"+"\n"+"電影院：{}".format(theater.find("a").text)+"\n"
        for i in info:
            content+=i["data-movie_time"]+" "+i["data-movie_type"]+'\n'
    if(content==''):
        content='查無此電影場次'
    else:
        content+="======================"
    return content   

def back_movie_button():
    message = TemplateSendMessage(
        alt_text='返回電影選單',
        template=ButtonsTemplate(
            title=' ',
            text=' ',
            #thumbnail_image_url='https://i.imgur.com/QRIa5Dz.jpg',
            actions=[
                MessageTemplateAction(
                    label='返回電影選單',
                    text='back'
                )
            ]
        )
    )
    return message
def back_ptt_button():
    message = TemplateSendMessage(
        alt_text='返回PTT選單',
        template=ButtonsTemplate(
            title=' ',
            text=' ',
            actions=[
                MessageTemplateAction(
                    label='返回PTT選單',
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
                    label='電影',
                    text='電影'
                ),
                MessageTemplateAction(
                    label='PTT',
                    text='PTT'
                ),
                MessageTemplateAction(
                    label='FSM',
                    text='FSM'
                )
            ]
        )
    )
    return message


def movie_menu():
    message = TemplateSendMessage(
        alt_text='電影選單',
        template=ButtonsTemplate(
            title='電影選單',
            text='若要返回上一層,請輸入:back',
            thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
            actions=[
                MessageTemplateAction(
                    label='近期上映電影',
                    text='近期上映電影'
                ),
                MessageTemplateAction(
                    label='本周新片',
                    text='本周新片'
                ),
                MessageTemplateAction(
                    label='電影時刻查詢',
                    text='電影時刻查詢'
                ),
                MessageTemplateAction(
                    label='返回主選單',
                    text='back'
                )
            ]
        )
    )
    return message

def new_movie():
    target_url='http://www.atmovies.com.tw/movie/new/'
    rs=requests.session()
    res=rs.get(target_url, verify=False)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text, 'html.parser')
    content=""
    for i, data in enumerate(soup.select('div.filmTitle a')):
        if i > 20:
            break
        content += data.text + "\n" +"http://www.atmovies.com.tw/" + data['href'] + "\n\n"
    
    return content


def recommend_movie():
    target_url='http://www.atmovies.com.tw/movie/next/'
    rs=requests.session()
    res=rs.get(target_url, verify=False)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text, 'html.parser')
    content=""
    for i, data in enumerate(soup.select('div.filmtitle a')):
        if i > 20:
            break
        content += data.text + "\n" +"http://www.atmovies.com.tw/" + data['href'] + "\n\n"
    return content

def ptt_menu():
    message = TemplateSendMessage(
        alt_text='PTT選單',
        template=ButtonsTemplate(
            title='PTT選單',
            text='若要返回上一層,請輸入:back',
            thumbnail_image_url='https://i.imgur.com/d7nVN8F.jpg',
            actions=[
                MessageTemplateAction(
                    label='八卦',
                    text='八卦'
                ),
                MessageTemplateAction(
                    label='NBA',
                    text='NBA'
                ),
                MessageTemplateAction(
                    label='棒球',
                    text='棒球'
                ),
                MessageTemplateAction(
                    label='返回主選單',
                    text='back'
                )
            ]
        )
    )
    return message

def get_page_number(content):
    start_index=content.find('index')
    end_index=content.find('.html')
    page_number=content[start_index + 5: end_index]
    return int(page_number) + 1


def crawl_page(res):
    soup=BeautifulSoup(res.text, 'html.parser')
    article_plate=[]
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link=r_ent.find('a')['href']

            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title=r_ent.find(class_="title").text.strip()
                url_link='https://www.ptt.cc' + link
                article_plate.append({
                    'url_link': url_link,
                    'title': title
                })

        except Exception as e:
            print('delete', e)
    return article_plate


def crawl_ptt(plate):
    rs=requests.session()
    load={
        'from': '/bbs/'+plate+'/index.html',
        'yes': 'yes'
    }
    res=rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    soup=BeautifulSoup(res.text, 'html.parser')
    all_page_url=soup.select('.btn.wide')[1]['href']
    start_page=get_page_number(all_page_url)
    index_list=[]
    article_plate=[]
    for page in range(start_page, start_page - 2, -1):
        page_url='https://www.ptt.cc/bbs/'+plate+'/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index=index_list.pop(0)
        res=rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
        else:
            article_plate=crawl_page(res)
    content=''
    for index, article in enumerate(article_plate, 0):
        if index == 15:
            return content
        data='{}\n{}\n\n'.format(article.get(
            'title', None), article.get('url_link', None))
        content += data
    return content

