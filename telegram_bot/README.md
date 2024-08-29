# Telegram Bot Project

This project is a Telegram bot that rewards users for watching YouTube videos.

## Setup Instructions

1. Install Python 3.8 or later.
2. Create a virtual environment and activate it:
    ```
    python -m venv telegram_bot_env
    source telegram_bot_env/bin/activate  # On Windows use `telegram_bot_env\Scripts\activate`
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Configure the bot by editing `config.py` and adding your Telegram bot token.
5. Run the bot:
    ```
    python -m bot.bot
    ```

## How It Works

1. Users interact with the bot using the `/start` and `/watch` commands.
2. The bot sends a link to a YouTube video and asks users to enter a code shown at the end.
3. Upon entering the correct code, users earn tokens.

## Future Enhancements

- Adding a leaderboard to show top token earners.
- Adding more videos and codes dynamically.
