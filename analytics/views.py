from multiprocessing import context
from django.shortcuts import render
from random import randint
from django.views import generic
import requests
import json
from datetime import datetime
from pytz import timezone, utc
from tzlocal import get_localzone
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = "d79573f2f43541c09112691e2dd2ee57"
credentials = CognitiveServicesCredentials(subscription_key)
text_analytics_url = "https://slackanalytics.cognitiveservices.azure.com/"
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)

SLACK_CHANNEL_ID = 'C035M8NL7PD'
SLACK_URL = "https://slack.com/api/conversations.history"
TOKEN = "xoxp-1668835028433-1680046787136-3560202701600-3cb166e1d51c5d1c6d1e4a6a85ddd828"

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
    