from .models import Post
from django.conf import settings
from datetime import datetime
import requests
import json
from django.db.models import Avg
import time
#ダッシュボードの共通部分の処理
def return_compare_posts_conut(one_week_posts,two_week_posts):
    one_week_posts_count = len(one_week_posts)
    two_week_posts_count = len(two_week_posts)
    compare_posts_count = one_week_posts_count-two_week_posts_count
    return one_week_posts_count,compare_posts_count,two_week_posts_count

#メンバー登録時の処理↓
def get_slack_posts(channels,ago,form):
    SLACK_URL = settings.SLACK_URL
    TOKEN = settings.TOKEN
    for c in channels:
        payload = {
            "channel" : c.channel_id,
            "user_id" : form.slack_id,
            "oldest" : ago
        }
        headersAuth = {
            'Authorization' : 'Bearer ' + str(TOKEN), 
        }
        response = requests.get(SLACK_URL, headers=headersAuth, params=payload)
        json_data = response.json()
        msgs = json_data['messages']
        analytics_preparation(msgs,form,c)
        time.sleep(1.2)


def analytics_preparation(msgs,form,c):
    messages = []
    i=1
    for m in msgs:
        if m.get('user')==form.slack_id:
            dt = float(m.get('ts'))
            object = {'id': i,'ts' : datetime.fromtimestamp(dt)}
            messages.append(object)
            i += 1
    make_post(c,form,messages)


def make_post(c,employee,messages):
    for message in messages:
        try:
            Post.objects.create(channel=c,base=c.base,employee=employee,created_at=message["ts"])
        except:
            continue

        