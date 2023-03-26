from telegram.ext import (ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler)
from telegram import Update
from database.db_bilder import Topic, session


TOPIC_TITLE = range(1)


async def new_topic_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != 352354383 or update.message.from_user != 366585:
        await update.message.reply_text('Я тебя не знаю!')
        return ConversationHandler.END
    await update.message.reply_text('Введите название нового топика')
    return TOPIC_TITLE


async def new_topic_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic_title = update.message.text
    topic = await context.bot.createForumTopic(chat_id=-1001358438088, name=topic_title)
    session.add(Topic(topic_id=topic['message_thread_id'], titel=topic['name']))
    session.commit()
    await update.message.reply_text(f'Топик {topic_title} успешно создан!')
    return ConversationHandler.END


async def stop_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Диалог остановлен')
    return ConversationHandler.END

new_topic_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Создать новый топик'), new_topic_start)],
    states={
        TOPIC_TITLE: [MessageHandler(filters.TEXT, new_topic_end)]
    },
    fallbacks=[CommandHandler('stop', stop_conversation)])
