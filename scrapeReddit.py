import requests
import os
from dotenv import load_dotenv
import praw
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import pyrebase

config = {
    "apiKey": "AIzaSyAo4gZZE5tc9g-do0RAXIjTAvwv-54YoA0",
    "authDomain": "hacklytics-2021-626b7.firebaseapp.com",
    "projectId": "hacklytics-2021-626b7",
    "storageBucket": "hacklytics-2021-626b7.appspot.com",
    "messagingSenderId": "1024219270230",
    "appId": "1:1024219270230:web:102279cff4ccdc45effff7"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

reddit = praw.Reddit(client_id='7pdHgJ0aNnIqkQ', client_secret='QU-vPCVM1dAO3beUcrIghrHraRoULA', user_agent='my_user_agent')

load_dotenv()
IBM_CLOUD_KEY = os.getenv('IBM_CLOUD_KEY')

authenticator = IAMAuthenticator(IBM_CLOUD_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)
natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/90774996-ec17-4440-b524-2c61f3a14481')

def extract_comments(post):
    # comment_text = []
    comment_text = ""
    post.comments.replace_more(limit=2)
    for top_level_comment in post.comments:
        # comment_text.append(top_level_comment.body)
        comment_text += " " + top_level_comment.body
    return comment_text

def weigh(post_data):
    score = post_data["score"]
    created = post_data["created"]
    num_comments = post_data["num_comments"]
    polarity = post_data["polarity"]

    impact = score + created / 100000 + num_comments * 10 + abs(2 - polarity) * 100 #TODO: adjust formula
    return impact

def sentimentAnalysis(posts):
    # # using Sentiment140 API
    # data = {"data": posts}
    # r = requests.post('http://www.sentiment140.com/api/bulkClassifyJson?appid=ro.agarwal@hotmail.com', data = data)
    # print(r.content)
    # return r.text #TODO: get response body properly, return ['data'] key's value

    # using IBM Watson NLU
    for post in posts:
        sentiment_response = natural_language_understanding.analyze(
            text=post["text"],
            features=Features(sentiment=SentimentOptions())).get_result()
        sentiment = sentiment_response['sentiment']['document']['score']
        post['polarity'] = sentiment * 2 + 2 # to align with Sentiment140 for ease
    return posts

def scrape():
    posts = []

    # get 10 hot posts from the WSB subreddit
    hot_posts = reddit.subreddit('WallStreetBets').hot(limit=1) #TODO: adjust limit
    for post in hot_posts:
        comments = extract_comments(post)
        posts.append({
            "title": post.title, 
            "score": post.score, 
            "id": post.id, 
            "subreddit": post.subreddit.display_name, 
            "url": post.url, 
            "num_comments": post.num_comments, 
            "selftext": post.selftext,
            "created": post.created,
            "comments": comments,
            "text": post.title + " " + post.selftext + " " + comments
        })
    
    return posts

def upload(stocks_data):
    for stock_data in stocks_data:
        old_data =  db.child("stocks").child(stock_data["title"]).get().val()
        if old_data != None and old_data != {}:
            db.child("stocks").child(stock_data["title"]).set({
                "polarity": (stock_data["polarity"] + 0.5 * old_data["polarity"]) / 1.5,
                "popularity": (stock_data["score"] + stock_data["created"] / 100000 + 0.5 * old_data["popularity"]) / 1.5,
                "engagement": (stock_data["num_comments"] + 0.5 * old_data["engagement"]) / 1.5,
                "weight": (stock_data["weight"] + 0.5 * old_data["weight"]) / 1.5
            })        
        else: 
            db.child("stocks").child(stock_data["title"]).set({
                "polarity": stock_data["polarity"],
                "popularity": stock_data["score"] + stock_data["created"] / 100000,
                "engagement": stock_data["num_comments"],
                "weight": stock_data["weight"]
            })


data = scrape()
data = sentimentAnalysis(data)
for i, item in enumerate(data):
    weight = weigh(item)
    item["weight"] = weight

print(data)