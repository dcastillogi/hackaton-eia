import telebot

#Conexión con el bot de Telegram
TOKEN = '7115293919:AAHnu0ZEkVns7ur7IGL1u9j33WAn7HzXPhg'
bot = telebot.TeleBot(TOKEN)

#Comandos
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! ¿Como estaás prro?")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "¡Hola! ¿Como puedo ayudarte prro?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

#Iniciar el bot
bot.polling(none_stop=True)
