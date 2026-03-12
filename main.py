import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# ያንተ መረጃዎች
TELEGRAM_TOKEN = '8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII'
GEMINI_API_KEY = 'AIzaSyBAt_zIJ1DqE0W3KrPjpp0uRIxHxn2TCF0'

# Gemini AI አቀማመጥ
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# ስህተቶችን ለመከታተል
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! የ AI ቦቱ ስራ ጀምሯል። የፈለግከውን ጠይቀኝ!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # ለ AI ጥያቄውን መላክ
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("ይቅርታ፣ መልስ ለማመንጨት ስሞክር ስህተት አጋጥሞኛል።")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("ቦቱ እየሰራ ነው...")
    application.run_polling()
