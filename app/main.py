from fastapi import FastAPI
from fastapi.responses import JSONResponse
from facebook_scraper import get_posts,set_user_agent
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional, Dict, List
from urllib.parse import quote_plus
import os


app = FastAPI()
client = None

#set up a MongoDB client
def get_client():
    global client
    if bool(client):
        return client
    host = os.getenv('MONGODB_HOST', '')
    username = os.getenv('MONGODB_USER', '')
    password = os.getenv('MONGODB_PASSWORD', '')
    port = int(os.getenv('MONGODB_PORT', 27017))
    endpoint = 'mongodb://{0}:{1}@{2}:{3}'.format(quote_plus(username),
                                              quote_plus(password), host,port)
    client = MongoClient(endpoint)
    return client




class Post(BaseModel):
    post_id: str
    link: str =None
    text: str =None
    date: str =None
    page_name: str =None
    No_shares:Optional[int] =0
    comments: Optional[List[Dict]] = None
    


@app.post('/scraping/posts', response_model=str)
async def scrape_post(url: str='',pages:int=3):
    countInsert=0
    countUpdate=0
    get_client()
    db = client.posts
    for post in get_posts(url, pages=pages,options={"comments": True,"reactions": True}): 
        if post['comments_full'] != None:
            commentsDict = [{'text': comment['comment_text'], 'date': comment['comment_time'],
                 'link': comment['comment_url'],'commentor': comment['commenter_name']} for comment in post['comments_full']]
        p=db.reviews.find_one({'post_id':post['post_id']})
        postDict=Post(post_id=post['post_id'],link=post['link'], text=post['post_text'], date=str(post['time']),
                        page_name=post['username'], comments=commentsDict,No_shares=post['shares']).__dict__
        if p == None:
            resulti=db.reviews.insert_one(postDict)
            countInsert += 1
            print('Inserted {0} as {1}'.format(countInsert,resulti.inserted_id))
        else:
            db.reviews.update_one({'post_id':post['post_id']},{"$set":postDict})
            countUpdate += 1
            print('Updated {0} '.format(p['_id']))  
    return JSONResponse(content='finished scrapping {0} posts'.format(countInsert+countUpdate))    
    

