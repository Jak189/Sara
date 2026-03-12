import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# 1. ለ Render የሚሆን ትንሽ ሰርቨር (Port Error እንዳይመጣ)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 2. ያንተ መረጃዎች
TELEGRAM_TOKEN = '8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII'
GEMINI_API_KEY = 'AIzaSyBAt_zIJ1DqE0W3KrPjpp0uRIxHxn2TCF0'

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! ቦቱ በ Web Service ላይ ስራ ጀምሯል።")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("ይቅርታ፣ ስህተት አጋጥሞኛል።")

if __name__ == '__main__':
    # ሰርቨሩን በሌላ Thread ማስነሳት
    threading.Thread(target=run_health_check, daemon=True).start()
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("ቦቱ እየሰራ ነው...")
    application.run_polling()
