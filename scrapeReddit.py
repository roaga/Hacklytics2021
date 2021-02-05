import requests
import praw

reddit = praw.Reddit(client_id='my_client_id', client_secret='my_client_secret', user_agent='my_user_agent')

posts = []

# get 10 hot posts from the WSB subreddit
hot_posts = reddit.subreddit('WallStreetBets').hot(limit=10)
for post in hot_posts:
    print(post.title)
    posts.append({})
