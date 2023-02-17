from telegram.ext import ContextTypes
from telegram import Update
from database.db_bilder import session, Review


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
