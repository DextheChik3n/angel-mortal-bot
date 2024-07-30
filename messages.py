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
BOT_NOT_STARTED = f'Sorry your {config.ANGEL_ALIAS} has not started this bot'
REQUEST_PLAYER_MESSAGE = f'Please type your message to your {config.ANGEL_ALIAS}\n(/cancel to stop)'
RECEIVE_PHOTO = f'Your {config.ANGEL_ALIAS} sent you a photo:'
RECEIVE_STICKER = f'Your {config.ANGEL_ALIAS} sent you a sticker:'
RECEIVE_DOCUMENT = f'Your {config.ANGEL_ALIAS} sent you a file:'
RECEIVE_VIDEO = f'Your {config.ANGEL_ALIAS} sent you a video:'
RECEIVE_TELEBUBBLE = f'Your {config.ANGEL_ALIAS} sent you a telebubble:'
RECEIVE_VOICE = f'Your {config.ANGEL_ALIAS} sent you a voice recording:'
RECEIVE_AUDIO = f'Your {config.ANGEL_ALIAS} sent you an audio file:'
RECEIVE_GIF = f'Your {config.ANGEL_ALIAS} sent you a gif:'

def receivedMessage(text=""): 
    return f"Message from your {config.ANGEL_ALIAS}:\n\n{text}" if text != "" else f"Message from your {config.ANGEL_ALIAS}:"

def sentMessageLog(sender, receiver):
    return f'{sender} sent a message to their {config.ANGEL_ALIAS} {receiver}'

def notRegisteredLog(sender, receiver):
    return f'{sender} {config.ANGEL_ALIAS} {receiver} has not started the bot'

def getInfoQuestion(num):
    match num:
        case 1:
            return '\n\n1. What is your fav colour?\n'
        case 2:
            return '\n\n2. What is your fav food?\n'
        case 3:
            return '\n\n3. What is your fav animal?\n'