import random
import ConfigParser

import pandas as pd

from life_bars import LIFE

DIRC = "C:\Users\Sebastien\Dropbox\pythoncode\screenplay parser\cornell movie-dialogs corpus - Copy\\"
headings = ['word' , 'count' , 'normalized_score' , 'score']
WORD_CORPUS = pd.read_csv( DIRC + 'Combined_results.txt', engine='python', sep=' \+{3}\$\+{3} ',  header=None, names=headings)
            
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# config = ConfigParser.RawConfigParser()
# config.read('save_data.cfg')

# HIGHSCORE = int(config.get('Hangman Score', 'Highscore'))
# DEATHS = int(config.get('Hangman Score', 'deaths'))
# ALL_WORDS = int(config.get('Hangman Score', 'all_words'))

class HangingMan:
    def __init__(self):
        self.alive = True
        self.victory = False
        self.lives = 0
        self.repeated_letters = 4
        self.hints_remain =2
        
        self.correct_letters = []
        self.guessed_letters = []
        
        self.new_word()

    def new_word(self):
        choose = random.randint(20, len(WORD_CORPUS['word']) )          
        word = 	WORD_CORPUS.at[choose, 'word']
        self.word = word.lower()
        
    def check_health(self, guess_letter):
        if self.alive == True and self.victory == False:
            return self.check_guess(guess_letter)
        
    def check_guess(self, guess_letter):
        if guess_letter and guess_letter not in self.guessed_letters and guess_letter in ALPHABET:
            if guess_letter in self.word:
                self.correct_letters.append(guess_letter)
                self.guessed_letters.append(guess_letter)
                return 'Correct Guess, keep it up!' #Insert more sayings here
            else:
                self.guessed_letters.append(guess_letter)
                response = '{} is incorrect'.format(guess_letter)
                return self.lose_life(response)
                
        elif guess_letter and guess_letter in ALPHABET:
            self.repeated_letters -= 1
            
            if (self.repeated_letters) < 1:
                response = 'Already Guessed | No more repeats remaing.'
                return self.lose_life(response)

            else:
                response = 'Already Guessed | repeats remaing: '.format(self.repeated_letters)
                return response
        
        # Not a valid letter:
        else:
            self.repeated_letters -= 1            
            if (self.repeated_letters) < 1:
                response = 'Not a Valid Guess | No more attempts remaing'
                return self.lose_life(response)
                
            else:
                response = 'Not a Valid Guess | Attempts remaining: {}'.format(self.repeated_letters)
                return response
        
    def lose_life(self, response):
        self.lives += 1
        if self.lives == 6:
            self.alive = False
            self.playing = False
            self.save_info()
            return 'You have died... the word was {}. {}'.format(self.word, LIFE[self.lives])
        return '{} You have lost a life: {}'.format(response, LIFE[self.lives])
        
        
    def save_info(self):
        return 
        
    def show_progress(self):
        hidden_word = [ '_' for x in range(len(self.word))]
    
        for i,letter in enumerate(self.word):
            if letter in self.correct_letters:
                progress_letter = '' + letter + ''
                hidden_word = hidden_word[:i] + [progress_letter] + hidden_word[i+1:]
            else:
                hidden_word[i] =  '_'
                
        if '_' not in hidden_word:
            self.victory = True
            return 'VICTORY!'                
                
        response = ' '.join(hidden_word)
        print response
        return response
    
if __name__ == "__main__":

    game_object = HangingMan()
    while True:
        command = raw_input('take a guess:')
        print game_object.check_health(guess_letter=command)
        print game_object.show_progress()



