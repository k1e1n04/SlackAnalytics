from datetime import datetime,date,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import analytics.domain
import time
from .models import Base,Department,Channel,Employee,Post
from dateutil.relativedelta import relativedelta
now = datetime.now()

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

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution,'cron',hour=1)
    scheduler.start()

def start_delete():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_delete_execution,'cron',day=1)
    scheduler.start()