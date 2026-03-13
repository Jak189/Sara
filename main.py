import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Render ላይ Port ስህተት እንዳይመጣ የሚረዳ ሰርቨር
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# መረጃዎች (የተቀየረው API Key እዚህ አለ)
TOKEN = "8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII"
API_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

logging.basicConfig(level=logging.INFO)

async def start(update, context):
    await update.message.reply_text("ሰላም! አዲሱ API Key ተቀይሯል። አሁን መጠየቅ ትችላለህ።")

async def chat(update, context):
    try:
        user_input = update.message.text
        response = model.generate_content(user_input)
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("ይቅርታ፣ AI መልስ ማመንጨት አልቻለም።")
    except Exception as e:
        # ስህተት ካለ በትክክል ምን እንደሆነ ይነግርሃል
        await update.message.reply_text(f"⚠️ ስህተት ተፈጥሯል፦ {str(e)}")

if __name__ == '__main__':
    # ሰርቨሩን ማስነሳት
    threading.Thread(target=run_server, daemon=True).start()
    
    # ቦቱን ማስነሳት
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    
    print("Bot is starting...")
    app.run_polling()
