import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# መረጃዎች
TOKEN = "8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII"
API_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

# AI ቅንብር
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

logging.basicConfig(level=logging.INFO)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text
        # ለተጠቃሚው መልስ ማመንጨት
        response = model.generate_content(user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        # ስህተት ካለ እዚህ ጋር ይነግረናል
        await update.message.reply_text(f"⚠️ ስህተት፡ {str(e)}")

if __name__ == '__main__':
    # ቦቱን በቀጥታ ማስነሳት (ያለ Flask)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    
    print("ቦቱ እየሰራ ነው...")
    app.run_polling()
