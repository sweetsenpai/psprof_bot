from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    InlineQueryHandler,
    CallbackQueryHandler, ContextTypes)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        bot = context.args
        print(bot)
    except:
        print('None')
    button = InlineKeyboardButton(text='Чат', url='https://t.me/SPBprofBot?start=1234')
    await update.message.reply_text('Привет', reply_markup=InlineKeyboardMarkup([[button]]))
    # 3 4 5
    print('----------------------------------------')
    # await context.bot.send_message(chat_id=-1001358438088, text='test', disable_notification=False, message_thread_id=3)
    return


def main() -> None:
    application = Application.builder().token().build()
    start_command = CommandHandler('start', start)
    application.add_handler(start_command)
    application.run_polling()


if __name__ == '__main__':
    main()