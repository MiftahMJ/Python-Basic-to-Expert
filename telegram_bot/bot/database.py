# bot/database.py

import sqlite3
from .config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            token_balance INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            video_id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_video(url, code):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO videos (url, code) VALUES (?, ?)', (url, code))
    conn.commit()
    conn.close()

def get_random_video():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT url, code FROM videos ORDER BY RANDOM() LIMIT 1')
    video = cursor.fetchone()
    conn.close()
    return video

def update_user_tokens(user_id, tokens):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, token_balance) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET token_balance = token_balance + ?
    ''', (user_id, tokens, tokens))
    conn.commit()
    conn.close()
