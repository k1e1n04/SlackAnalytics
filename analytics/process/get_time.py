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

def get_diff_month_ago(diff_month):
    diff_month_ago = now + relativedelta(months=- diff_month)
    diff_month_ago = datetime(diff_month_ago.year,diff_month_ago.month,diff_month_ago.month)
    return diff_month_ago

def get_next_monday():
    dayofWeek = now.weekday()
    addDay = 7 - dayofWeek
    next_monday = now + timedelta(days= + addDay)
    next_monday = datetime(next_monday.year,next_monday.month,next_monday.day)
    return next_monday

def six_month_dateList(next_monday):
    dateList=[]
    for i in range(24):
        diff_days_ago = next_monday  + timedelta(days= - i*7)
        diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
        dateList.append(diff_days_ago)
    dateList.reverse()
    return dateList
