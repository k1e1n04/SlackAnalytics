from multiprocessing import context
from django.shortcuts import render
from random import randint
from django.views import generic
import requests
import json
import os
from datetime import datetime
from pytz import timezone, utc
from tzlocal import get_localzone
from dotenv import load_dotenv
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
load_dotenv('.env') 

subscription_key = os.environ.get("subscription_key")
credentials = CognitiveServicesCredentials(subscription_key)
text_analytics_url = os.environ.get("text_analytics_url")
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)

SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_URL = os.environ.get("SLACK_URL")
TOKEN = os.environ.get("TOKEN")

def toya_analytics(request):
    payload = {
        "channel" : SLACK_CHANNEL_ID,
        "oldest" : "1622761200"
    }
    headersAuth = {
        'Authorization' : 'Bearer ' + str(TOKEN), 
    }
    response = requests.get(SLACK_URL, headers=headersAuth, params=payload)
    json_data = response.json()
    msgs = json_data['messages']

    messages = []
    i = 1
    for d in msgs:
        if d.get('user')=='U029RBMMZC7':
            dt = float(d.get('ts'))
            object = {'id': i,'language': 'ja','text' : d.get('text').replace('\n',''),'ts' : datetime.fromtimestamp(dt)}
            messages.append(object)
            i += 1
    def json_serial(obj):
        if isinstance(obj, (datetime)):
            return obj.isoformat()
        raise TypeError (f'Type {obj} not serializable')

    documents = json.dumps(messages, ensure_ascii=False,indent=4,default=json_serial)
    perse_documents = json.loads(documents)
    response = text_analytics.sentiment(documents=perse_documents)
    j = 0
    for document in response.documents:
        messages[j]["score"] = document.score
        j += 1

    context = {'emotions':messages}


    return render(request,'analytics/analytics_list.html',context)
    