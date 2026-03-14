import os
import asyncio
import logging
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Logging setup (ስህተቶችን በ Render Log ላይ ለማየት)
logging.basicConfig(level=logging.INFO)

# API Keys
TELEGRAM_TOKEN = "8604780681:AAH0H8zQBWUd_iz_M9Mpdg5Fr9ftvqIiMHk"
GEMINI_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- Render Web Service Health Check (Flask) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    # Render የሚሰጠውን Port መጠቀም (ካልተሰጠ 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Handlers ---

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም አማን! ቦቱ አሁን ዝግጁ ነው። የሚሰማህን ነገር አውራኝ።")

@dp.message()
async def chat_handler(message: types.Message):
    if not message.text:
        return
    
    try:
        # ለ Gemini መልዕክቱን መላክ
        response = model.generate_content(message.text)
        
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("ይቅርታ፣ ምላሽ ማመንጨት አልቻልኩም።")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("ትንሽ ስህተት አጋጥሞኛል። ቆይተህ ሞክር።")

async def main():
    # Flaskን በሌላ Thread ማስጀመር (Render እንዳይዘጋው)
    threading.Thread(target=run_flask, daemon=True).start()
    
    logging.info("ቦቱ ሥራ ጀምሯል...")
    # ቦቱ መልእክቶችን መቀበል እንዲጀምር (Polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("ቦቱ ቆሟል!")
