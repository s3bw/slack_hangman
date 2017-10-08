import os
import configparser

abs_save_path = os.path.abspath(
    os.path.join(
        os.path.dirname( __file__ ),
        '..',
        'save_data.cfg'
    )
)

saved_data = configparser.RawConfigParser()
saved_data.read(abs_save_path)


game_stats = [
    'highscore',
    'deaths',
    'all_words',
    'current_streak',
]


player_stats = [
    'highscore',
    'incorrect',
    'total_guesses',
    'current_streak',
    'accuracy',
]


def load_data(section_id):
    load_fields = game_stats if section_id == 'HANGMAN_SCORE' else player_stats
    print(load_fields)
    try:
        return {field: float(saved_data.get(section_id, field)) for field in load_fields}

    except configparser.NoSectionError:
        saved_data.add_section(section_id)
        data_dict = {field: 0 for field in load_fields}
        print(data_dict)
        set_data(section_id, data_dict)

        return data_dict


def set_data(section_id, data_dict):
    load_fields = game_stats if section_id == 'HANGMAN_SCORE' else player_stats

    for field in load_fields:
        saved_data.set(section_id, field, str(data_dict[field]))


def save_data():
    with open(abs_save_path, 'w') as configfile:
        saved_data.write(configfile)


def update_match(good_result):
    game_dict = load_data('HANGMAN_SCORE')

    game_dict['all_words'] += 1
    if good_result:
        game_dict['current_streak'] += 1
        
        new_highscore = game_dict['current_streak'] > game_dict['highscore']
        if new_highscore:
            game_dict['highscore'] = game_dict['current_streak']
            
    else:
        game_dict['deaths'] += 1
        game_dict['current_streak'] = 0
    
    set_data('HANGMAN_SCORE', game_dict)
    save_data()


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
        
    set_data(player_id, player_dict)
    save_data()

