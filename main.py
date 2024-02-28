from telegram.ext import Application, CallbackQueryHandler, MessageHandler, \
    AIORateLimiter, filters, CommandHandler
from datetime import time
from admin.publish_content import aprove_review, decline_review, show_review, master_card
from admin.topic_conversation import new_topic_conversation
from admin.master_conversation import new_master_conversation
from user.comment_conversation import new_comment_conversation
from admin.db_backup import send_backup_file
from admin.delete_content import del_topic_menu, del_master, del_master_menu
from admin.update_masters import update_conversation
import logging
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


PORT = int(os.environ.get('PORT', '50'))


def main() -> None:
    application = Application.builder().token(token).rate_limiter(AIORateLimiter()).build()

    application.add_handler(MessageHandler(filters.Regex('Удалить мастера из БД'), del_topic_menu))

    application.add_handler(CallbackQueryHandler(pattern='PR,', callback=aprove_review))
    application.add_handler(CallbackQueryHandler(pattern='DR,', callback=decline_review))
    application.add_handler(CallbackQueryHandler(pattern='VR,', callback=show_review))
    application.add_handler(CallbackQueryHandler(pattern='BM,', callback=master_card))
    application.add_handler(CallbackQueryHandler(pattern='DLT,', callback=del_master_menu))
    application.add_handler(CallbackQueryHandler(pattern='DLM,', callback=del_master))

    application.job_queue.run_daily(callback=send_backup_file, days=[1], job_kwargs={'misfire_grace_time': 600},
                                    time=time.fromisoformat('12:00:00+03:00'))

    application.add_handler(update_conversation)
    application.add_handler(new_comment_conversation)
    application.add_handler(new_topic_conversation)
    application.add_handler(new_master_conversation)
    application.run_polling()


if __name__ == '__main__':

    main()
