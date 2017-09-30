import os
import random

from life_bars import LIFE
from game_stats import update_match


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def load_words():
    word_file = 'words.txt'
    word_path = os.path.join(os.path.dirname(__file__), word_file)
    word_directory = os.path.abspath(word_path)

    with open(word_directory, 'r') as words:
        word_data = words.read().split('\n')

    return word_data


WORD_CORPUS = load_words()

class HangingMan:
    def __init__(self):
        self.alive = True
        self.victory = False
        
        self.lives = 0
        self.repeated_letters = 4
        self.hints = 2
        
        self.correct_letters = []
        self.guessed_letters = []
        
        self.new_word()

    def new_word(self):
        choose = random.randint(0, len(WORD_CORPUS) - 1)
        word = 	WORD_CORPUS[choose]
        self.word = word.lower()


    def check_health(self, guess_letter):
        if self.alive == True and self.victory == False:
            return self.check_guess(guess_letter)


    def check_guess(self, guess_letter):
        guess_is_letter = guess_letter in ALPHABET
        not_repeated_guess = guess_letter not in self.guessed_letters
        
        if guess_letter and not_repeated_guess and guess_is_letter:
            
            # Correct Guess
            if guess_letter in self.word:
                self.correct_letters.append(guess_letter)
                self.guessed_letters.append(guess_letter)
                
                if set(self.correct_letters) == set(list(self.word)):
                     return self.win_match()
                
                return 'Correct Guess, keep it up!'
                
            # Incorrect Guess
            else:
                self.guessed_letters.append(guess_letter)
                response = '{} is incorrect'.format(guess_letter)
                return self.lose_life(response)
                
        elif guess_letter and guess_is_letter:
            self.repeated_letters -= 1
            
            if (self.repeated_letters) < 1:
                response = 'Already Guessed | No more repeats remaining.'
                return self.lose_life(response)
            else:
                response = 'Already Guessed | repeats remaining: {}'.format(self.repeated_letters)
                return response
        
        # Not a valid letter:
        else:
            self.repeated_letters -= 1            
            if (self.repeated_letters) < 1:
                response = 'Not a Valid Guess | No more attempts remaining'
                return self.lose_life(response)
                
            else:
                response = 'Not a Valid Guess | Attempts remaining: {}'.format(self.repeated_letters)
                return response


    def lose_life(self, response):
        self.lives += 1
        if self.lives == 1:
            self.alive = False
            self.playing = False
            self.save_info(self.alive)
            return (self.word, LIFE[self.lives])

        return '{} You have lost a life: {}'.format(response, LIFE[self.lives])
        
    def win_match(self):
        self.victory = True
        self.playing = False
        self.save_info(self.alive)        
        return 'Word: {}'.format(self.word)
        
        
    def save_info(self, game_outcome):
        update_match(game_outcome) 


    def show_progress(self):
        hidden_word = [ '_' for x in range(len(self.word))]
    
        for i, letter in enumerate(self.word):
            if letter in self.correct_letters:
                hidden_word = hidden_word[:i] + [letter] + hidden_word[i+1:]
                
            else:
                hidden_word[i] =  '_'

        response = ' '.join(hidden_word)
        print response
        return response


if __name__ == "__main__":

    game_object = HangingMan()
    while True:
        command = raw_input('take a guess:')
        print game_object.check_health(guess_letter=command)
        print game_object.show_progress()



