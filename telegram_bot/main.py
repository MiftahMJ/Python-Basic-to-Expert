import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Dictionary to store user data
user_data = {}

# A simple list of videos and codes (for demonstration purposes)
videos = [
    {"url": "https://www.youtube.com/watch?v=example1", "code": "CODE123"},
    {"url": "https://www.youtube.com/watch?v=example2", "code": "CODE456"}
]

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id

    if chat_id not in user_data:
        user_data[chat_id] = {'tokens': 0}

    await update.message.reply_text(
        'Welcome! Watch videos to earn tokens. Type /watch to get a video link.'
    )

# Command to provide a video link
async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if chat_id not in user_data:
        user_data[chat_id] = {'tokens': 0}

    # Choose a random video
    video = random.choice(videos)
    context.user_data['current_video'] = video

    await update.message.reply_text(
        f'Watch this video: {video["url"]}\nEnter the code at the end to earn tokens.'
    )

# Message handler to validate the code
async def validate_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    code_entered = update.message.text.strip()

    if 'current_video' in context.user_data:
        correct_code = context.user_data['current_video']['code']

        if code_entered == correct_code:
            user_data[chat_id]['tokens'] += 10  # Reward tokens
            await update.message.reply_text(f'Correct! You have earned 10 tokens. Total tokens: {user_data[chat_id]["tokens"]}')
        else:
            await update.message.reply_text('Incorrect code. Please try again.')
    else:
        await update.message.reply_text('Please watch a video first by typing /watch.')

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    # Replace 'YOUR_API_TOKEN' with your bot's API token
    application = ApplicationBuilder().token("YOUR_API_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("watch", watch))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validate_code))

    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
