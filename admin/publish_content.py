import asyncio

import telegram.error
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, error
from database.db_bilder import session, Review, Master


async def aprove_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_review_id = int(update.callback_query.data.split(',')[1])
    review = session.query(Review).where(Review.review_id == new_review_id).one()
    try:
        await message_update(update, context, master_id=review.user_master)
    except telegram.error.BadRequest:
        pass
    review.review_moderation = True
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
                                             [InlineKeyboardButton(text='Назад',  url=f'https://t.me/PSPROF/{master_msg}')]])
    if abs(show_review_id)!=0:
        msg = f'{comments[show_review_id].review_text}\n{comments[show_review_id].review_rating}/5⭐️\n\n<i>{comments[show_review_id].time}\n{abs(show_review_id)}/{len(comments)}</i>'
    else:
        msg = f'{comments[show_review_id].review_text}\n{comments[show_review_id].review_rating}/5⭐️\n\n<i>{comments[show_review_id].time}\n{len(comments)}/{len(comments)}</i>'

    await update.callback_query.edit_message_text(text=msg, reply_markup=comment_keyboard, parse_mode='HTML')
    return


async def show_review_star(update: Update, context: ContextTypes.DEFAULT_TYPE, master_id):
    show_master_id = master_id
    show_review_id = -1
    comments = session.query(Review).where(Review.user_master == show_master_id).where(Review.review_moderation == 1).all()
    master_msg = session.query(Master).where(Master.master_id == master_id).one().msg_id
    if len(comments) == abs(show_review_id):
        show_review_id = 0
    comment_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='◀️', callback_data=f'VR,{show_master_id},{show_review_id + 1} '),
          InlineKeyboardButton(text='▶️', callback_data=f'VR,{show_master_id},{show_review_id - 1} ')],
         [InlineKeyboardButton(text='Назад', url=f'https://t.me/PSPROF/{master_msg}')]])

    msg = f'{comments[show_review_id].review_text}\n{comments[show_review_id].review_rating}/5⭐️\n\n<i>{comments[show_review_id].time}\n1/{len(comments)}</i>'
    await update.message.reply_text(text=msg, reply_markup=comment_keyboard, parse_mode='HTML')
    return


async def master_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    show_card_master = int(update.callback_query.data.split(',')[1])
    master = session.query(Master).where(Master.master_id == show_card_master).one()
    msg = ''
    buttons_keyboard = []
    for key, values in master.__msgdict__().items():
        if values is not None:
            if key == 'Ссылка на телеграм':
                buttons_keyboard.append(
                    [InlineKeyboardButton(text='Написать в телеграм', url=f'https://t.me/{values}')])
                continue
            msg += f'<b>{key}</b>: {values}\n\n'
    buttons_keyboard.append([InlineKeyboardButton(text='Отзывы', callback_data=f'VR,{master.master_id},-1')])
    buttons_keyboard.append(
        [InlineKeyboardButton(text='Оставить отзыв', url=f'https://t.me/psprofbot?start={master.master_id}')])
    await update.callback_query.edit_message_text(text=msg, reply_markup=InlineKeyboardMarkup(buttons_keyboard), parse_mode='HTML')

    return


async def message_update(update: Update, context: ContextTypes.DEFAULT_TYPE, master_id: int):
    master_record = session.query(Master).where(Master.master_id == master_id).one()
    reviews = session.query(Review).where(Review.user_master == master_record.master_id).where(Review.review_moderation == 1).all()
    leav_review = InlineKeyboardButton(text='Оставить отзыв', url=f'https://t.me/psprofbot?start={master_record.master_id}')
    show_reviews = InlineKeyboardButton(text='Отзывы', url=f'https://t.me/psprofbot?start=R{master_record.master_id}')

    msg = ''
    buttons_keyboard = []
    for key, values in master_record.__msgdict__().items():
        if values is not None:
            if key == 'Ссылка на телеграм':
                buttons_keyboard.append(
                    [InlineKeyboardButton(text='Написать в телеграм', url=f'https://t.me/{values}')])
                continue
            msg += f'<b>{key}</b>: {values}\n\n'

    if not reviews:
        buttons_keyboard.append([leav_review])
    else:
        buttons_keyboard.append([show_reviews])
        buttons_keyboard.append([leav_review])
        avg_reiting = 0
        for review in reviews:
            avg_reiting += review.review_rating
        if len(reviews) != 0:
            avg_reiting = avg_reiting/len(reviews)
        msg += f'Рейтинг: {round(avg_reiting, 1)}⭐️'
    print(buttons_keyboard)
    await context.bot.edit_message_text(chat_id='@PSPROF', message_id=master_record.msg_id,
                                        text=msg, reply_markup=InlineKeyboardMarkup(buttons_keyboard), parse_mode='HTML')

    return
