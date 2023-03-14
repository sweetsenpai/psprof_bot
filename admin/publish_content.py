from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from database.db_bilder import session, Review, Master


async def aprove_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_review_id = int(update.callback_query.data.split(',')[1])
    session.query(Review).where(Review.review_id == new_review_id).one().review_moderation = True
    session.commit()
    answer_id = update.callback_query.from_user.id
    await context.bot.sendMessage(chat_id=answer_id, text='Отзыв опубикован!')
    await update.callback_query.edit_message_reply_markup(reply_markup=None)
    await update.callback_query.answer()
    return


async def decline_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_review_id = int(update.callback_query.data.split(',')[1])
    session.query(Review).where(Review.review_id == new_review_id).delete()
    session.commit()
    answer_id = update.callback_query.from_user.id
    await context.bot.sendMessage(chat_id=answer_id, text='Отзыв удален!')
    await update.callback_query.edit_message_reply_markup(reply_markup=None)
    await update.callback_query.answer()
    return


async def show_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    show_master_id = int(update.callback_query.data.split(',')[1])
    show_review_id = int(update.callback_query.data.split(',')[2])
    master_msg = session.query(Master).where(Master.master_id == show_master_id).one().msg_id

    comments = session.query(Review).where(Review.user_master == show_master_id).where(Review.review_moderation == 1).all()

    if len(comments) == abs(show_review_id):
        show_review_id = 0
    comment_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text='◀️', callback_data=f'VR,{show_master_id},{show_review_id + 1} '),
                                              InlineKeyboardButton(text='▶️', callback_data=f'VR,{show_master_id},{show_review_id - 1} ')],
                                             [InlineKeyboardButton(text='Назад',  url=f'https://t.me/spb_test123/{master_msg}')]])
    msg = f'{comments[show_review_id].review_text}\n{comments[show_review_id].review_rating}/5⭐️'
    await update.callback_query.edit_message_text(text=msg, reply_markup=comment_keyboard, parse_mode='HTML')
    return


async def show_review_star(update: Update, context: ContextTypes.DEFAULT_TYPE, master_id):
    show_master_id = master_id
    comments = session.query(Review).where(Review.user_master == show_master_id).where(
        Review.review_moderation == 1).all()
    show_review_id = -1
    print(show_review_id, show_master_id)
    comments = session.query(Review).where(Review.user_master == show_master_id).where(Review.review_moderation == 1).all()
    master_msg = session.query(Master).where(Master.master_id == master_id).one().msg_id
    if len(comments) == abs(show_review_id):
        show_review_id = 0
    comment_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='◀️', callback_data=f'VR,{show_master_id},{show_review_id + 1} '),
          InlineKeyboardButton(text='▶️', callback_data=f'VR,{show_master_id},{show_review_id - 1} ')],
         [InlineKeyboardButton(text='Назад', url=f'https://t.me/spb_test123/{master_msg}')]])

    msg = f'{comments[show_review_id].review_text}\n{comments[show_review_id].review_rating}/5⭐️'
    await update.message.reply_text(text=msg, reply_markup=comment_keyboard, parse_mode='HTML')
    return


async def master_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    show_card_master = int(update.callback_query.data.split(',')[1])
    master = session.query(Master).where(Master.master_id == show_card_master).one()
    review = InlineKeyboardButton(text='Отзывы', callback_data=f'VR,{master.master_id},-1')
    leav_review = InlineKeyboardButton(text='Оставить отзыв', url=f'https://t.me/SPBprofBot?start={master.master_id}')
    msg = ''
    for key, values in master.__msgdict__().items():
        if values is not None:
            msg += f'{key}: <i>{values}</i>\n'
    await update.callback_query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup([[review], [leav_review]]), parse_mode='HTML')

    return


async def raiting_update(context: ContextTypes.DEFAULT_TYPE):
    masters = session.query(Master).all()
    for master in masters:
        avg_reiting = 0
        reviews = session.query(Review).where(Review.user_master == master.master_id).where(Review.review_moderation == 1).all()
        if len(reviews) == 0:
            continue
        for review in reviews:
            avg_reiting += review.review_rating

        avg_reiting = avg_reiting/len(reviews)
        msg = ''
        for key, values in master.__msgdict__().items():
            if values is not None:
                msg += f'{key}: <i>{values}</i>\n'
        msg += f'Рейтинг: {round(avg_reiting, 1)}⭐️'
        review = InlineKeyboardButton(text='Отзывы', url=f'https://t.me/SPBprofBot?start=R{master.master_id}')
        leav_review = InlineKeyboardButton(text='Оставить отзыв',
                                               url=f'https://t.me/SPBprofBot?start={master.master_id}')

        try:
            await context.bot.edit_message_text(chat_id='@spb_test123', message_id=master.msg_id, text=msg, parse_mode='HTML',
                                                reply_markup=InlineKeyboardMarkup([[review], [leav_review]]),)
        except error.BadRequest:
            continue
    return

