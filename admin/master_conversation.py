from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import Topic, Master, session
from admin.topic_conversation import stop_conversation

TOPIC, COMPANY, NAME, PHONE, TELEGRAM, ADDRES, SPEC, OPTIONAL = range(8)


def create_topic_keyboard():
    topics = session.query(Topic).all()
    button_list = []
    for topic in topics:

        button_list.append([KeyboardButton(text=topic.title)])
    return ReplyKeyboardMarkup(keyboard=button_list)


async def new_master_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in [352354383, 366585]:
        await update.message.reply_text('Я тебя не знаю!')
        return ConversationHandler.END
    await update.message.reply_text('Выберите топик в который хотите добавить мастера:',
                                    reply_markup=create_topic_keyboard())
    return TOPIC


async def new_master_company_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    master_topic_label = update.message.text
    topic_master_id = session.query(Topic).where(Topic.title == master_topic_label).one().topic_id
    session.add(Master(topic_master=topic_master_id, optional='whaiting to update'))
    session.commit()
    await update.message.reply_text(text='Введи название организации или нажми /skip если это поле не требуется.')
    return COMPANY


async def new_master_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    company_name = update.message.text
    if company_name == '/skip':
        pass
    else:
        session.query(Master).where(Master.optional == 'whaiting to update').one().company_name = company_name
        session.commit()

    await update.message.reply_text(text='Введи имя мастера или нажми /skip если это поле не требуется.')
    return NAME


async def new_master_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    master_name = update.message.text
    if master_name == '/skip':
        pass
    else:
        session.query(Master).where(Master.optional == 'whaiting to update').one().name = master_name
        session.commit()
    await update.message.reply_text(text='Введи контактный номер мастера или организации,  или нажми /skip если это поле не требуется.')

    return PHONE


async def new_master_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    if phone == '/skip':
        pass
    else:
        session.query(Master).where(Master.optional == 'whaiting to update').one().phone = phone
        session.commit()
    await update.message.reply_text(text='Введи telegram или нажми /skip если это поле не требуется.')
    return TELEGRAM


async def new_master_addres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram = update.message.text
    if telegram == '/skip':
        pass
    else:
        session.query(Master).where(Master.optional == 'whaiting to update').one().telegram = telegram
        session.commit()
    await update.message.reply_text(text='Введи адрес мастера/организации или нажми /skip если это поле не требуется.')
    return ADDRES


async def new_master_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    addres = update.message.text
    if addres == '/skip':
        pass
    else:
        session.query(Master).where(Master.optional == 'whaiting to update').one().addres = addres
        session.commit()
    await update.message.reply_text(text='Введи специализацию мастера или нажми /skip если это поле не требуется.')
    return SPEC


async def new_master_optional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spec = update.message.text
    if spec == '/skip':
        pass
    else:
        session.query(Master).where(Master.optional == 'whaiting to update').one().specialization = spec
        session.commit()
    await update.message.reply_text(text='Введи дополнительные данные которые могут быть полезны клиентам,'
                                         ' или нажми /skip если это поле не требуется.')
    return OPTIONAL


async def new_master_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    optional = update.message.text
    new_master = session.query(Master).where(Master.optional == 'whaiting to update').one()
    if optional == '/skip':
        new_master.optional = None
        session.commit()
    else:
        new_master.optional = optional
        session.commit()
    await publish_new_master(context, new_master)
    await update.message.reply_text('Новый мастер успешно добавлен в БД и запись о нем опубликована в соответствующем топике.')
    return ConversationHandler.END


async def publish_new_master(context: ContextTypes.DEFAULT_TYPE,  master: Master):
    leav_review = InlineKeyboardButton(text='Оставить отзыв', url=f'https://t.me/psprofbot?start={master.master_id}')
    msg = ''
    for key, values in master.__msgdict__().items():
        if values is not None:
            if key == 'Номер':
                msg += f'<b>{key}<b>: <code>{values}</code>\n\n'
            else:
                msg += f'<b>{key}</b>: {values}\n\n'

    x = await context.bot.send_message(chat_id='@PSPROF', message_thread_id=master.topic_master, text=msg,
                                       reply_markup=InlineKeyboardMarkup([[leav_review]]), parse_mode='HTML')
    master.msg_id = x['message_id']
    session.commit()
    return

new_master_conversation = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Добавить нового мастера'), new_master_topic)],
    states={
        TOPIC: [MessageHandler(filters.TEXT, new_master_company_name)],
        COMPANY: [MessageHandler(filters.TEXT, new_master_name)],
        NAME:  [MessageHandler(filters.TEXT, new_master_phone)],
        PHONE:  [MessageHandler(filters.TEXT, new_master_telegram)],
        TELEGRAM: [MessageHandler(filters.TEXT, new_master_addres)],
        ADDRES:  [MessageHandler(filters.TEXT, new_master_specialization)],
        SPEC:  [MessageHandler(filters.TEXT, new_master_optional)],
        OPTIONAL:  [MessageHandler(filters.TEXT, new_master_end)]
    }, fallbacks=[CommandHandler('stop', stop_conversation)], conversation_timeout=120
)

