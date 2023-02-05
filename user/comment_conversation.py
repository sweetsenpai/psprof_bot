from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.db_bilder import Review, session
from admin.topic_conversation import stop_conversation

RAITING, COMMENT = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    parametr = context.args
    if parametr[0] is None:
        return ConversationHandler.END
    inline_raiting = InlineKeyboardMarkup([[InlineKeyboardButton(text= '⭐️⭐️⭐️⭐️⭐️', callback_data=5)],
                                           [InlineKeyboardButton(text= '⭐️⭐️⭐️⭐️', callback_data=4)],
                                           [InlineKeyboardButton(text= '⭐️⭐️⭐️', callback_data=3)],
                                           [InlineKeyboardButton(text= '⭐️⭐️', callback_data=2)],
                                           [InlineKeyboardButton(text= '⭐️', callback_data=1)]])
    await update.message.reply_text(text='Оцените мастера по шкале от 1 до 5', reply_markup=inline_raiting)
    return RAITING


async def leave_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.args)
    # session.add(Review(user_id=update.callback_query.from_user.id,
    #                    user_name=update.callback_query.from_user,
    #                    user_))
    raitng = update.callback_query.data
    print(raitng)
    await context.bot.sendMessage(chat_id=update.callback_query.from_user.id,
                                  text='Пришлите ваш отзыв.')
    return COMMENT


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comment = update.message.text
    print(comment)
    await update.message.reply_text(text='Спасибо за отзыв! \nВаш отзыв будет обупликован после модерации.')
    return ConversationHandler.END


new_comment_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        RAITING: [CallbackQueryHandler(leave_comment,)],
        COMMENT: [MessageHandler(filters.TEXT, end)]},
    fallbacks=[CommandHandler('stop', stop_conversation)])
