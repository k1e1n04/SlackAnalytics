from .models import Channel, Post
from django.conf import settings
from datetime import datetime

#各部署のチャンネルへの投稿数の配列を返す
def return_departments_posts_count(departments,employee,month):
    departments_posts_count = []
    for department in departments:
        channels = Channel.objects.filter(department=department)
        department_posts = Post.objects.filter(employee=employee,channel__in=channels,created_at__gt=month)
        department_posts_count = len(department_posts)
        departments_posts_count.append(department_posts_count)
    return departments_posts_count

#任意のメンバーの24週間分の投稿を取得
def getSixWeeksPosts(dateList,employee):
    postList = []
    for d in range(len(dateList)-1):
        postList.append(len(Post.objects.filter(employee=employee,created_at__gt=dateList[d],created_at__lte=dateList[d+1])))
    return postList


#2期間の投稿数の比較
def return_compare_posts_conut(one_week_posts,two_week_posts):
    one_week_posts_count = len(one_week_posts)
    two_week_posts_count = len(two_week_posts)
    compare_posts_count = one_week_posts_count-two_week_posts_count
    return one_week_posts_count,compare_posts_count,two_week_posts_count
        