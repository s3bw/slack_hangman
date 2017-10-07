import os
import time

from slackclient import SlackClient

from hangman_utils import (
    HangingMan,
    load_match_stats,
    load_data,
)

from bot_utils import (
    STATS_TEMPLATE,
    PLAYER_STATS_TEMPLATE,
    DEATH_TEMPLATE,
    GAME_STEP,
    VICTORY_TEMPLATE,
)


BOT_TOKEN = os.environ.get('API_TOKEN')
BOT_NAME = 'sweetbot'
CHANNEL_NAME = "general"

BOT_ID = os.environ.get('BOT_ID')
AT_BOT = "<@{bot_id}>".format(bot_id=BOT_ID)

EXAMPLE_COMMAND = "?"

READ_WEBSOCKET_DELAY = 1

slack_client = SlackClient(BOT_TOKEN)
slack_client.rtm_connect()


play_hangman_list = [
    'hangman',
    'play',
    'start',
]

KEY_WORDS = [
    'sweetbot',
    '?',
    AT_BOT
]


def parse_slack_output(slack_rtm_output):
    """
    The Slack Real Time Messaging API is an events fire-hose.
    this parsing function returns None unless a message is
    directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    
    if output_list and len(output_list) > 0:
        for output in output_list:
        
            # Don't reply to your own comments
            if output and 'user' in output and output['user'] == BOT_ID:
                return None, None, None
                
            if output and 'text' in output and any(keyword in output['text'] for keyword in KEY_WORDS) :
                utterance = output['text']
                user_id = output['user']
            
                # Contains command word
                if EXAMPLE_COMMAND in utterance:
                    return utterance.strip().lower(), output['channel'], user_id
                       
                # return text after the @ mention, whitespace removed
                return utterance.split(AT_BOT)[1].strip().lower(), output['channel'], user_id
                
    return None, None, None

# Make points and success rate


def handle_command(command, channel, player_guessing, bot_state, game_object=None):
    """
    Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not,
    returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *{eg_command}* command with numbers, delimited by spaces.".format(eg_command=EXAMPLE_COMMAND)
    player_name, player_id = player_guessing

    if command.startswith(EXAMPLE_COMMAND):
        command = command.split(EXAMPLE_COMMAND)[1]
        print(bot_state, command)
        
        initialise_hangman = command in play_hangman_list
        
        if bot_state == 'listening' and initialise_hangman:
            bot_state = 'playing'
            game_object = HangingMan()
            response = 'Hangman initialised!'
            
        elif bot_state == 'listening' and command == 'stats':
            response = STATS_TEMPLATE.format(load_match_stats())
            
        elif bot_state == 'listening' and command == 'me':
            response = PLAYER_STATS_TEMPLATE.format(player_data=load_data(player_id))
            
        elif bot_state == 'playing' and len(command) == 1:
            response = game_object.check_health(guess_letter=command, guessed_by=player_id)
            
            if game_object.alive == False:
                bot_state = 'listening'
                response = DEATH_TEMPLATE.format(response)
                
            if game_object.victory == True:
                bot_state = 'listening'
                response = VICTORY_TEMPLATE.format(response)
            
            else:
                response = GAME_STEP.format(response, game_object.show_progress())
            
        else:
            response = "'{}' is not recognised.".format(command)
        
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    return bot_state, game_object


if __name__ == "__main__":

    bot_state = 'listening'
    game_object = None
    
    # get user list
    api_call = slack_client.api_call("users.list")

    user_list = {} 
    for user in api_call['members']:
        user_list[user['id']] = user['profile']['real_name']
    
    while True:
        command, channel, uttering_id = parse_slack_output(slack_client.rtm_read())
        
        if command and channel:
            player_guessing = (user_list[uttering_id], uttering_id)
            bot_state, game_object = handle_command(command, channel, player_guessing, bot_state, game_object)
            
        time.sleep(READ_WEBSOCKET_DELAY)

