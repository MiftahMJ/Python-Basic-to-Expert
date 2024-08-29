# bot/bot.py

import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .config import TELEGRAM_BOT_TOKEN
from .handlers import start, watch, validate_code
from .database import init_db

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    # Initialize the database
    init_db()

    # Create the application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("watch", watch))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validate_code))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
