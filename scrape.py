import datetime
import re
import requests
from bs4 import BeautifulSoup


def get_action_contest():
    """
    現在開催中のコンテストを取得する。

    :return: re_contests
    :rtype: list
    """
    re_contests = []
    # コンテスト一覧ページの情報を取得 日本語で欲しいのでlang=ja追加
    url = "https://atcoder.jp"
    res = requests.get(url + "/contests/?lang=ja").text
    # htmlのパース処理
    soup = BeautifulSoup(res, "html.parser")
    # div#contest-table-actionに開催中のコンテスト情報が格納されている
    contests_div = soup.find("div", id="contest-table-action")
    # 開催中のコンテストが無い場合
    if contests_div is None:
        return re_contests

    contests_tr = contests_div.tbody.find_all("tr")
    # trタグの内容(コンテスト名, URL, 終了日時)を格納
    for tr in contests_tr:
        # "contests"の文字列を含むaタグを取得
        contest_a = tr.find("a", href=re.compile("contests"))
        # aタグの中の文字(コンテスト名)を取得
        contest_name = contest_a.text
        # URL + aタグのurl情報(コンテストページのurl)
        contest_url = url + contest_a.get("href")

        # コンテストページの取得
        res = requests.get(contest_url).text
        # コンテストページ遷移
        soup = BeautifulSoup(res,  "html.parser")
        # "fixtime-full"クラス属性を持つtimeタグを取得 ※classは予約語なのでclass_
        contest_fin_time = soup.find("time", class_="fixtime-full") + " 終了"

        # 返却用の変数に値を格納
        re_contest = dict(name=contest_name, url=contest_url, time=contest_fin_time)
        re_contests.append(re_contest)

    return re_contests


def get_upcoming_contest():
    """
    2週間以内に開催されるコンテストを取得する。

    :return: re_contests
    :rtype: list
    """
    re_contests = []
    # コンテスト一覧ページの情報を取得
    url = "https://atcoder.jp"
    res = requests.get(url + "/contests/?lang=ja").text
    # htmlのパース処理
    soup = BeautifulSoup(res, "html.parser")
    # div#contest-table-upcomingに開催予定のコンテスト情報が格納されている
    contests_div = soup.find("div", id="contest-table-upcoming")
    # 開催予定のコンテストが無い場合
    if contests_div is None:
        return re_contests

    contests_tr = contests_div.tbody.find_all("tr")
    # 今日の日時を取得(月曜日)
    today = datetime.datetime.today()

    # trタグの内容(コンテスト名, URL, 開始日時)を格納
    for tr in contests_tr:
        # 今週開催されるもの以外は無視
        contest_date = str_to_date(tr.find("time").text[:16])
        if (contest_date - today).days >= 14:
            break

        # "contests"の文字列を含むaタグを取得
        contest_a = tr.find("a", href=re.compile("contests"))
        # aタグの中の文字(コンテスト名)を取得
        contest_name = contest_a.text
        # URL + aタグのurl情報(コンテストページのurl)
        contest_url = url + contest_a.get("href")
        # contest_dateに" 開始"を追加
        contest_date = date_to_str(contest_date) + " 開始"

        # 返却用の変数に値を格納
        re_contest = dict(name=contest_name, url=contest_url, time=contest_date)
        re_contests.append(re_contest)

    return re_contests


def str_to_date(str_date: str) -> datetime.datetime:
    """
    datetimeオブジェクトにして返す

    :param str_date:
    :type str_date:
    :return: date
    :rtype: datetime
    """

    date = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M')
    return date


def date_to_str(date):
    """
    datetimeオブジェクトをstrオブジェクトにして返す

    :param date:
    :type date:
    :return: str_date
    :rtype: str
    """

    day_of_the_week = ("月", "火", "水", "木", "金", "土", "日")
    str_date = (
        '{:d}-{:d}-{:d}({}) {:d}:{}'.format(
            date.year, date.month, date.day, day_of_the_week[date.weekday()], date.hour, str(date.minute).ljust(2, "0")
        )
    )
    return str_date
