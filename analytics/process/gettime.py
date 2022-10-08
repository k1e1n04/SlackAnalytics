from datetime import datetime,timedelta
import time
from dateutil.relativedelta import relativedelta

def get_diff_days_ago_unix(diff_day):
    """ 任意日前の日付の0:00のUNIX時間を返す\n
    :param diff_day: 遡りたい日付の数字
    :type diff_day: int
    :return unix_diff_days_ago: 任意日前の日付の0:00のUNIX時間
    :type unix_diff_days_ago: float
    """
    now = datetime.now()
    diff_days_ago = now + timedelta(days= - diff_day)
    diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
    unix_diff_days_ago = time.mktime(diff_days_ago.timetuple())
    return unix_diff_days_ago

def get_diff_days_ago(diff_day):
    """ 任意日前の日付の0:00のdatetimeを返す\n
    :param diff_day: 遡りたい日付の数字
    :type diff_day: int
    :return diff_days_ago: 任意日前の日付の0:00のdatetime
    :type diff_days_ago: datetime
    """
    now = datetime.now()
    diff_days_ago = now + timedelta(days= - diff_day)
    diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
    return diff_days_ago

def get_diff_month_ago(diff_month):
    """ 任意ヶ月前の1日の0:00のdatetimeを返す\n
    :param diff_month: 遡りたい日付の数字
    :type diff_month: int
    :return diff_month_ago: 任意ヶ月前の1日の0:00のdatetime
    :type diff_month_ago: datetime
    """
    now = datetime.now()
    diff_month_ago = now + relativedelta(months=- diff_month)
    diff_month_ago = datetime(diff_month_ago.year,diff_month_ago.month,1)
    return diff_month_ago

def get_next_monday():
    """ 翌月曜日の日付の0:00のdatetimeを返す\n
    :return next_monday: 任意日前の日付の0:00のUNIX時間
    :type next_monday: datetime
    """
    now = datetime.now()
    dayofWeek = now.weekday()
    addDay = 7 - dayofWeek
    next_monday = now + timedelta(days= + addDay)
    next_monday = datetime(next_monday.year,next_monday.month,next_monday.day)
    return next_monday

def six_month_dateList(next_monday):
    """ 過去6ヶ月間の月曜日のstringとdatetimeのListを返す\n
    :param next_monday: 任意日前の日付の0:00のUNIX時間
    :type next_monday: datetime
    :return dateList: 過去6ヶ月間の月曜日の日付リスト(datetime)
    :type dateList: list of datetime
    :return str_dateList: 過去6ヶ月間の月曜日の日付リスト(string)
    :type str_dateList: list of string
    """
    dateList=[]
    str_dateList=[]
    six_month_as_week = 24
    for week in range(six_month_as_week):
        diff_days_ago = next_monday  + timedelta(days= - week*7)
        diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
        str_diff_days_ago = "{}/{}/{}".format(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
        dateList.append(diff_days_ago)
        str_dateList.append(str_diff_days_ago)
    dateList.reverse()
    str_dateList.reverse()
    return dateList,str_dateList
