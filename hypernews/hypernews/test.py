from settings import NEWS_JSON_PATH
import json

with open('/Users/eek/PycharmProject/HyperNews Portal/HyperNews Portal/task/news.json') as f:
    print(len(json.load(f)))