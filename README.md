# LineBot_Twitter_SA
## Intro
It is a Line ChatBot. You can use it to get Twitter user tweets and other information. <br />
Includeing:
<br />
* SA(Sentiment Analysis)
* Most Like Tweets
* Most ReTweet Twees 
<br />

Also you can get **FSM graph** by using the BOT


## How to use
### Install kit
```
pip install -r requirements.txt
```
### Run
```
python app.py
```

## Deploy
```
heroku login
heroku git:remote -a HEROKU_APP_NAME
git add .
git push -f heroku master  
Heroku logs --tail -a HEROKU_APP_NAME
```

## Ref
[Textblob](https://textblob.readthedocs.io/en/dev/quickstart.html)

[Twitter API](https://developer.twitter.com/en/docs)

