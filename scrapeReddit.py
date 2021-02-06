import requests
import praw

reddit = praw.Reddit(client_id='7pdHgJ0aNnIqkQ', client_secret='QU-vPCVM1dAO3beUcrIghrHraRoULA', user_agent='my_user_agent')

def extract_comments(post):
    comment_text = []
    post.comments.replace_more(limit=8)
    for top_level_comment in post.comments:
        comment_text.append(top_level_comment.body)
    return comment_text

def weigh(post_data):
    score = post_data["score"]
    created = post_data["created"]
    num_comments = post_data["num_comments"]
    polarity = post_data["polarity"] #TODO: check for field name

    impact = score + created / 100000 + num_comments * 10 + abs(2 - polarity) * 100
    return impact

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
for i, item in enumerate(data):
    weight = weigh(item)
    data.append({"weight": weight})

print(data)