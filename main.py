from googleapiclient.discovery import build
from pymongo import MongoClient

MONGO_CLIENT = ""

cluster = MongoClient("")
db = cluster["YTv3"]
collection = db["YTv3"]

DEVELOPER_KEY = "" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
   
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                                        developerKey = DEVELOPER_KEY)
   
   
def youtube_search_keyword(query, max_results):
       
    search_keyword = youtube_object.search().list(part = "snippet", q = query,
                                               maxResults = max_results).execute()
       
    title = []
    description = []
    publishedAt = []
    dict = {}

    max_num = 0

    for i in search_keyword['items']:
        if title.index(i['snippet']['title']) == -1:
            title.append(i['snippet']['title'])
            description.append(i['snippet']['description'])
            publishedAt.append(i['snippet']['publishedAt'])
        else:
            max_num += 1

    dict['title'] = title
    dict['description'] = description
    dict['publishedAt'] = publishedAt
    collection.insert_one(dict)

    val = max_results - max_num
    if val != 0:
        youtube_search_keyword(query, val)

if __name__ == "__main__":
    youtube_search_keyword('Apple', max_results = 100)