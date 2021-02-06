import requests
import praw

reddit = praw.Reddit(client_id='7pdHgJ0aNnIqkQ', client_secret='QU-vPCVM1dAO3beUcrIghrHraRoULA', user_agent='my_user_agent')

def extract_comments(post):
    comment_text = ""
    post.comments.replace_more(limit=8)
    for top_level_comment in post.comments:
        comment_text += " " + top_level_comment.body
    return comment_text

def scrape():
    posts = []

    # get 10 hot posts from the WSB subreddit
    hot_posts = reddit.subreddit('WallStreetBets').hot(limit=25)
    for post in hot_posts:
        posts.append({
            "title": post.title, 
            "score": post.score, 
            "id": post.id, 
            "subreddit": post.subreddit.display_name, 
            "url": post.url, 
            "num_comments": post.num_comments, 
            "selftext": post.selftext,
            "created": post.created,
            "comments": extract_comments(post)
        })
    
    return posts


data = scrape()
print(data)