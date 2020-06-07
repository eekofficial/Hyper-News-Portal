from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import json
from hypernews.settings import NEWS_JSON_PATH
from collections import defaultdict
import datetime
import random
from django.shortcuts import redirect

class NewObject:
    def __init__(self, new_elem):
        self.created = new_elem['created']
        self.title = new_elem['title']
        self.link = new_elem['link']
        self.text = new_elem['text']

def get_news_list():
    with open(NEWS_JSON_PATH) as f:
        data = json.load(f)
    return data

def unique_id(news_list):
    used_id = dict()
    for new in news_list:
        used_id[new['link']] = 1
    new_id = random.randint(1, 100000000)
    while new_id in used_id:
        new_id = random.randint(1, 100000000)
    return new_id


def find_news(news_id):
    with open(NEWS_JSON_PATH) as f:
        data_list = json.load(f)
    for new in data_list:
        if new['link'] == int(news_id):
            return new
    return dict()

def add_new(news_list):
    with open(NEWS_JSON_PATH, 'w') as f:
        json.dump(news_list, f)

def find_news_by_date(q):
    news_dict = defaultdict(list)
    with open(NEWS_JSON_PATH) as f:
        data_list = json.load(f)
    for new in data_list:
        date_with_time = datetime.datetime.strptime(new['created'], '%Y-%m-%d %H:%M:%S')
        if q:
            if q.lower() in new['title'].lower():
                news_dict[date_with_time].append(NewObject(new))
        else:
            news_dict[date_with_time].append(NewObject(new))
    print(news_dict)
    sorted_news_dict = defaultdict(list)
    for date in sorted(news_dict.keys(), reverse=True):
        str_date = datetime.datetime.strftime(date.date(), '%Y-%m-%d')
        sorted_news_dict[str_date].extend(news_dict[date])
    sorted_news_dict = dict(sorted_news_dict)
    print(sorted_news_dict.items())
    return sorted_news_dict

class MainPageView(View):
    def get(self, request):
        return render(request, 'news/welcome.html')

class AllNewsView(View):
    def get(self, request):
        news = find_news_by_date(request.GET.get('q'))
        return render(request, 'news/index.html', {'news': news})

class NewsView(View):
    def get(self, request, news_id):
        new = find_news(news_id)
        params = {
            'title': new.get('title'),
            'created': new.get('created'),
            'text': new.get('text')
        }
        return render(request, 'news/news_by_id.html', params)

class CreateNewsView(View):
    def get(self, request):
        return render(request, 'news/create_news.html')

    def post(self, request):
        news_list = get_news_list()
        new = {
            'link': unique_id(news_list),
            'title':request.POST.get('title'),
            'text': request.POST.get('text'),
            'created': datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
        }
        news_list.append(new)
        add_new(news_list)
        return redirect('/news')




