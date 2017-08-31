import ConfigParser
from slackclient import SlackClient

Config = ConfigParser.ConfigParser()
Config.read('config.cfg')
BOT_TOKEN = Config.get('BOT_TOKEN', 'API_TOKEN')

slack_client = SlackClient(BOT_TOKEN)

BOT_NAME = 'sweetbot'


slack_client.rtm_connect()
saying = raw_input('')

saying ="""

Heyyy
Yoou!
"""
slack_client.rtm_send_message("general", saying)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)