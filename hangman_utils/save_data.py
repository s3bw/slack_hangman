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


def load_game_data(section):
    try:
        return {field: float(saved_data.get(section, field)) for field in game_stats}

    except configparser.NoSectionError:
        saved_data.add_section(section)
        game_dict = {field: 0 for field in list_of_fields}
        set_dict_data(section, game_dict)

        return game_dict


    return int(saved_data.get('HANGMAN_SCORE', field))


def set_data(section, game_dict):

    for field in game_stats:
        saved_data.set(section, field, str(game_dict[field]))


def save_data():
    with open(abs_save_path, 'w') as configfile:
        saved_data.write(configfile)


def update_match(good_result):
    game_dict = load_game_data('HANGMAN_SCORE')

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

