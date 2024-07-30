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

INFO_CHOOSING, TYPING_REPLY, SEND_CHOOSING, ANGEL = range(4)

# Enable logging
# For logging using .log files
'''
logging.basicConfig(
    filename=f'logs/{datetime.datetime.now(datetime.UTC).strftime("%d-%m-%Y-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
'''

# For logging using terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# players Dict. contains entries of Player objects involved in the Angel Mortal Sesh
players = collections.defaultdict(player.Player)
player.loadPlayers(players)


async def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    playerName = update.message.chat.username.lower()
    players[playerName].chat_id = update.message.chat.id

    if players[playerName].username is None:
        await update.message.reply_text(messages.NOT_REGISTERED)
        return

    if players[playerName].chat_id is None:
        await update.message.reply_text(messages.ERROR_CHAT_ID)
        return ConversationHandler.END

    logger.info(
        f'{playerName} started the bot with chat_id {players[playerName].chat_id}')

    if players[playerName].info is None:
        # When the player runs the bot for the first time, prompt to answer their profile questions first
        players[playerName].info = ['blank', 'blank', 'blank']
        q1_ans = players[playerName].info[0]
        q2_ans = players[playerName].info[1]
        q3_ans = players[playerName].info[2]

        send_menu = [[InlineKeyboardButton('Question 1', callback_data='1')],
                     [InlineKeyboardButton('Question 2', callback_data='2')],
                     [InlineKeyboardButton('Question 3', callback_data='3')],
                     [InlineKeyboardButton('Done', callback_data='done')],]
        reply_markup = InlineKeyboardMarkup(send_menu)

        await update.message.reply_text(
            messages.FILL_UP_QUESTIONS
            + messages.getInfoQuestion(1) + q1_ans
            + messages.getInfoQuestion(2) + q2_ans
            + messages.getInfoQuestion(3) + q3_ans,
            reply_markup=reply_markup)

        return INFO_CHOOSING

    else:
        # if the player answer already, allow to view angel profile and send message
        if players[playerName].angel.chat_id is None:
            await update.message.reply_text(messages.BOT_NOT_STARTED)

            logger.info(
                messages.notRegisteredLog(playerName, players[playerName].angel.username))

            return ConversationHandler.END

        send_menu = [[InlineKeyboardButton('View Angel Info.', callback_data='view')],
                     [InlineKeyboardButton('Send Message', callback_data='send')]]
        reply_markup = InlineKeyboardMarkup(send_menu)

        await update.message.reply_text('What would you like to do?', reply_markup=reply_markup)

        return SEND_CHOOSING


async def fill_info(update: Update, context: CallbackContext) -> int:
    """To prompt the user to type their answer for the question selected"""
    qnSelected = int(update.callback_query.data)
    context.user_data["choice"] = qnSelected

    await update.callback_query.message.reply_text(messages.getInfoQuestion(qnSelected) + messages.PROMPT_ANSWER)

    return TYPING_REPLY


async def received_info(update: Update, context: CallbackContext) -> int:
    """To retrieve user input and save info"""
    userText = update.message.text
    playerName = update.message.chat.username.lower()
    qnSelected = context.user_data["choice"]
    players[playerName].info[qnSelected - 1] = userText
    del context.user_data["choice"]

    q1_ans = players[playerName].info[0]
    q2_ans = players[playerName].info[1]
    q3_ans = players[playerName].info[2]

    send_menu = [[InlineKeyboardButton('Question 1', callback_data='1')],
                 [InlineKeyboardButton('Question 2', callback_data='2')],
                 [InlineKeyboardButton('Question 3', callback_data='3')],
                 [InlineKeyboardButton('Done', callback_data='done')],]
    reply_markup = InlineKeyboardMarkup(send_menu)

    await update.message.reply_text(
        messages.FILL_UP_QUESTIONS
        + messages.getInfoQuestion(1) + q1_ans
        + messages.getInfoQuestion(2) + q2_ans
        + messages.getInfoQuestion(3) + q3_ans,
        reply_markup=reply_markup)

    return INFO_CHOOSING


