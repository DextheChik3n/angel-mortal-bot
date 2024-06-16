import logging
import player
import messages
import datetime
import collections
import config
import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler

ANGEL = range(1)

# Enable logging
logging.basicConfig(
    filename=f'logs/{datetime.datetime.now(datetime.UTC).strftime("%d-%m-%Y-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# players Dict. contains entries of Player objects involved in the Angel Mortal Sesh
players = collections.defaultdict(player.Player)
player.loadPlayers(players)


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    playerName = update.message.chat.username.lower()
    if players[playerName].username is None:
        await update.message.reply_text(messages.NOT_REGISTERED)
        return

    players[playerName].chat_id = update.message.chat.id

    logger.info(
        f'{playerName} started the bot with chat_id {players[playerName].chat_id}')

    await update.message.reply_text(f'Hi! {messages.HELP_TEXT}')


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(messages.HELP_TEXT)


async def send_command(update: Update, context: CallbackContext):
    """Start send convo when the command /send is issued."""
    playerName = update.message.chat.username.lower()

    if players[playerName].username is None:
        await update.message.reply_text(messages.NOT_REGISTERED)
        return ConversationHandler.END

    if players[playerName].chat_id is None:
        await update.message.reply_text(messages.ERROR_CHAT_ID)
        return ConversationHandler.END

    if players[playerName].angel.chat_id is None:
        await update.message.reply_text(messages.getBotNotStartedMessage(config.ANGEL_ALIAS))

        logger.info(
            messages.getNotRegisteredLog(
                config.ANGEL_ALIAS, playerName, players[playerName].angel.username))

        return ConversationHandler.END

    await update.message.reply_text(messages.getPlayerMessage(config.ANGEL_ALIAS))

    return ANGEL


async def sendAngel(update: Update, context: CallbackContext):
    playerName = update.message.chat.username.lower()

    if update.message.text:
        await context.bot.send_message(
            text=messages.getReceivedMessage(
                config.MORTAL_ALIAS, update.message.text),
            chat_id=players[playerName].angel.chat_id)
    # else:
    #     await context.bot.send_message(
    #         text=messages.getReceivedMessage(config.MORTAL_ALIAS),
    #         chat_id=players[playerName].angel.chat_id)

    #     sendNonTextMessage(update.message, context.bot, players[playerName].angel.chat_id)

    await update.message.reply_text(messages.MESSAGE_SENT)

    logger.info(
        messages.getSentMessageLog(
            config.ANGEL_ALIAS, playerName, players[playerName].angel.username))

    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'Sending message cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    logger.info(f"{update.message.chat.username} canceled the conversation.")

    return ConversationHandler.END


def main() -> None:
    # Load environment variables
    load_dotenv('secret.env')

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('send', send_command)],
        states={
            # CHOOSING: [CallbackQueryHandler(startAngel, pattern='angel')],
            ANGEL: [MessageHandler(~filters.COMMAND, sendAngel)]
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
        logger.info(
            f'Player chat ids have been saved in {config.CHAT_ID_JSON}')
