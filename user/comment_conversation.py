from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from database.db_bilder import Master, Review, session
from admin.topic_conversation import stop_conversation
from admin.publish_content import show_review_star
from datetime import datetime
import re

RAITING, COMMENT, CHECK, REWRITE = range(4)


async def main_board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_keyboard = ReplyKeyboardMarkup([[KeyboardButton('Создать новый топик')],
                                          [KeyboardButton('Добавить нового мастера')],
                                          [KeyboardButton('Изменить информацию о мастере')],
                                          [KeyboardButton('Удалить мастера из БД')]])
    await update.message.reply_text(text='Выбери действие', reply_markup=admin_keyboard)
    return


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    parametr = context.args
    if not parametr:
        if update.message.from_user.id in [366585, 352354383]:
            await main_board(update, update)
            return ConversationHandler.END
        else:
            await update.message.reply_text(text='Я нужен только для отзывов...')
            return ConversationHandler.END
    if re.search('[a-zA-Z]', parametr[0]):
        master = ''.join(re.findall(r'\d+', parametr[0]))
        await show_review_star(update, context, master_id=int(master))
        return ConversationHandler.END
    context.user_data['master'] = int(parametr[0])
    inline_raiting = InlineKeyboardMarkup([[InlineKeyboardButton(text= '⭐️⭐️⭐️⭐️⭐️', callback_data=5)],
                                           [InlineKeyboardButton(text= '⭐️⭐️⭐️⭐️', callback_data=4)],
                                           [InlineKeyboardButton(text= '⭐️⭐️⭐️', callback_data=3)],
                                           [InlineKeyboardButton(text= '⭐️⭐️', callback_data=2)],
                                           [InlineKeyboardButton(text= '⭐️', callback_data=1)]])
    await update.message.reply_text(text='Оцените мастера по шкале от 1 до 5', reply_markup=inline_raiting)
    return RAITING


async def leave_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query.data is not None:
        raitng = update.callback_query.data
        context.user_data['raiting'] = raitng
        await context.bot.sendMessage(chat_id=update.callback_query.from_user.id,
                                      text='Напишите мне Ваш отзыв о мастере')
        await update.callback_query.answer()
    else:
        await update.message.reply_text(text='Напишите мне Ваш отзыв о мастере')
    return CHECK


async def user_chek_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['text'] = update.message.text
    await update.message.reply_text('Проерьте ваш  комментарий перед отправкой')
    await update.message.reply_text(text=f"<i>{context.user_data['text']}</i>", parse_mode='HTML')
    await update.message.reply_text(text='Отправить сообщение в исходном виде?', reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text='Да'), KeyboardButton(text='Исправить')]]))
    return REWRITE


async def user_rewritecomment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text =='Да':
        review = Review(user_id=update.message.from_user.id,
                           user_name=update.message.from_user.username,
                           user_master=context.user_data['master'],
                           review_text=context.user_data['text'],
                           review_rating=context.user_data['raiting'],
                           time=datetime.today().strftime('%Y-%m-%d %H:%M'))
        session.add(review)
        session.commit()
        await update.message.reply_text(text='Спасибо! Ваш отзыв будет опубликован после проверки модератором')
        await send_comment_to_modderation(context, review)
        return ConversationHandler.END
    await update.message.reply_text(text='Напишите мне новый отзыв о мастере')
    return CHECK


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    review = Review(user_id=update.message.from_user.id,
                    user_name=update.message.from_user.username,
                    user_master=context.user_data['master'],
                    review_text=context.user_data['text'],
                    review_rating=context.user_data['raiting'],
                    time=datetime.today().strftime('%Y-%m-%d %H:%M'))
    session.add(review)
    session.commit()
    await update.message.reply_text(text='Спасибо! Ваш отзыв будет опубликован после проверки модератором')
    await send_comment_to_modderation(context, review)
    return ConversationHandler.END


new_comment_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        RAITING: [CallbackQueryHandler(pattern='[1-5]', callback=leave_comment)],
        CHECK: [MessageHandler(filters.TEXT, user_chek_comment)],
        REWRITE: [MessageHandler(callback=user_rewritecomment, filters=filters.ALL)],
        COMMENT: [MessageHandler(filters.TEXT, end)]},
    fallbacks=[CommandHandler('stop', stop_conversation)], allow_reentry=True)


async def send_comment_to_modderation(context: ContextTypes.DEFAULT_TYPE, review: Review):
    msg = f'НОВЫЙ ОТЗЫВ!\n Пользователь: @{review.user_name}\n Оценка: {review.review_rating}⭐️\n {review.review_text}'
    admin_review_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text='Опубликовать', callback_data=f'PR,{review.review_id}'),
                                                   InlineKeyboardButton(text='Отклонить', callback_data=f'DR,{review.review_id}')]])
    await context.bot.sendMessage(chat_id=352354383, text=msg, reply_markup=admin_review_keyboard)
    await context.bot.sendMessage(chat_id=366585, text=msg, reply_markup=admin_review_keyboard)
    return
