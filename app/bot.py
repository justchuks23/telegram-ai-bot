from telegram.ext import Application
from app.config import BOT_TOKEN

def create_bot():
    return Application.builder().token(BOT_TOKEN).build()
