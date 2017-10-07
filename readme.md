# Hangman Bot for Slack.

This bot allows games of hangman in slack channels.

## Deploying to Heroku:

After installing heroku

```bash
heroku login
git clone git@github.com:GiantsLoveDeathMetal/slack_hangman.git
cd slack_hangman
heroku create
git push heroku master
```

Setup config vars on heroku from slack api:
`API_TOKEN`
`BOT_ID`

# Using hangman bot:

The bot picks up the key word `"?"`

```bash
Play hangman: ?hangman
Check your stats: ?me
Check all stats: ?stats
See highscores: ?leaders
```
Guessing a letter `(e.g. '?t', '?p')`
