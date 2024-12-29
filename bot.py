import time, threading, schedule
from telebot import TeleBot

API_TOKEN = ''
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    bot.reply_to(message, f"Привет! Я бот {bot.get_me().first_name}!'напишите /help для просмотра функций ")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "/start-приветствие, /help-просмотр функций, /set <секунды> - начать таймер , /unset- закончить таймер")

def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
bot.polling()
