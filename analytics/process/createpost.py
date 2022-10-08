from analytics.models import Post
from django.conf import settings
from datetime import datetime
import requests
import time

def get_slack_posts(channel,ago,employee):
    """ SlackAPIを叩いてmessagesのみを返す\n
    チャンネル、oldest、メンバーを引数として受け取り、
    リクエストボディにて絞り込みのパラメーターを渡す`\n
    リクエストヘッダーには環境変数で定義したSlackBotのトークンを与える\n
    返ってきたJSON形式のSlackの投稿は"messages"のみを抽出し返す\n
    :param channel: Channelインスタンス
    :param ago: 任意のUNIX時間
    :param employee: Employeeインスタンス
    :return msgs: 投稿取得SlackAPIのレスポンスの"messages"のみを抽出したもの
    :type msgs: list of JSON
    """
    SLACK_URL = settings.SLACK_URL
    TOKEN = settings.TOKEN
    payload = {
        "channel" : channel.channel_id,
        "user_id" : employee.slack_id,
        "oldest" : ago
    }
    headersAuth = {
        'Authorization' : 'Bearer ' + str(TOKEN), 
    }
    response = requests.get(SLACK_URL, headers=headersAuth, params=payload)
    json_data = response.json()
    msgs = json_data['messages']
    time.sleep(1)
    return msgs


def analytics_preparation(msgs,employee):
    """ SlackメッセージをPostに保存するための準備\n
    SlackAPIの戻り値からmessagesのみを抽出したリストを引数として受け取り、
    1つ1つのmessageに対してユーザーのチェックとタイムスタンプのdatetime型への変換を行う\n
    変換が行われたmessagのidとタイムスタンプのdictをリストに格納し返す\n
    :param msgs: 投稿取得SlackAPIのレスポンスの"messages"のみを抽出したもの
    :type msgs: list of JSON
    :param employee: Employeeインスタンス
    :return messages: それぞれのmessageのid(新たに作成)とdatetimeのdictが格納されたリスト
    :type messages: list of dicts
    """
    messages = []
    i=1
    for m in msgs:
        if m.get('user')==employee.slack_id:
            dt = float(m.get('ts'))
            object = {'id': i,'ts' : datetime.fromtimestamp(dt)}
            messages.append(object)
            i += 1
    return messages


def make_post(channel,employee,messages):
    """ Postの作成\n
    Slackの投稿の、id(自分で作成したもの)とdatetimeが格納されたdictのリストからPostを作成する\n
    投稿の作成にはパラメータとして受け取ったchannel,base,employeeとdict内のdatetimeを用いる\n
    既にchannelとcreated_atが重複した投稿が作成された場合は例外を発生させ処理を続ける\n
    :param messages: それぞれのmessageのid(新たに作成)とdatetimeのdictが格納されたリスト
    :type messages: list of dicts
    :param employee: Employeeインスタンス
    :param channel: Channelインスタンス
    """
    for message in messages:
        try:
            Post.objects.create(channel=channel,base=channel.base,employee=employee,created_at=message["ts"])
        except:
            continue