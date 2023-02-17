from telegram.ext import (
    Application,
    CommandHandler, CallbackQueryHandler,
    ContextTypes)
from telegram import Update
from admin.publish_content import aprove_review, decline_review
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


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(chat_id=352354383, text=update.callback_query.data)
    return


def main() -> None:
    application = Application.builder().token(token).build()

    application.add_handler(CallbackQueryHandler(pattern='PR,', callback=aprove_review))
    application.add_handler(CallbackQueryHandler(pattern='DR,', callback=decline_review))
    application.add_handler(CommandHandler('test', test))
    application.add_handler(new_comment_conversation)
    application.add_handler(new_topic_conversation)
    application.add_handler(new_master_conversation)
    application.run_polling()


if __name__ == '__main__':
    main()