import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# በቀጥታ Token እና Key እዚህ ጋር እናስገባለን
BOT_TOKEN = "8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII"
GEMINI_API_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

genai.configure(api_key=GEMINI_API_KEY)
# ሞዴሉን ወደ አዲሱ 'gemini-1.5-flash' ብንቀይረው ፈጣን ነው
model = genai.GenerativeModel("gemini-1.5-flash")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ ስህተት፡ {str(e)}")

app = Flask('')

@app.route('/')
def home():
    return "AI Bot Running!"

def run():
    # Render የሚጠቀመው ፖርት 10000 ወይም ከ Environment Variable የሚመጣ ነው
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
    print("AI Bot Started...")
    # ቦቱን እናስጀምራለን
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling()
