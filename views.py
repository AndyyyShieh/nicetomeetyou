from django.shortcuts import render

# Create your views here.
from bs4 import BeautifulSoup
import re
import urllib
from .models import News as newsModel
from .serializers import NewsSerializer
from rest_framework import viewsets

from django.http import HttpResponse
import requests

# Create your views here.
class NewsViewSet(viewsets.ModelViewSet):
    queryset = newsModel.objects.all()
    serializer_class = NewsSerializer


def newscrawler(request):

    url = 'https://nba.udn.com/nba/index?gr=www'   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')
    sp = BeautifulSoup(data, "html.parser")
 
    title = []
    titles = sp.find("div", {"class":"box_body"}).findAll("h3")
    for title1 in titles:
        title.append(title1.text)
 
    link = []
    links = sp.find("div", {"class":"box_body"}).findAll("a")
    for link1 in links:
        link.append('https://nba.udn.com' + link1['href'])
    
    for i in range(3):
        try:
            check = newsModel.objects.get(title = title[i])
        except newsModel.MultipleObjectsReturned:
        	check = newsModel.objects.filter(title = title[i]).first()
        except newsModel.DoesNotExist:
            check = None
        if check == None:
            newsModel.objects.create(title = title[i], link = link[i])
            #render(request, "newscrawler.html", {'isNew': title[i]})
    
    all = zip(title, link)
    return HttpResponse(render(request, "newscrawler.html", locals()))
