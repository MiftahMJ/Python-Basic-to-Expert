# bot/handlers.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from .database import get_random_video, update_user_tokens
from .utils import read_template

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_message = read_template('templates/messages/welcome.txt')
    await update.message.reply_text(welcome_message.format(first_name=user.first_name))

async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = get_random_video()
    if video:
        context.user_data['current_video'] = video
        await update.message.reply_text(f'Watch this video: {video[0]}\nEnter the code shown at the end to earn tokens.')
    else:
        await update.message.reply_text('No videos available at the moment.')

async def validate_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    code_entered = update.message.text.strip()

    if 'current_video' in context.user_data:
        correct_code = context.user_data['current_video'][1]
        if code_entered == correct_code:
            update_user_tokens(user.id, 10)  # Reward tokens
            await update.message.reply_text(f'Correct! You have earned 10 tokens.')
        else:
            await update.message.reply_text('Incorrect code. Please try again.')
    else:
        await update.message.reply_text('Please watch a video first by typing /watch.')
