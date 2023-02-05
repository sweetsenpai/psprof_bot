from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import Topic, Master, session
from admin.topic_conversation import stop_conversation
from sqlalchemy import update as sql_update
TOPIC, MASTER_INFO = range(2)


def create_topic_keyboard():
    topics = session.query(Topic).all()
    button_list = []
    for topic in topics:
        button_list.append([KeyboardButton(text=topic.title)])
    return ReplyKeyboardMarkup(keyboard=button_list)


async def new_master_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Выбирите топик в который хотите добавить мастера:',
                                    reply_markup=create_topic_keyboard())
    return TOPIC


async def new_master_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_master_topic_label = update.message.text
    await update.message.reply_text(text='Введите текст объявления.')
    print(new_master_topic)
    topic_master_id = session.query(Topic).where(Topic.title == new_master_topic_label).one().topic_id
    print(topic_master_id)
    session.add(Master(topic_master=topic_master_id, info='whaiting to update'))
    session.commit()
    return MASTER_INFO


async def new_master_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    master_info = update.message.text
    update_master = session.query(Master).where(Master.info == 'whaiting to update').one()
    update_master.info = master_info
    session.commit()
    await update.message.reply_text(text='Новый мастер добавлен!')
    await publish_new_master(context, update_master)
    await update.message.reply_text(text='Запись опубликована в группе.')
    return ConversationHandler.END

new_master_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Добавить нового мастера'), new_master_topic)],
    states={
        TOPIC: [MessageHandler(filters.TEXT, new_master_info)],
        MASTER_INFO: [MessageHandler(filters.TEXT, new_master_end)]
    },
    fallbacks=[CommandHandler('stop', stop_conversation)])


async def publish_new_master(context: ContextTypes.DEFAULT_TYPE,  master):
    review = InlineKeyboardButton(text='Отзывы', callback_data=f'VR,{master.master_id}')
    leav_review = InlineKeyboardButton(text='Оставить отзыв', url=f'https://t.me/SPBprofBot?start={master.master_id}')
    await context.bot.send_message(chat_id=-1001358438088, message_thread_id=master.topic_master, text=master.info,
                                   reply_markup=InlineKeyboardMarkup([[review], [leav_review]]))
    return
