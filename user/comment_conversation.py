from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import Master, Review, session
from admin.topic_conversation import stop_conversation

RAITING, COMMENT = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    parametr = context.args[0]
    if parametr is None:
        return ConversationHandler.END
    inline_raiting = InlineKeyboardMarkup([[InlineKeyboardButton(text= '⭐️⭐️⭐️⭐️⭐️', callback_data=5)],
                                           [InlineKeyboardButton(text= '⭐️⭐️⭐️⭐️', callback_data=4)],
                                           [InlineKeyboardButton(text= '⭐️⭐️⭐️', callback_data=3)],
                                           [InlineKeyboardButton(text= '⭐️⭐️', callback_data=2)],
                                           [InlineKeyboardButton(text= '⭐️', callback_data=1)]])
    await update.message.reply_text(text='Оцените мастера по шкале от 1 до 5', reply_markup=inline_raiting)
    session.add(Review(user_id=update.message.from_user.id,
                       user_name=update.message.from_user.username,
                       user_master=int(parametr),
                       review_text='in progress'))
    session.commit()
    return RAITING


async def leave_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    raitng = update.callback_query.data
    await update.callback_query.answer()
    session.query(Review).where(Review.user_id == update.callback_query.from_user.id and Review.review_text == 'in progress').first().review_rating = raitng
    session.commit()
    await context.bot.sendMessage(chat_id=update.callback_query.from_user.id,
                                  text='Пришлите ваш отзыв.')
    return COMMENT


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    review = session.query(Review).where(Review.user_id == update.message.from_user.id, Review.review_text == 'in progress').first()
    review.review_text = update.message.text
    session.commit()
    await update.message.reply_text(text='Спасибо за отзыв! \nВаш отзыв будет обупликован после модерации.')
    await send_comment_to_modderation(context, review)
    return ConversationHandler.END


new_comment_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        RAITING: [CallbackQueryHandler(leave_comment,)],
        COMMENT: [MessageHandler(filters.TEXT, end)]},
    fallbacks=[CommandHandler('stop', stop_conversation)])


async def send_comment_to_modderation(context: ContextTypes.DEFAULT_TYPE, review: Review):
    message_master_id = session.query(Master).where(Master.master_id == review.user_master).one().msg_id
    await context.bot.forwardMessage(chat_id=352354383, from_chat_id='@spb_test123', message_id=message_master_id)
    msg = f'НОВЫЙ ОТЗЫВ!\n Пользователь: @{review.user_name}\n Оценка: {review.review_rating}⭐️\n {review.review_text}'
    admin_review_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text='Опубликовать', callback_data='PR'), InlineKeyboardButton(text='Отклонить', callback_data='DR')]])
    await context.bot.sendMessage(chat_id=352354383, text=msg, reply_markup=admin_review_keyboard)
    return
