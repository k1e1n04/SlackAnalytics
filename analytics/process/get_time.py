from datetime import datetime,timedelta
import time
from dateutil.relativedelta import relativedelta

now = datetime.now()

def get_diff_days_ago_unix(diff_day):
    diff_days_ago = now + timedelta(days= - diff_day)
    diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
    unix_diff_days_ago = time.mktime(diff_days_ago.timetuple())
    return unix_diff_days_ago

def get_diff_days_ago(diff_day):
    diff_days_ago = now + timedelta(days= - diff_day)
    diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
    return diff_days_ago

def get_diff_month_ago_unix(diff_month):
    diff_month_ago = now + relativedelta(months=- diff_month)
    diff_month_ago = datetime(diff_month_ago.year,diff_month_ago.month,1)
    unix_diff_month_ago = time.mktime(diff_month_ago.timetuple())
    return unix_diff_month_ago