import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Render Port Error እንዳያሳይ
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), HealthCheck).serve_forever()

# መረጃዎች
TOKEN = "8604780681:AAH4tnRnMAk-gahwahZfsxMIe0oQcQNKqII"
genai.configure(api_key="AIzaSyBAt_zIJ1DqE0W3KrPjpp0uRIxHxn2TCF0")
model = genai.GenerativeModel('gemini-pro')

async def start(update, context):
    await update.message.reply_text("ሰላም! ቦቱ ሰርቷል!")

async def chat(update, context):
    try:
        res = model.generate_content(update.message.text)
        await update.message.reply_text(res.text)
    except:
        await update.message.reply_text("ስህተት አለ።")

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
    app.run_polling()
