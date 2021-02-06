import requests
import praw

reddit = praw.Reddit(client_id='7pdHgJ0aNnIqkQ', client_secret='QU-vPCVM1dAO3beUcrIghrHraRoULA', user_agent='my_user_agent')

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

    impact = score + created / 100000 + num_comments * 10 + abs(2 - polarity) * 100
    return impact

def sentimentAnalysis(posts):
    # using Sentiment140 API
    data = {"data": posts}
    r = requests.post('http://www.sentiment140.com/api/bulkClassifyJson?appid=ro.agarwal@hotmail.com', data = data)
    print(r.content)
    return r.text #TODO: get response body properly, return ['data'] key's value


def scrape():
    posts = []

    # get 10 hot posts from the WSB subreddit
    hot_posts = reddit.subreddit('WallStreetBets').hot(limit=1)
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


data = scrape()
data = sentimentAnalysis(data)
for i, item in enumerate(data):
    weight = weigh(item)
    data.append({"weight": weight})

print(data)