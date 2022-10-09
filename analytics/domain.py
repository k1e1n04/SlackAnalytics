from .models import Channel, Post
from django.conf import settings
from datetime import datetime

#任意のメンバーの24週間分の投稿を取得(Chart.js用)
def getSixWeeksPosts(dateList,employee=None,base=None):
    postList = []
    for d in range(len(dateList)-1):
        if employee is not None:
            postList.append(len(Post.objects.filter(employee=employee,created_at__gt=dateList[d],created_at__lte=dateList[d+1])))
        elif base is not None:
            postList.append(len(Post.objects.filter(base=base,created_at__gt=dateList[d],created_at__lte=dateList[d+1])))
    return postList

#任意のメンバーの24週間分の投稿を取得(GoogelChart用)
def getGoogleChartPosts(dateList,str_dateList,employee=None,base=None):
    retList = []
    for date_index in range(len(dateList)-1):
        if employee is not None:
            posts_count = len(Post.objects.filter(employee=employee,created_at__gt=dateList[date_index],created_at__lte=dateList[date_index+1]))
        elif base is not None:
            posts_count = len(Post.objects.filter(base=base,created_at__gt=dateList[date_index],created_at__lte=dateList[date_index+1]))
        else:
            posts_count = len(Post.objects.filter(created_at__gt=dateList[date_index],created_at__lte=dateList[date_index+1]))
        retList.append([str(str_dateList[date_index]),posts_count])
    return retList
    

        