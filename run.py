from slackbot.bot import Bot
from slacker import Slacker

import slackbot_settings


def main():

    # slack api token 設定
    slack = Slacker(slackbot_settings.API_TOKEN)

    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('start slackbot')
    main()
