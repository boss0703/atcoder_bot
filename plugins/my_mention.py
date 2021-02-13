from slackbot.bot import respond_to, listen_to
from slacker import Slacker
import slackbot_settings
from run import info


@respond_to('コンテスト')
def respond_contest_func(message):
    channel = "test"
    # slack api token 設定
    slack = Slacker(slackbot_settings.API_TOKEN)
    info(channel, slack)


@listen_to('コンテスト')
def listen_contest_func(message):
    channel = "test"
    # slack api token 設定
    slack = Slacker(slackbot_settings.API_TOKEN)
    info(channel, slack)