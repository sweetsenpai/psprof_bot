from telegram.ext import Application,CommandHandler, CallbackQueryHandler, ContextTypes, AIORateLimiter
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from admin.publish_content import aprove_review, decline_review, show_review, master_card, raiting_update
from admin.topic_conversation import new_topic_conversation
from admin.master_conversation import new_master_conversation
from user.comment_conversation import new_comment_conversation
import logging
import os
token = os.environ['TOKEN']
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_keyboard = ReplyKeyboardMarkup([[KeyboardButton('Добавить нового мастера.')], [KeyboardButton('Создать новый топик')]])
    await update.message.reply_text(text='Выбери действие', reply_markup=admin_keyboard)
    return


def main() -> None:
    application = Application.builder().token(token).rate_limiter(AIORateLimiter(group_time_period=15, group_max_rate=0)).build()

    application.add_handler(CommandHandler('menu', main_board))
    application.add_handler(CallbackQueryHandler(pattern='PR,', callback=aprove_review))
    application.add_handler(CallbackQueryHandler(pattern='DR,', callback=decline_review))
    application.add_handler(CallbackQueryHandler(pattern='VR,', callback=show_review))
    application.add_handler(CallbackQueryHandler(pattern='BM,', callback=master_card))
    application.add_handler(new_comment_conversation)
    application.add_handler(new_topic_conversation)
    application.add_handler(new_master_conversation)
    application.job_queue.run_repeating(callback=raiting_update, interval=30, job_kwargs={'misfire_grace_time': 60})
    application.run_polling()


if __name__ == '__main__':
    main()