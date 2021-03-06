#-*- coding: utf-8 -*-
import  requests
# from django.conf import settings
# from celery import Celery
# BROKER='redis://127.0.0.1:6379/1'
# celery=Celery('tasks',broker=BROKER)
from celeryconfig import celery
from bcrobot import settings
from bcstart.models import Subscriber
from hacknews.hnapi import HackerNewsAPI
import json

@celery.task(name="app.tasks.add")
def add(x, y):
    z = x + y
    print("{} + {} = {}".format(x, y, z))
    return z

    #
    # r=requests.post(settings.BC_WEBHOOK,json=payload,headers=headers)
    # if r.ok:
    #     return True
    # else:
    #     return False
    # data = {"payload": '{"text":"notify from celery"}'}
    # session = requests.Session()
    # r2 = session.post(url=settings.BC_WEBHOOK, data=data)
    # if r2.ok:
    #     return True
    # else:
    #     return False

@celery.task
def publish_server():
    data={"text":u"来自服务器的消息","attachments":[{"title":u"服务器运行状况","text":u"正常","color":"#ffa500"}]}
    headers = {'content=type': 'application/json'}
    #notify all user
    subscribers=Subscriber.objects.filter(subtype='server')
    for item in subscribers:
        data['text']="@"+item.username+" "+data['text']
        # r=requests.post(item.url,json=data,headers=headers )
        r=requests.post(item.url,data={'payload':json.dumps(data)})

        print r
        if not r.ok:
            print 'error in publish function'
    #

@celery.task
def publish_hn():
    api=HackerNewsAPI()
    stories=api.getNewestStories(1)
    attachments=[]
    for item in stories:
        attadict={}
        attadict['title']=item.title
        attadict['text']="["+item.title +"]("+ item.URL+")"
        attadict['color']='#ffa500'
        attachments.append(attadict)

    data={"text":"HackNews","attachments":attachments}
    headers = {'content=type': 'application/json'}
    #notify all user
    subscribers=Subscriber.objects.filter(subtype='hackernews')
    for item in subscribers:
        data['text']="@"+item.username+" "+data['text']
        # r=requests.post(item.url,json=data,headers=headers )
        r=requests.post(item.url,data={'payload':json.dumps(data)})

        print r
        if not r.ok:
            print 'error in publish function'

@celery.task
def publish_weather():
    attachments=[]
    data={"text":"Weather","markdown":True,"attachments":attachments}
    headers = {'content=type': 'application/json'}
    #notify all user
    subscribers=Subscriber.objects.filter(subtype='weather')
    for item in subscribers:
        data['text']="@"+item.username+" "+data['text']
        # r=requests.post(item.url,json=data,headers=headers )
        r=requests.post(item.url,data={'payload':json.dumps(data)})
        print r
        if not r.ok:
            print 'error in publish function'