async def done_info(update: Update, context: CallbackContext) -> int:
    """Send success message when user press done button"""
    await update.callback_query.message.reply_text(messages.REGISTRATION_SUCCESS)

    return ConversationHandler.END


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(messages.HELP_TEXT)


async def view_angel_info(update: Update, context: CallbackContext) -> int:
    """Display player's angel personality quiz answers"""
    playerName = update.callback_query.message.chat.username.lower()
    angelInfo = players[playerName].angel.info
    
    await update.callback_query.edit_message_reply_markup(None) # hide inline keyboard after user select
    await update.callback_query.message.reply_text(messages.getAngelInformation(angelInfo))

    return ConversationHandler.END


async def send_command(update: Update, context: CallbackContext) -> int:
    """Start send convo when the command /send is issued."""

    await update.callback_query.edit_message_reply_markup(None) # hide inline keyboard after user select
    await update.callback_query.message.reply_text(messages.REQUEST_PLAYER_MESSAGE)

    return ANGEL


async def sendAngel(update: Update, context: CallbackContext) -> int:
    """Send the message to the player's Angel"""
    playerName = update.message.chat.username.lower()

    if update.message.text:
        await context.bot.send_message(
            text=messages.receivedMessage(update.message.text),
            chat_id=players[playerName].angel.chat_id)
    else:
        await sendNonTextMessage(
            context, update.message, context.bot, players[playerName].angel.chat_id)

    await update.message.reply_text(messages.MESSAGE_SENT)

    logger.info(
        messages.sentMessageLog(playerName, players[playerName].angel.username))

    return ConversationHandler.END


async def sendNonTextMessage(context, message, bot, chat_id):
    if message.photo:
        await context.bot.send_message(
            text=messages.RECEIVE_PHOTO,
            chat_id=chat_id)

        await bot.send_photo(
            photo=message.photo[-1],
            caption=message.caption,
            chat_id=chat_id)

    elif message.sticker:
        await context.bot.send_message(
            text=messages.RECEIVE_STICKER,
            chat_id=chat_id)

        await bot.send_sticker(
            sticker=message.sticker,
            chat_id=chat_id)

    elif message.document:
        await context.bot.send_message(
            text=messages.RECEIVE_DOCUMENT,
            chat_id=chat_id)

        await bot.send_document(
            document=message.document,
            caption=message.caption,
            chat_id=chat_id)

    elif message.video:
        await context.bot.send_message(
            text=messages.RECEIVE_VIDEO,
            chat_id=chat_id)

        await bot.send_video(
            video=message.video,
            caption=message.caption,
            chat_id=chat_id)

    elif message.video_note:
        await context.bot.send_message(
            text=messages.RECEIVE_TELEBUBBLE,
            chat_id=chat_id)

        await bot.send_video_note(
            video_note=message.video_note,
            chat_id=chat_id)

    elif message.voice:
        await context.bot.send_message(
            text=messages.RECEIVE_VOICE,
            chat_id=chat_id)

        await bot.send_voice(
            voice=message.voice,
            chat_id=chat_id)

    elif message.audio:
        await context.bot.send_message(
            text=messages.RECEIVE_AUDIO,
            chat_id=chat_id)

        await bot.send_audio(
            audio=message.audio,
            chat_id=chat_id)

    elif message.animation:
        await context.bot.send_message(
            text=messages.RECEIVE_GIF,
            chat_id=chat_id)

        await bot.send_animation(
            animation=message.animation,
            chat_id=chat_id)


async def cancel(update: Update, context: CallbackContext) -> int:
    """Send message when user enters /cancel command"""
    await update.message.reply_text(messages.CANCEL_COMMAND, reply_markup=ReplyKeyboardRemove())

    logger.info(f"{update.message.chat.username} canceled the conversation.")

    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Load environment variables
    load_dotenv('secret.env')

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    application.add_handler(CommandHandler("help", help_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INFO_CHOOSING: [CallbackQueryHandler(fill_info, pattern='^(1|2|3)$'), CallbackQueryHandler(done_info, pattern='done')],
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~(filters.COMMAND), received_info)],
            SEND_CHOOSING: [CallbackQueryHandler(view_angel_info, pattern='view'), CallbackQueryHandler(send_command, pattern='send')],
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
