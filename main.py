import os
import asyncio
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# API Keys
TELEGRAM_TOKEN = "8604780681:AAH0H8zQBWUd_iz_M9Mpdg5Fr9ftvqIiMHk"
GEMINI_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- Render Port Error ለማስቀረት (Flask) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
# ----------------------------------------

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም! አሁን ቦቱ ዝግጁ ነው። ምን ላግዝህ?")

@dp.message()
async def chat_handler(message: types.Message):
    if not message.text: return
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # Flaskን በሌላ Thread ማስጀመር
    threading.Thread(target=run_flask, daemon=True).start()
    # ቦቱን ማስጀመር
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
