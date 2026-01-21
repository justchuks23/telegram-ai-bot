from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters

from app.bot import create_bot
from app.handler import start, ai_chat
from app.config import WEBHOOK_URL

from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
bot_app = create_bot()

# Register handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))

@app.on_event("startup")
async def startup():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def shutdown():
    await bot_app.shutdown()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "FastAPI server running"}

@app.get("/test-ai")
async def test_ai(prompt: str):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "reply": response.output_text
    }