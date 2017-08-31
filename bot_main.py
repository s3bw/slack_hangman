import time
import ConfigParser

from slackclient import SlackClient
import hangman_utils.hangman as hm

Config = ConfigParser.ConfigParser()
Config.read('config.cfg')

BOT_TOKEN = Config.get('BOT_TOKEN', 'API_TOKEN')
BOT_NAME = 'sweetbot'
CHANNEL_NAME = "general"

BOT_ID = Config.get('BOT_TOKEN', 'BOT_ID')
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "fly"

READ_WEBSOCKET_DELAY = 1

slack_client = SlackClient(BOT_TOKEN)
slack_client.rtm_connect()

KEY_WORDS = [
    'sweetbot',
    'fly',
    AT_BOT
]


def parse_slack_output(slack_rtm_output):
    """
    The Slack Real Time Messaging API is an events firehose.
    this parsing function returns None unless a message is
    directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    
    if output_list and len(output_list) > 0:
        for output in output_list:
        
            # Dont reply to your own comments
            if output and 'user' in output and output['user'] == BOT_ID:
                return None, None, None
                
            if output and 'text' in output and any(keyword in output['text'] for keyword in KEY_WORDS) :
                utterance = output['text']
                user_id = output['user']
            
                # Contains command word
                if 'fly' in utterance:
                    return utterance.strip().lower(), output['channel'], user_id
                       
                # return text after the @ mention, whitespace removed
                return utterance.split(AT_BOT)[1].strip().lower(), output['channel'], user_id
                
    return None, None, None

# Make points and success rate

def give_guess():
    global guesses,hints_remain

    check = raw_input('\nLetter?  ').upper()
    
    if check == word:
        for letter in check:
            check_guess(letter)


def handle_command(command, channel, name_of_mention, bot_state, game_object=None):
    """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."

    if command.startswith(EXAMPLE_COMMAND):
        command = command.split(EXAMPLE_COMMAND)[1]
        print bot_state, command
        if bot_state == 'listening' and command == 'hangman':
            bot_state = 'playing'
            game_object = hm.HangingMan()
            response = 'Hangman initialised!'
            
        elif bot_state == 'playing' and len(command) == 1:
            response = game_object.check_health(guess_letter=command)
            response = '\n\n{} Hidden word: `{}`'.format(response, game_object.show_progress())
            
        else:
            response = "{}? Thats not recognised.".format(command)
        
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    return bot_state, game_object


if __name__ == "__main__":

    bot_state = 'listening'
    game_object = None
    
    # get user list
    api_call = slack_client.api_call("users.list")
    user_list = {} 
    for user in api_call['members']:
        user_list[user['id']] = user['profile']['first_name']
    
    while True:
        command, channel, uttering_id = parse_slack_output(slack_client.rtm_read())
        
        if command and channel:
            bot_state, game_object = handle_command(command, channel, user_list[uttering_id], bot_state, game_object)
            
        time.sleep(READ_WEBSOCKET_DELAY)

