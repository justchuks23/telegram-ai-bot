from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = "You are a helpful AI assistant inside a Telegram bot."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm an AI-powered Telegram bot.\nAsk me anything!"
    )

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        ai_reply = response.output_text or "I couldn't generate a response."
        await update.message.reply_text(ai_reply)

    except Exception as e:
        print("OpenAI API error:", e)
        await update.message.reply_text("⚠️ AI error. Please try again later.")
