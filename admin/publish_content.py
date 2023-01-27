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


async def topic_selection():
    return