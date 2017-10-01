import os
import configparser

abs_save_path = os.path.abspath(
    os.path.join(
        os.path.dirname( __file__ ),
        '..',
        'player_data.cfg'
    )
)

player_data = configparser.RawConfigParser()
player_data.read(abs_save_path)

list_of_fields = [
    'highscore',
    'incorrect',
    'total_guesses',
    'current_streak',
    'accuracy',
]


def load_data(player_id):
    try:
        return {field: float(player_data.get(player_id, field)) for field in list_of_fields}
        
    except configparser.NoSectionError:
        player_data.add_section(player_id)
        player_dict = {field: 0 for field in list_of_fields}
        set_dict_data(player_id, player_dict)
        
        return player_dict


def set_dict_data(player_id, player_dict):
    print(player_dict)
    for field in list_of_fields:
        player_data.set(player_id, field, str(player_dict[field]))


def save_data():
    with open(abs_save_path, 'w') as configfile:
        player_data.write(configfile)


def update_player(player_id, correct_guess):
    player_dict = load_data(player_id)
    
    player_dict['total_guesses'] += 1
    if correct_guess:
        player_dict['current_streak'] += 1
        
        new_highscore = player_dict['current_streak'] > player_dict['highscore']
        if new_highscore:
            player_dict['highscore'] = player_dict['current_streak']
            
    else:
        player_dict['incorrect'] += 1
        player_dict['current_streak'] = 0
        
    correct_guesses = player_dict['total_guesses'] - player_dict['incorrect']
    player_dict['accuracy'] = correct_guesses / player_dict['total_guesses']
        
    set_dict_data(player_id, player_dict)
    save_data()




