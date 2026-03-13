import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Logging setup
logging.basicConfig(level=logging.INFO)

# API Keys
TELEGRAM_TOKEN = "8604780681:AAH0H8zQBWUd_iz_M9Mpdg5Fr9ftvqIiMHk"
GEMINI_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("ሰላም! እኔ በ AI የታገዝኩ ቦት ነኝ። ምን ላግዝህ?")

@dp.message()
async def chat_handler(message: types.Message):
    if not message.text:
        return
    try:
        # ለ Gemini መልዕክቱን መላክ
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("ይቅርታ፣ አሁን ላይ ምላሽ መስጠት አልቻልኩም። ቆይተው ይሞክሩ።")

async def main():
    logging.info("ቦቱ ሥራ ጀምሯል...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("ቦቱ ቆሟል!")
