import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Render Port ሰርቨር
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is online")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), HealthCheck).serve_forever()

# መረጃዎች (አዲሱን ቁልፍ እዚህ አስገብቼዋለሁ)
TOKEN = "8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII"
API_KEY = "AIzaSyB_2QVb9rSbS9SUQm-vHf5g4usf3lq5Pwo"

genai.configure(api_key=API_KEY)
# ሞዴሉን ወደ gemini-1.5-flash ቀይረነዋል
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update, context):
    await update.message.reply_text("ሰላም! አሁን ቦቱ ተስተካክሏል። መጠየቅ ትችላለህ።")

async def chat(update, context):
    try:
        user_input = update.message.text
        response = model.generate_content(user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ ስህተት፡ {str(e)}")

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    app.run_polling()
