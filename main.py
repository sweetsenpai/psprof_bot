from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from admin.topic_conversation import new_topic_conversation
from admin.master_conversation import new_master_conversation
from user.comment_conversation import new_comment_conversation
from user.comment_conversation import start
import logging
import os
token = os.environ['TOKEN']
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(token).build()
    application.add_handler(new_comment_conversation)
    application.add_handler(new_topic_conversation)
    application.add_handler(new_master_conversation)
    application.run_polling()


if __name__ == '__main__':
    main()