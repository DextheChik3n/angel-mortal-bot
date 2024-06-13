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

CHOOSING, ANGEL, MORTAL = range(3)

# Enable logging
logging.basicConfig(
    filename=f'logs/{datetime.datetime.now(datetime.UTC).strftime("%d-%m-%Y-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# players Dict. contains entries of Player objects
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
        logger.info(
            f'Player chat ids have been saved in {config.CHAT_ID_JSON}')
