from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import Topic, Master, session
from admin.topic_conversation import stop_conversation

TOPIC, COMPANY, NAME, PHONE, TELEGRAM, ADDRES, SPEC, OPTIONAL, TELEGRAM_URL = range(9)


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
    # session.add(Master(topic_master=topic_master_id, optional='WHAITING FOR UP DATE'))
    # session.commit()
    context.user_data['topic_id'] = topic_master_id
    await update.message.reply_text(text='Введи название организации или нажми /skip если это поле не требуется.')
    return COMPANY


async def new_master_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    company_name = update.message.text
    if company_name == '/skip':
        context.user_data['company_name'] = None
    else:
        context.user_data['company_name'] = company_name
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().company_name = company_name
        # session.commit()

    await update.message.reply_text(text='Введи имя мастера или нажми /skip если это поле не требуется.')
    return NAME


async def new_master_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    master_name = update.message.text
    if master_name == '/skip':
        context.user_data['phone'] = None
    else:
        context.user_data['master_name'] = master_name
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().name = master_name
        # session.commit()
    await update.message.reply_text(text='Введи контактный номер мастера или организации,  или нажми /skip если это поле не требуется.')

    return PHONE


async def new_master_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.replace(' ', '')
    if phone == '/skip':
        context.user_data['phone'] = None
    else:
        context.user_data['phone'] = phone
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().phone = phone
        # session.commit()
    await update.message.reply_text(text='Введи telegram или нажми /skip если это поле не требуется.')
    return TELEGRAM


async def new_master_telegram_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram = update.message.text
    if telegram == '/skip':
        context.user_data['telegram'] = None
    else:
        context.user_data['telegram'] = telegram
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().telegram = telegram
        # session.commit()
    await update.message.reply_text(text='Введи номер по которому можно будет создать ссылку вида t.me/*номер* или нажми /skip если это поле не требуется.')
    return TELEGRAM_URL


async def new_master_addres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_url = update.message.text
    if telegram_url == '/skip':
        context.user_data['telegram_url'] = None
    else:
        context.user_data['telegram_url'] = telegram_url
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().tg_url = telegram_url
        # session.commit()
    await update.message.reply_text(text='Введи адрес мастера/организации или нажми /skip если это поле не требуется.')
    return ADDRES


async def new_master_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    addres = update.message.text
    if addres == '/skip':
        context.user_data['addres'] = None
    else:
        context.user_data['addres'] = addres
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().addres = addres
        # session.commit()
    await update.message.reply_text(text='Введи специализацию мастера или нажми /skip если это поле не требуется.')
    return SPEC


async def new_master_optional(update: Update, context: ContextTypes.DEFAULT_TYPE):
    spec = update.message.text
    if spec == '/skip':
        pass
    else:
        context.user_data['spec'] = spec
        # session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one().specialization = spec
        # session.commit()
    await update.message.reply_text(text='Введи дополнительные данные которые могут быть полезны клиентам,'
                                         ' или нажми /skip если это поле не требуется.')
    return OPTIONAL


async def new_master_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    optional = update.message.text
    # new_master = session.query(Master).where(Master.optional == 'WHAITING FOR UP DATE').one()
    if optional == '/skip':
        # new_master.optional = None
        # session.commit()
        context.user_data['optional'] = None
    else:
        context.user_data['optional'] = optional
    session.add(Master(topic_master=context.user_data['topic_id'],
                                    company_name=context.user_data['company_name'],
                                    name=context.user_data['master_name'],
                                    phone=context.user_data['phone'],
                                    Telegram=context.user_data['telegram'],
                                    addres=context.user_data['addres'],
                                    specialization=context.user_data['spec'],
                                    tg_url=context.user_data['telegram_url'],
                                    optional=context.user_data['optional']))
    session.commit()
    new_master = session.query(Master).order_by(Master.master_id.desc()).first()
    await publish_new_master(context, new_master)
    await update.message.reply_text('Новый мастер успешно добавлен в БД и запись о нем опубликована в соответствующем топике.\nВернуться в начало: /start')
    return ConversationHandler.END


async def publish_new_master(context: ContextTypes.DEFAULT_TYPE,  master: Master):
    msg = ''
    buttons_keyboard = []
    for key, values in master.__msgdict__().items():
        if values is not None:
            if key == 'Ссылка на телеграм':
                buttons_keyboard.append([InlineKeyboardButton(text='Написать в телеграм', url=f'https://t.me/{values}')])
                continue
            msg += f'<b>{key}</b>: {values}\n\n'
    buttons_keyboard.append([InlineKeyboardButton(text='Оставить отзыв', url=f'https://t.me/psprofbot?start={master.master_id}')])
    x = await context.bot.send_message(chat_id='@PSPROF', message_thread_id=master.topic_master, text=msg,
                                       reply_markup=InlineKeyboardMarkup(buttons_keyboard), parse_mode='HTML')
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
        TELEGRAM: [MessageHandler(filters.TEXT, new_master_telegram_url)],
        TELEGRAM_URL: [MessageHandler(filters.TEXT, new_master_addres)],
        ADDRES:  [MessageHandler(filters.TEXT, new_master_specialization)],
        SPEC:  [MessageHandler(filters.TEXT, new_master_optional)],
        OPTIONAL:  [MessageHandler(filters.TEXT, new_master_end)]
    }, fallbacks=[CommandHandler('stop', stop_conversation)], conversation_timeout=600
)

