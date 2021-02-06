import requests
import os
from dotenv import load_dotenv
import praw
from pandas import DataFrame
import re
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
# import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./firebaseserviceaccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

reddit = praw.Reddit(client_id='7pdHgJ0aNnIqkQ', client_secret='QU-vPCVM1dAO3beUcrIghrHraRoULA', user_agent='my_user_agent')

load_dotenv()
IBM_CLOUD_KEY = os.getenv('IBM_CLOUD_KEY')

authenticator = IAMAuthenticator(IBM_CLOUD_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)
natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/90774996-ec17-4440-b524-2c61f3a14481')

def get_stock_stats(posts):
    stocks = []
    with open('stocknames.txt') as f:
        next(f) #skip header
        for stock in f:
            stock = re.split('[|]',stock)
            symbol = stock[0]
            name = stock[1]
            count = 0
            polarity = 0
            weight = 0
            score = 0
            for post in posts:
                count+=len(re.findall(symbol,post['text']))  #TODO: match case, match only if there is a space after 
                #count+=len([m.start() for m in re.finditer(symbol, post['text'])]) #find number of occurences in text
                if count > 0 :
                    polarity+=post['polarity'] #add post polarity to the stock
                    weight+=post['weight'] #add weight of post to the stock
                    score+=post['score']

            stocks.append({
                symbol +'-' + name :
                {
                "title": symbol +'-' + name,
                "polarity": polarity,
                "score" : score,
                "weight": weight,
                "num_comments" : count,
                }
            })

    print(stocks[4])

    #dataframe
    # df = DataFrame(stocks) #convert list to dataframe
    # if os.path.exists("stocks.txt"):
    #     os.remove("stocks.txt")
    # df.to_csv(r'stocks.txt', header=None, index=None, sep=' ', mode='a') #print to txt file for viewing
            

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
    # return r.text #does not get response body properly, return ['data'] key's value

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
    hot_posts = reddit.subreddit('WallStreetBets').hot(limit=10) #TODO: adjust limit
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
    old_stocks_stream = db.collection("stocks").stream()
    old_stocks = {}
    for doc in old_stocks_stream:
        old_stocks[doc.id] = doc.to_dict()

    for stock_data in stocks_data.values():
        old_data = old_stocks[stock_data["title"]] if stock_data["title"] in old_stocks else None
        if old_data != None and old_data != {}:
            db.collection("stocks").document(stock_data["title"]).set({
                "title": stock_data["title"],
                "polarity": (stock_data["polarity"] + 0.5 * old_data["polarity"]) / 1.5,
                "popularity": (stock_data["score"] + stock_data["created"] / 100000 + 0.5 * old_data["popularity"]) / 1.5,
                "engagement": (stock_data["num_comments"] + 0.5 * old_data["engagement"]) / 1.5,
                "weight": (stock_data["weight"] + 0.5 * old_data["weight"]) / 1.5
            })        
        else: 
            db.collection("stocks").document(stock_data["title"]).set({
                "title": stock_data["title"],
                "polarity": stock_data["polarity"],
                "popularity": stock_data["score"] + stock_data["created"] / 100000,
                "engagement": stock_data["num_comments"],
                "weight": stock_data["weight"]
            })


#TODO: put on periodic loop
data = scrape()
data = sentimentAnalysis(data)
for i, item in enumerate(data):
    #print(item)
    weight = weigh(item)
    item["weight"] = weight

#print(data[0]["text"])
get_stock_stats(data)

#upload(None)
