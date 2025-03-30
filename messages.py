import config

MESSAGE_SENT = 'Message sent!\n(/start to send another!)'
HELP_TEXT = (
    f'Use /start to send a message to your {config.ANGEL_ALIAS} or {config.MORTAL_ALIAS} and /cancel to cancel message.'
    f'\n\n'
    f'This bot supports forwarding only text, photos, stickers, documents, audio, video, and animations.'
)
ERROR_CHAT_ID = 'Sorry an error occured please type /start again'
SEND_COMMAND = 'Send a message to my:\n(/cancel to stop)'
NOT_REGISTERED = 'Sorry you are not registered with the game currently, please contact Dexter @chik3n about it'
FILL_UP_QUESTIONS = 'Fill up the following questions:'
PROMPT_ANSWER = 'Please enter your answer for:'
REGISTRATION_SUCCESS = 'Registration success! please enter /start again to begin talking to your angel!'
CANCEL_COMMAND = 'Operation cancelled.'
BOT_NOT_STARTED = f'Sorry your {config.ANGEL_ALIAS} has not started this bot, please contact Dexter @chik3n about it' # message to ask user to wait or contact welfare team and then click on /start again
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
            return '\n\n1. What’s a simple thing/things in your life that brings you a lot of joy?\n'
        case 2:
            return '\n\n2. What’s a hobby or activity you’ve always wanted to try?\n'
        case 3:
            return '\n\n3. If you had unlimited budget for one trip, where would you go?\n'


def getAngelInformation(angelInfo):
    return f'Here are some information about your {config.ANGEL_ALIAS}:' + \
        getInfoQuestion(1) + angelInfo[1] + \
        getInfoQuestion(2) + angelInfo[2] + \
        getInfoQuestion(3) + angelInfo[3] + \
        '\n\n\n(/start to send a message!)'
