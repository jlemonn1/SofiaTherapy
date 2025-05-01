# bot_telegram.py

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from app.db.base import Base, engine

from app.ia.motor import procesar

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Respuesta a cada mensaje de texto
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text

    respuesta = procesar(user_id, texto)
    await update.message.reply_text(respuesta)

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    Base.metadata.create_all(bind=engine)

    print("🤖 Sofía está escuchando en Telegram...")
    app.run_polling()
