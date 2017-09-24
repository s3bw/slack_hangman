import os
import ConfigParser

abs_save_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'save_data.cfg'))
saved_data = ConfigParser.RawConfigParser()
saved_data.read(abs_save_path)

def load_data(field):
    return int(saved_data.get('HANGMAN_SCORE', field))
    
def set_data(field, value):
    saved_data.set('HANGMAN_SCORE', field, str(value))
    
def save_data():
    with open(abs_save_path, 'wb') as configfile:
        saved_data.write(configfile)

def load_match_stats():
    return(
        load_data('highscore'),
        load_data('deaths'),
        load_data('all_words'),
        load_data('current_streak'),
    )

def update_match(good_result):
    highscore, deaths, all_words, current_streak = load_match_stats()
    
    all_words += 1
    if good_result:
        current_streak += 1
        
        if current_streak > highscore:
            highscore = current_streak
            
    else:
        deaths += 1
        current_streak = 0
        
    set_data('highscore', highscore)
    set_data('deaths', deaths)
    set_data('all_words', all_words)
    set_data('current_streak', current_streak)
    save_data()




