from apscheduler.schedulers.background import BackgroundScheduler
import analytics.process.createpost as createpost
from .models import Channel,Employee,Post
import analytics.process.gettime as gettime
import logging
logger = logging.getLogger('scheduler')

def periodic_execution():
    logger.debug("period_execution called")
    try:
        diff_day=1
        unix_one_day_ago = gettime.get_diff_days_ago_unix(diff_day)
        employees = Employee.objects.all()
        for employee in employees:
            employee_base = employee.base
            #所属拠点のチャンネルを全て取得
            channels = Channel.objects.filter(base=employee_base)
            for channel in channels:
                try:
                    slack_res = createpost.get_slack_posts(channel,unix_one_day_ago,employee)
                    messages = createpost.analytics_preparation(slack_res,employee)
                    createpost.make_post(channel,employee,messages)
                except:
                    logger.error("Tried to create posts of organization:{} channel:{}, but couldn't".format(channel.organization,channel))
                    continue
    except:
        logger.critical("Something happened! periodic_execution stopped")

def periodic_delete_execution():
    logger.debug("period_delete_execution called")
    try:
        diff_month = 7
        half_year_ago = gettime.get_diff_month_ago(diff_month)
        posts = Post.objects.filter(created_at__lt=half_year_ago)
        logger.info("{} posts were deleted".format(len(posts)))
        posts.delete()
    except:
        logger.critical("Something happened! periodic_delete_execution stopped")
        
        

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_execution,'interval',minutes=30)
    try:
        scheduler.start()
    except:
        logger.critical("could not start periodic_execution")

def start_delete():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_delete_execution,'interval',weeks=1)
    try:
        scheduler.start()
    except:
        logger.critical("could not start periodic_delete_execution")