import requests
import praw

reddit = praw.Reddit(client_id='7pdHgJ0aNnIqkQ', client_secret='QU-vPCVM1dAO3beUcrIghrHraRoULA', user_agent='my_user_agent')

posts = []

# get 10 hot posts from the WSB subreddit
hot_posts = reddit.subreddit('WallStreetBets').hot(limit=10)
for post in hot_posts:
    print(post.title)
    posts.append({})
