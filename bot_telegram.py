# bot_telegram.py

import os
from dotenv import load_dotenv
from sqlalchemy import text
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from app.db.base import Base, engine

from app.ia.motor import procesar

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
RESET = os.getenv("RESET")

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
    
    if RESET == "si" :
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            conn.execute(text("DROP TABLE IF EXISTS usuario, frente, mensaje, recuerdo, entrada_diaria;"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    Base.metadata.create_all(bind=engine)

    print("🤖 Sofía está escuchando en Telegram...")
    app.run_polling()
