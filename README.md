# Project IMH Angel and Mortals Bot

Send anonymous messages between people! 

## Read on Medium

https://chatbotslife.com/building-a-chatbot-for-angel-mortal-5d389ab7acde

## User data

PLAYERS_FILENAME file is used to store usernames of players and assign pairings.

After cloning project from Github, remember to create a .csv file with the same file name used in config.py under PLAYERS_FILENAME

Order of columns is player and angel with one header row.

Sample of csv file formatting:
```
Player,Angel
username1,username2
username2,username1
```

## Environment variables
_(this is outdated)_

```
ANGEL_BOT_TOKEN = os.environ['ANGEL_BOT_TOKEN']

PLAYERS_FILENAME = os.environ['PLAYERS_FILENAME']

CHAT_ID_JSON = os.environ['CHAT_ID_JSON']

ANGEL_ALIAS = os.environ['ANGEL_ALIAS']

MORTAL_ALIAS = os.environ['MORTAL_ALIAS']
```

## Useful references
https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.sendAnimation
https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message