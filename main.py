import os
import google.generativeai as genai
from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --------- KEYS ----------
BOT_TOKEN = os.getenv("8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII")
GEMINI_API_KEY = os.getenv("AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo")

# --------- GEMINI ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# --------- AI CHAT ----------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = model.generate_content(user_text)
    reply = response.text

    await update.message.reply_text(reply)

# --------- TELEGRAM ----------
bot = ApplicationBuilder().token(BOT_TOKEN).build()
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# --------- FLASK (UPTIME) ----------
app = Flask('')

@app.route('/')
def home():
    return "AI Bot Running!"

def run():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --------- START ----------
keep_alive()
print("AI Bot Started...")
bot.run_polling()
