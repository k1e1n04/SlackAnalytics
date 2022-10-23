from datetime import datetime,timedelta
import time
from dateutil.relativedelta import relativedelta
import logging
logger = logging.getLogger('datetime')

def get_diff_days_ago_unix(diff_day):
    """ 任意日前の日付の0:00のUNIX時間を返す\n
    :param diff_day: 遡りたい日付の数字
    :type diff_day: int
    :return unix_diff_days_ago: 任意日前の日付の0:00のUNIX時間
    :type unix_diff_days_ago: float
    """
    logger.debug("get_diff_days_ago_unix called")
    now = datetime.now()
    diff_days_ago = now + timedelta(days= - diff_day)
    diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
    unix_diff_days_ago = time.mktime(diff_days_ago.timetuple())
    logger.debug("get_diff_days_ago_unix return {}".format(unix_diff_days_ago))
    return unix_diff_days_ago

def get_diff_days_ago(diff_day):
    """ 任意日前の日付の0:00のdatetimeを返す\n
    :param diff_day: 遡りたい日付の数字
    :type diff_day: int
    :return diff_days_ago: 任意日前の日付の0:00のdatetime
    :type diff_days_ago: datetime
    """
    logger.debug("get_diff_days_ago called")
    now = datetime.now()
    diff_days_ago = now + timedelta(days= - diff_day)
    diff_days_ago = datetime(diff_days_ago.year,diff_days_ago.month,diff_days_ago.day)
    logger.debug("get_diff_days_ago return {}".format(diff_days_ago))
    return diff_days_ago

def get_diff_month_ago(diff_month):
    """ 任意ヶ月前の1日の0:00のdatetimeを返す\n
    :param diff_month: 遡りたい日付の数字
    :type diff_month: int
    :return diff_month_ago: 任意ヶ月前の1日の0:00のdatetime
    :type diff_month_ago: datetime
    """
    logger.debug("get_diff_month_ago called")
    now = datetime.now()
    diff_month_ago = now + relativedelta(months=- diff_month)
    diff_month_ago = datetime(diff_month_ago.year,diff_month_ago.month,1)
    logger.debug("get_diff_month_ago_unix return {}".format(diff_month_ago))
    return diff_month_ago

def get_next_monday():
    """ 翌月曜日の日付の0:00のdatetimeを返す\n
    :return next_monday: 任意日前の日付の0:00のUNIX時間
    :type next_monday: datetime
    """
    logger.debug("get_next_monday called")
    now = datetime.now()
    dayofWeek = now.weekday()
    addDay = 7 - dayofWeek
    next_monday = now + timedelta(days= + addDay)
    next_monday = datetime(next_monday.year,next_monday.month,next_monday.day)
    logger.debug("get_next_monday return {}".format(next_monday))
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
    logger.debug("six_month_dateList called")
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
    logger.debug("six_month_dateList return {}".format(dateList))
    logger.debug("six_month_dateList return {}".format(str_dateList))
    return dateList,str_dateList
