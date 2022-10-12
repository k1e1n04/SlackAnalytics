from django.test import TestCase
from datetime import datetime
from freezegun import freeze_time
from analytics.process.gettime import get_diff_days_ago,get_diff_days_ago_unix,get_diff_month_ago,get_next_monday,six_month_dateList

# 任意日前の日付の0:00のunixtimeを返すテスト
class TestGetDiffDaysAgoUnix(TestCase):
    # 2022-09-02に時間を固定
    @freeze_time("2022-09-02")
    # 1日前をunixtimeで取得できることをテスト
    def test_get_diff_days_ago_unix_case001(self):
        result = get_diff_days_ago_unix(1)

        # 2022年9月1日0:00のunix時間
        unix_one_day_ago_sample = 1661958000.0
        self.assertEqual(result, unix_one_day_ago_sample)

    # 2022-09-01に時間を固定
    @freeze_time("2022-09-01")
    # # 月を跨いでも問題ないことをテスト
    def test_get_diff_days_ago_unix_case002(self):
        result = get_diff_days_ago_unix(1)

        # 2022年8月31日0:00のunix時間
        unix_one_day_ago_sample = 1661871600.0
        self.assertEqual(result, unix_one_day_ago_sample)

# 任意日前の日付の0:00のdatetimeを返すテスト
class TestGetDiffDaysAgo(TestCase):
    # 2022-09-02に時間を固定
    @freeze_time("2022-09-02")
    # 1日前をdatetimeで取得できることをテスト
    def test_get_diff_days_ago_case001(self):
        result = get_diff_days_ago(1)

        # 2022年9月1日0:00
        one_day_ago_sample = datetime(2022,9,1)
        self.assertEqual(result, one_day_ago_sample)

    # 2022-09-01に時間を固定
    @freeze_time("2022-09-01")
    # 月を跨いでも問題ないことをテスト
    def test_get_diff_days_ago_case002(self):
        result = get_diff_days_ago(2)

        # 2022年8月30日0:00
        one_day_ago_sample = datetime(2022,8,30)
        self.assertEqual(result, one_day_ago_sample)

# 任意ヶ月前の1日の0:00のdatetimeを返すテスト
class TestGetDiffMonthAgo(TestCase):
    # 2022-09-02に時間を固定
    @freeze_time("2022-09-02")
    # 1ヶ月前の1日を取得できるかテスト
    def test_get_diff_month_ago_case001(self):
        result = get_diff_month_ago(1)

        # 2022年8月1日0:00
        one_month_ago_sample = datetime(2022,8,1)
        self.assertEqual(result, one_month_ago_sample)

    # 2022-09-02に時間を固定
    @freeze_time("2022-09-02")
    # 年を跨いだ1日を取得できるかテスト
    def test_get_diff_month_ago_case002(self):
        result = get_diff_month_ago(9)

        # 2021年12月1日0:00
        one_month_ago_sample = datetime(2021,12,1)
        self.assertEqual(result, one_month_ago_sample)

# 次の月曜日のdatetimeを返すテスト
class TestGetDiffMonthAgo(TestCase):
    # 2022-09-02に時間を固定
    @freeze_time("2022-09-02")
    # 次の月曜日を取得できるかテスト
    def test_get_next_moday_case001(self):
        result = get_next_monday()

        # 2022年9月5日0:00(月)
        next_monday_sample = datetime(2022,9,5)
        self.assertEqual(result, next_monday_sample)

    # 2022-09-05に時間を固定
    @freeze_time("2022-09-05")
    # 当日が月曜日だった場合のテスト
    def test_get_next_moday_case002(self):
        result = get_next_monday()

        # 2022年9月12日0:00(月)
        next_monday_sample = datetime(2022,9,12)
        self.assertEqual(result, next_monday_sample)

# 過去6ヶ月間の月曜日のstringとdatetimeのListを返すテスト
class TestSixMonthDateList(TestCase):
    # 2022-09-02に時間を固定
    @freeze_time("2022-09-02")
    # 次の月曜日を取得できるかテスト
    def test_six_month_dateList_case001(self):
        next_monday = datetime(2022,9,12)
        dateList,str_dateList = six_month_dateList(next_monday)
        # 想定される6ヶ月分の月曜日のdatetimeList
        sample_dateList = [datetime(2022, 4, 4, 0, 0), datetime(2022, 4, 11, 0, 0), datetime(2022, 4, 18, 0, 0), datetime(2022, 4, 25, 0, 0), datetime(2022, 5, 2, 0, 0), datetime(2022, 5, 9, 0, 0), datetime(2022, 5, 16, 0, 0), datetime(2022, 5, 23, 0, 0), datetime(2022, 5, 30, 0, 0), datetime(2022, 6, 6, 0, 0), datetime(2022, 6, 13, 0, 0), datetime(2022, 6, 20, 0, 0), datetime(2022, 6, 27, 0, 0), datetime(2022, 7, 4, 0, 0), datetime(2022, 7, 11, 0, 0), datetime(2022, 7, 18, 0, 0), datetime(2022, 7, 25, 0, 0), datetime(2022, 8, 1, 0, 0), datetime(2022, 8, 8, 0, 0), datetime(2022, 8, 15, 0, 0), datetime(2022, 8, 22, 0, 0), datetime(2022, 8, 29, 0, 0), datetime(2022, 9, 5, 0, 0), datetime(2022, 9, 12, 0, 0)]
        # 想定される6ヶ月分の月曜日の文字列List
        sample_str_dateList = ['2022/4/4', '2022/4/11', '2022/4/18', '2022/4/25', '2022/5/2', '2022/5/9', '2022/5/16', '2022/5/23', '2022/5/30', '2022/6/6', '2022/6/13', '2022/6/20', '2022/6/27', '2022/7/4', '2022/7/11', '2022/7/18', '2022/7/25', '2022/8/1', '2022/8/8', '2022/8/15', '2022/8/22', '2022/8/29', '2022/9/5', '2022/9/12']
        # サンプルとの比較
        self.assertEqual(dateList, sample_dateList)
        self.assertEqual(str_dateList, sample_str_dateList)
        # 24週間分かチェック
        six_month = 24
        self.assertEqual(len(dateList), six_month)
        self.assertEqual(len(str_dateList), six_month)