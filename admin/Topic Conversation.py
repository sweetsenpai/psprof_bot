from telegram.ext import (ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler)
from telegram import Update
from database.db_bilder import session, Topic
import logging

TOPIC_TITLE = range(1)


async def new_topic_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Введите название нового топика')
    return TOPIC_TITLE


async def new_topic_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_title = update.message.text
    x = await context.bot.createForumTopic(chat_id=-1001358438088, name=topic_title)
    print(x)
    return ConversationHandler.END

    # session.add(Topic(titel=topic_title))


async def stop_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Диалог остановлен')
    return ConversationHandler.END

topic_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Создать новый топик'), new_topic_start)],
    states={
        TOPIC_TITLE: [MessageHandler(filters.TEXT, new_topic_end)]
    },
    fallbacks=[CommandHandler('stop', stop_conversation)])
