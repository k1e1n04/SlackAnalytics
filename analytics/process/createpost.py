from analytics.models import Post
from django.conf import settings
from datetime import datetime
import requests
import time


#メンバー登録時の処理↓
def get_slack_posts(channel,ago,employee):
    SLACK_URL = settings.SLACK_URL
    TOKEN = settings.TOKEN
    payload = {
        "channel" : channel.channel_id,
        "user_id" : employee.slack_id,
        "oldest" : ago
    }
    headersAuth = {
        'Authorization' : 'Bearer ' + str(TOKEN), 
    }
    response = requests.get(SLACK_URL, headers=headersAuth, params=payload)
    json_data = response.json()
    msgs = json_data['messages']
    time.sleep(1)
    return msgs


def analytics_preparation(msgs,employee):
    messages = []
    i=1
    for m in msgs:
        if m.get('user')==employee.slack_id:
            dt = float(m.get('ts'))
            object = {'id': i,'ts' : datetime.fromtimestamp(dt)}
            messages.append(object)
            i += 1
    return messages


def make_post(c,employee,messages):
    for message in messages:
        try:
            Post.objects.create(channel=c,base=c.base,employee=employee,created_at=message["ts"])
        except:
            continue