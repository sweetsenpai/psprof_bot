from telegram.ext import ContextTypes
from telegram import Update
from datetime import datetime


async def send_backup_file(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(chat_id=366585, document='psprof.db', caption=f'db backup from {datetime.now().date()}')
    await context.bot.send_document(chat_id=366585, document='../../admin/DB/admin.db', caption=f'db backup from {datetime.now().date()}')
    return

