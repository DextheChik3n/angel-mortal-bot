import logging
import player
import messages
import datetime
import collections

import config, os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler

CHOOSING, ANGEL, MORTAL = range(3)


# Enable logging
logging.basicConfig(
    filename=f'logs/{datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

players = collections.defaultdict(player.Player)
player.loadPlayers(players)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    playerName = update.message.chat.username.lower()
    if players[playerName].username is None:
        await update.message.reply_text(messages.NOT_REGISTERED)
        return

    players[playerName].chat_id = update.message.chat.id

    logger.info(f'{playerName} started the bot with chat_id {players[playerName].chat_id}')

    await update.message.reply_text(f'Hi! {messages.HELP_TEXT}')

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(messages.HELP_TEXT)

async def reload_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /reloadplayers is issued."""
    player.saveChatID(players)
    logger.info(f'Player chat ids have been saved in {config.CHAT_ID_JSON}')

    player.loadPlayers(players)
    logger.info(f'Players reloaded')

    await update.message.reply_text(f'Players reloaded')

async def send_command(update: Update, context: CallbackContext):
    """Start send convo when the command /send is issued."""
    playerName = update.message.chat.username.lower()

    if players[playerName].username is None:
        await update.message.reply_text(messages.NOT_REGISTERED)
        return ConversationHandler.END

    if players[playerName].chat_id is None:
        await update.message.reply_text(messages.ERROR_CHAT_ID)
        return ConversationHandler.END

    send_menu = [[InlineKeyboardButton(config.ANGEL_ALIAS, callback_data='angel')],
                 [InlineKeyboardButton(config.MORTAL_ALIAS, callback_data='mortal')]]
    reply_markup = InlineKeyboardMarkup(send_menu)
    await update.message.reply_text(messages.SEND_COMMAND, reply_markup=reply_markup)

    return CHOOSING

async def startAngel(update: Update, context: CallbackContext):
    playerName = update.callback_query.message.chat.username.lower()
    if players[playerName].angel.chat_id is None:
        await update.callback_query.message.reply_text(messages.getBotNotStartedMessage(config.ANGEL_ALIAS))
        logger.info(messages.getNotRegisteredLog(config.ANGEL_ALIAS, playerName, players[playerName].angel.username))
        return ConversationHandler.END

    await update.callback_query.message.reply_text(messages.getPlayerMessage(config.ANGEL_ALIAS))
    return ANGEL

async def startMortal(update: Update, context: CallbackContext):
    playerName = update.callback_query.message.chat.username.lower()
    if players[playerName].mortal.chat_id is None:
        await update.callback_query.message.reply_text(messages.getBotNotStartedMessage(config.MORTAL_ALIAS))
        logger.info(messages.getNotRegisteredLog(config.MORTAL_ALIAS, playerName, players[playerName].mortal.username))
        return ConversationHandler.END

    await update.callback_query.message.reply_text(messages.getPlayerMessage(config.MORTAL_ALIAS))
    return MORTAL

async def sendNonTextMessage(message, bot, chat_id):
    if message.photo:
        bot.send_photo(
            photo = message.photo[-1],
            caption = message.caption,
            chat_id = chat_id
            )
    elif message.sticker:
        bot.send_sticker(
            sticker = message.sticker,
            chat_id = chat_id
            )
    elif message.document:
        bot.send_document(
            document = message.document,
             caption = message.caption,
            chat_id = chat_id
        )
    elif message.video:
        bot.send_video(
            video = message.video,
            caption = message.caption,
            chat_id = chat_id
        )
    elif message.video_note:
        bot.send_video_note(
            video_note = message.video_note,
            chat_id = chat_id
        )
    elif message.voice:
        bot.send_voice(
            voice = message.voice,
            chat_id = chat_id
        )
    elif message.audio:
        bot.send_audio(
            audio = message.audio,
            chat_id = chat_id
        )
    elif message.animation:
        bot.send_animation(
            animation = message.animation,
            chat_id = chat_id
        )

async def sendAngel(update: Update, context: CallbackContext):
    playerName = update.message.chat.username.lower()
    
    if update.message.text:
        await context.bot.send_message(
            text = messages.getReceivedMessage(config.MORTAL_ALIAS, update.message.text),
            chat_id = players[playerName].angel.chat_id
        )
    else:
        await context.bot.send_message(
            text = messages.getReceivedMessage(config.MORTAL_ALIAS),
            chat_id = players[playerName].angel.chat_id
        )
        sendNonTextMessage(update.message, context.bot, players[playerName].angel.chat_id)

    await update.message.reply_text(messages.MESSAGE_SENT)

    logger.info(messages.getSentMessageLog(config.ANGEL_ALIAS, playerName, players[playerName].angel.username))

    return ConversationHandler.END

async def sendMortal(update: Update, context: CallbackContext):
    playerName = update.message.chat.username.lower()

    if update.message.text:
        await context.bot.send_message(
            text = messages.getReceivedMessage(config.ANGEL_ALIAS, update.message.text),
            chat_id = players[playerName].mortal.chat_id
        )
    else:
        await context.bot.send_message(
            text = messages.getReceivedMessage(config.ANGEL_ALIAS),
            chat_id = players[playerName].mortal.chat_id
        )
        sendNonTextMessage(update.message, context.bot, players[playerName].mortal.chat_id)

    await update.message.reply_text(messages.MESSAGE_SENT)

    logger.info(messages.getSentMessageLog(config.MORTAL_ALIAS, playerName, players[playerName].mortal.username))

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    logger.info(f"{update.message.chat.username} canceled the conversation.")
    await update.message.reply_text(
        'Sending message cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main() -> None:
    # Load environment variables
    load_dotenv('secret.env')

    """Start the bot."""
     # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reloadplayers", reload_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('send', send_command)],
        states={
            CHOOSING: [CallbackQueryHandler(startAngel, pattern='angel'), CallbackQueryHandler(startMortal, pattern='mortal')],
            ANGEL: [MessageHandler(~filters.COMMAND, sendAngel)],
            MORTAL: [MessageHandler(~filters.COMMAND, sendMortal)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        main()
    finally:
        player.saveChatID(players)
        logger.info(f'Player chat ids have been saved in {config.CHAT_ID_JSON}')