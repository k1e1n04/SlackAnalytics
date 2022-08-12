from datetime import datetime,date,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import analytics.domain
import time
from .models import Base,Department,Channel,Employee,Post
from dateutil.relativedelta import relativedelta
now = datetime.now()

def periodic_first_execution():
    print("スタート")
    employees = Employee.objects.all()
    employees.reverse()
    if len(employees) > 10:
        new_employees = employees[0:11]
    for e in new_employees:
        total_posts = Post.objects.filter(employee=e)
        if len(total_posts):
            employee_base = e.base
            channels = Channel.objects.filter(base=employee_base)
            unix_three_month_ago = analytics.process.get_time.get_diff_month_ago_unix(3)
            analytics.domain.get_slack_posts(channels,unix_three_month_ago,e)
            unix_two_month_ago = analytics.process.get_time.get_diff_month_ago_unix(2)
            analytics.domain.get_slack_posts(channels,unix_two_month_ago,e)
            unix_one_month_ago = analytics.process.get_time.get_diff_month_ago_unix(1)
            analytics.domain.get_slack_posts(channels,unix_one_month_ago,e)

def periodic_execution():
    one_day_ago = now + timedelta(days=-1)
    one_day_ago = datetime(one_day_ago.year,one_day_ago.month,one_day_ago.day)
    unix_one_day_ago = time.mktime(one_day_ago.timetuple())
    employees = Employee.objects.all()
    for e in employees:
        employee_base = e.base
        #所属拠点のチャンネルを全て取得
        channels = Channel.objects.filter(base=employee_base)
        analytics.domain.get_slack_posts(channels,unix_one_day_ago,e)

def periodic_delete_execution():
    half_year_ago = now + relativedelta(months=-7)
    half_year_ago =datetime(half_year_ago.year,half_year_ago.month,1)
    posts = Post.objects.filter(created_at__lt=half_year_ago)
    posts.delete()


def start_first():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_first_execution,'interval',minutes=1)
    scheduler.start()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution,'interval',hours=1)
    scheduler.start()

def start_delete():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_delete_execution,'interval',weeks=1)
    scheduler.start()