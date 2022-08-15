from .models import Channel, Post
from django.conf import settings
from datetime import datetime
import requests
import json
from django.db.models import Avg
import time
#各部署のチャンネルへの投稿数の配列を返す
def return_departments_posts_count(departments,employee,month):
    departments_posts_count = []
    for department in departments:
        channels = Channel.objects.filter(department=department)
        department_posts = Post.objects.filter(employee=employee,channel__in=channels,created_at__gt=month)
        department_posts_count = len(department_posts)
        departments_posts_count.append(department_posts_count)
    return departments_posts_count

#2期間の投稿数の比較
def return_compare_posts_conut(one_week_posts,two_week_posts):
    one_week_posts_count = len(one_week_posts)
    two_week_posts_count = len(two_week_posts)
    compare_posts_count = one_week_posts_count-two_week_posts_count
    return one_week_posts_count,compare_posts_count,two_week_posts_count

#メンバー登録時の処理↓
def get_slack_posts(channels,ago,employee):
    SLACK_URL = settings.SLACK_URL
    TOKEN = settings.TOKEN
    for c in channels:
        payload = {
            "channel" : c.channel_id,
            "user_id" : employee.slack_id,
            "oldest" : ago
        }
        headersAuth = {
            'Authorization' : 'Bearer ' + str(TOKEN), 
        }
        response = requests.get(SLACK_URL, headers=headersAuth, params=payload)
        json_data = response.json()
        msgs = json_data['messages']
        analytics_preparation(msgs,employee,c)
        time.sleep(1.2)


def analytics_preparation(msgs,employee,c):
    messages = []
    i=1
    for m in msgs:
        if m.get('user')==employee.slack_id:
            dt = float(m.get('ts'))
            object = {'id': i,'ts' : datetime.fromtimestamp(dt)}
            messages.append(object)
            i += 1
    make_post(c,employee,messages)


def make_post(c,employee,messages):
    for message in messages:
        try:
            Post.objects.create(channel=c,base=c.base,employee=employee,created_at=message["ts"])
        except:
            continue

        