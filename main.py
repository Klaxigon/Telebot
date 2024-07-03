import telebot # type: ignore
from telebot import types # type: ignore
import logging
import time
import threading
from datetime import datetime

API_TOKEN = '//'

bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(level=logging.INFO)

def delete_message(chat_id, message_id, delay):
    time.sleep(delay)
    bot.delete_message(chat_id, message_id)

def log_user_data(user, user_id, timestamp):
    with open("user_data.txt", "a") as file:
        file.write(f"User: {user}, UserID: {user_id}, Timestamp: {timestamp}\n")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user.username or "NoUsername"
    user_id = message.from_user.id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_user_data(user, user_id, timestamp)

    markup = types.InlineKeyboardMarkup()
    yes_button = types.InlineKeyboardButton("Ja", callback_data="yes")
    no_button = types.InlineKeyboardButton("Nein", callback_data="no")
    markup.add(yes_button, no_button)
    sent_message = bot.reply_to(message, "Möchtest du auf eine Webseite weitergeleitet werden?", reply_markup=markup)

    threading.Thread(target=delete_message, args=(sent_message.chat.id, sent_message.message_id, 30)).start()

@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def handle_callback(call):
    if call.data == "yes":
        msg = bot.send_message(call.message.chat.id, "Hier ist der Link: [Soon](https://000101011.netlify.app/)", parse_mode='Markdown')
        threading.Thread(target=delete_message, args=(msg.chat.id, msg.message_id, 20)).start()
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Okay, keine Weiterleitung.")

if __name__ == "__main__":
    try:
        print("Bot läuft...")
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
