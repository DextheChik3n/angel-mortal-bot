import config

MESSAGE_SENT = 'Message sent!\n(/start to send another!)'
HELP_TEXT = (
    f'Use /start to send a message to your {config.ANGEL_ALIAS} or {config.MORTAL_ALIAS} and /cancel to cancel message.'
    f'\n\n'
    f'This bot supports forwarding only text, photos, stickers, documents, audio, video, and animations.'
)
ERROR_CHAT_ID = 'Sorry an error occured please type /start again'
SEND_COMMAND = 'Send a message to my:\n(/cancel to stop)'
NOT_REGISTERED = 'Sorry you are not registered with the game currently'
FILL_UP_QUESTIONS = 'Fill up the following questions:'
PROMPT_ANSWER = '\n\nPlease type your answer...'
REGISTRATION_SUCCESS = 'Registration success! please enter /start again to begin talking to your angel!'
CANCEL_COMMAND = 'Operation cancelled.'

def getBotNotStartedMessage(alias):
    return f'Sorry your {alias} has not started this bot'

def getPlayerMessage(alias):
    return f'Please type your message to your {alias}\n(/cancel to stop)'

def getReceivedMessage(alias, text=""):
    return f"Message from your {alias}:\n\n{text}" if text != "" else f"Message from your {alias}:"

def getSentMessageLog(alias, sender, receiver):
    return f'{sender} sent a message to their {alias} {receiver}'

def getNotRegisteredLog(alias, sender, receiver):
    return f'{sender} {alias} {receiver} has not started the bot'

def getInfoQuestion(num):
    match num:
        case 1:
            return '\n\n1. What is your fav colour?\n'
        case 2:
            return '\n\n2. What is your fav food?\n'
        case 3:
            return '\n\n3. What is your fav animal?\n'