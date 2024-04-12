from dotenv import load_dotenv
import os
from lib.db import get_user


load_dotenv()

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from lib.process import run

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtener id del usuario
    user_id = update.effective_user.id
    # Verificar si el usuario ya se encuentra registrado
    user = get_user(user_id)
    if user:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"¡Hola {user['name']}! 👋. Ingresa el tema del que quieres escuchar un podcast:")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hey 👋, parece que aún no te has registrado., realizalo en la siguiente página:", parse_mode="markdown", reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "Registrarme",
                        "url": "https://croissantai.vercel.app/register?telegram_id=" + str(user_id) + "&chat_id=" + str(update.effective_chat.id),
                    }
                ]
            ]
        })
        
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Verificar si el usuario ya se encuentra registrado
    user = get_user(user_id)
    # get the message that the user sent
    msg = update.message.text
    if user:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Espera un momento por favor, estamos generando el podcast") 
        path = run(str(msg), str(user_id))
        # read file input
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=path)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hey 👋, parece que aún no te has registrado., realizalo en la siguiente página:", parse_mode="markdown", reply_markup={
            "inline_keyboard": [
                [
                    {
                        "text": "Registrarme",
                        "url": "https://croissantai.vercel.app/register?telegram_id=" + str(user_id) + "&chat_id=" + str(update.effective_chat.id),
                    }
                ]
            ]
        })
    
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    start_handler = CommandHandler("start", start)
    anything_else_handler = MessageHandler(None, generate)

    application.add_handler(start_handler)
    application.add_handler(anything_else_handler)
    
    application.run_polling()