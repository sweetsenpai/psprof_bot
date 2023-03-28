from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CallbackQueryHandler, CommandHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import session, Topic, Master, Review

MASTER, DEL = range(2)


async def del_topic_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in [366585, 352354383]:
        await update.message.reply_text('Я тебя не знаю!')
        return
    topics = session.query(Topic).all()
    topic_menu_button = []
    for topic in topics:
        topic_menu_button.append([InlineKeyboardButton(text=topic.title, callback_data=f'DLT,{topic.topic_id}')])
    await update.message.reply_text(text='Выберете топик из которого необходимо удалить мастера', reply_markup=InlineKeyboardMarkup(topic_menu_button))
    return


async def del_master_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.callback_query.data.split(',')[1])
    masters = session.query(Master).where(Master.topic_master == update.callback_query.data.split(',')[1]).all()
    master_menu_button = []
    for master in masters:
        master_menu_button.append([InlineKeyboardButton(text=master.phone, callback_data=f'DLM,{master.master_id}')])
    await update.callback_query.edit_message_text(text='Выберете мастера которого необходимо удалить.\n Помните, что после удаления все данные и комментарии будут утеряны!',
                                                  reply_markup=InlineKeyboardMarkup(master_menu_button))
    await update.callback_query.answer()
    return


async def del_master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    del_maste_id = update.callback_query.data.split(',')[1]
    session.query(Master).filter(Master.master_id == del_maste_id).delete()
    session.query(Review).filter(Review.user_master == del_maste_id).delete()
    session.commit()
    await update.callback_query.edit_message_text(text='Мастер удален из БД. Теперь можно удалить сообщение из группы.')
    await update.callback_query.answer()
    return


