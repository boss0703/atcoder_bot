import datetime

from slackbot.bot import Bot
from slacker import Slacker

import scrape
import slackbot_settings


def make_message(channel, slack, contests, message):
    """
    slack.chat.post_messageを用いてメッセージを送る。

    :param channel:
    :type channel:
    :param slack:
    :type slack:
    :param contests:
    :type contests:
    :param message:
    :type message:
    :return:
    :rtype:
    """
    for contest in contests:
        message = message+"\n"+contest["time"]+"\n"+contest["name"]+"\n"+contest["url"]+"\n"

    # pos_messageでslackに投稿ができる
    # channelには投稿したいチャンネル
    # messageには投稿したいメッセージ
    # as_userはTrueにしておくことでurlが展開されて投稿される
    slack.chat.post_message(channel, message, as_user=True)


def info(channel, slack):
    """
    コンテスト情報をslackに投稿する

    :param channel:
    :param slack:
    :return:
    """

    print("-- scrape start --")
    # スクレイピングを行い、コンテスト情報を格納する
    action_contests = scrape.get_action_contest()
    upcoming_contests = scrape.get_upcoming_contest()
    print("-- scrape finish --")

    if len(action_contests) != 0:
        make_message(channel, slack, action_contests, "*[開催中のコンテスト一覧]*")
    else:
        slack.chat.post_message(channel, "*開催中のコンテストはありません*", as_user=True)

    if len(upcoming_contests) != 0:
        make_message(channel, slack, upcoming_contests, "*[再来週までのコンテスト一覧]*")
    else:
        slack.chat.post_message(channel, "*再来週までのコンテストはありません*", as_user=True)


def main():
    print('-- main --')
    # Botを動かす前にそのチャンネルにBotアプリケーションを追加することを忘れずに
    channel = "test"
    # slack api token 設定
    slack = Slacker(slackbot_settings.API_TOKEN)
    print('-- info --')
    # 月曜であることの確認 (テスト用に削除)
    if datetime.datetime.today().weekday() == 0:
        info(channel, slack)

    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('start slackbot')
    main()
