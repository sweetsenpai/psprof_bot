from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CallbackQueryHandler, CommandHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import session, Topic, Master

MASTER, OPTION, ACTION, ANSWER, UPDATE = range(5)


async def choice_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in [366585, 352354383]:
        await update.message.reply_text('Я тебя не знаю!')
        return ConversationHandler.END
    keyboard_topic = []
    for topic in session.query(Topic).all():
        keyboard_topic.append([InlineKeyboardButton(text=topic.title, callback_data=f'{topic.topic_id}')])
    await update.message.reply_text('Выберете топик в котором нужно изменить данные мастера:',
                                    reply_markup=InlineKeyboardMarkup(keyboard_topic))
    return MASTER


async def choice_master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_topic_id = int(update.callback_query.data)
    keyboard_master = []
    for master in session.query(Master).where(Master.topic_master == target_topic_id).all():
        if master.name is None:
            keyboard_master.append([InlineKeyboardButton(text=f'{master.company_name}: {master.phone}',
                                                             callback_data=f'{master.master_id}')])
        elif master.company_name is None:
            keyboard_master.append([InlineKeyboardButton(text=f'{master.name}: {master.phone}',
                                                             callback_data=f'{master.master_id}')])
    await update.callback_query.edit_message_text(text='Выберете мастера:',
                                                  reply_markup=InlineKeyboardMarkup(keyboard_master))
    return OPTION


async def choice_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.callback_query.data)
    master_id = int(update.callback_query.data)
    keyboard_option = [
        [InlineKeyboardButton(text='Название организации', callback_data=f'{master_id},company_name')],
        [InlineKeyboardButton(text='Имя', callback_data=f'{master_id},name')],
        [InlineKeyboardButton(text='Телефон', callback_data=f'{master_id},phone')],
        [InlineKeyboardButton(text='Адрес', callback_data=f'{master_id},addres')],
        [InlineKeyboardButton(text='Специализация', callback_data=f'{master_id},specialization')],
        [InlineKeyboardButton(text='Опционально', callback_data=f'{master_id},optional')]
    ]
    await update.callback_query.edit_message_text(text='Выберете категорию:',
                                                  reply_markup=InlineKeyboardMarkup(keyboard_option))
    return ACTION


async def choice_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    keyboard_action = [
        [InlineKeyboardButton(text='Изменить', callback_data=f'UP,{data}'),
         InlineKeyboardButton(text='Удалить', callback_data=f'DEL,{data}')]
    ]
    await update.callback_query.edit_message_text(text='Выберете действие:', reply_markup=InlineKeyboardMarkup(keyboard_action))
    return ANSWER


async def action_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.callback_query.data.split(',')

    master = session.query(Master).where(Master.master_id == answer[1]).one()

    for key in master.__to_dict__().keys():
        if key == answer[2]:
            if answer[0] == 'DEL':
                setattr(master, key, None)
                session.commit()
                await update.callback_query.edit_message_text('Занчение успешно удалено.')
                return ConversationHandler.END
            if answer[0] == 'UP':
                setattr(master, key, 'WHAITING FOR UP DATE')
                session.commit()
                await update.callback_query.edit_message_text('Введите новое значение:')
                return UPDATE


async def update_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_data = update.message.text
    masters = session.query(Master).all()
    for master in masters:
        for key, values in master.__to_dict__().items():
            if values == 'WHAITING FOR UP DATE':
                setattr(master, key, new_data)
                session.commit()
    await update.message.reply_text('Значение успешно обновлено.')
    return ConversationHandler.END


async def stop_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Диалог остановлен')
    return ConversationHandler.END

update_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Изменить информацию о мастере'), choice_topic)],
    states={
        MASTER: [CallbackQueryHandler(callback=choice_master)],
        OPTION: [CallbackQueryHandler(callback=choice_option)],
        ACTION: [CallbackQueryHandler(callback=choice_action)],
        ANSWER: [CallbackQueryHandler(callback=action_answer)],
        UPDATE: [MessageHandler(filters.TEXT, update_data)]
    },
    fallbacks=[CommandHandler('stop', stop_conversation)], conversation_timeout=120)









