
STATS_TEMPLATE = """`Game Play Stats:`
High Score: `{game_data[highscore]}`
Deaths: `{game_data[deaths]}`
Words Seen: `{game_data[all_words]}`
Current Streak: `{game_data[current_streak]}`
"""

PLAYER_STATS_TEMPLATE = """`Your Stats:`
High Score: `{player_data[highscore]}`
Incorrect: `{player_data[incorrect]}`
Total Guesses: `{player_data[total_guesses]}`
Current Streak: `{player_data[current_streak]}`
Accuracy: `{player_data[accuracy]:.0%}`
"""

DEATH_TEMPLATE = """You have died... the word was *{0[0]}*. {0[1]}
How would you like to continue?
Display Stats: `?stats`
Leaderboard: `?leaders`
Your stats: `?me`
Play Again: `?hangman`
"""

VICTORY_TEMPLATE = """You Win Great Work!
{}
How would you like to continue?
Display Stats: `?stats`
Leaderboard: `?leaders`
Your stats: `?me`
Play Again: `?hangman`
"""

GAME_STEP = '{} Hidden word: `{}`'
