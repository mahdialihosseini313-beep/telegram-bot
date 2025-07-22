import os
import telebot
from flask import Flask, request

API_TOKEN = '7524757973:AAHo-nPJXiTryoIumR2EnLsacxS2OSKMtNU'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# دیکشنری فایل‌ها (عدد: نام فایل)
files = {
    '7': 'file7.mp3',
    '8': 'file8.mp4',
    '9': 'photo9.jpg',
    '10': 'document10.pdf',
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! عدد موردنظر آهنگ یا فایل رو برام بفرست.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    if user_input in files:
        file_path = f'files/{files[user_input]}'
        ext = file_path.split('.')[-1]
        with open(file_path, 'rb') as f:
            if ext in ['mp3', 'wav']:
                bot.send_audio(message.chat.id, f)
            elif ext in ['mp4', 'mov']:
                bot.send_video(message.chat.id, f)
            elif ext in ['jpg', 'jpeg', 'png']:
                bot.send_photo(message.chat.id, f)
            else:
                bot.send_document(message.chat.id, f)
    else:
        bot.reply_to(message, "عدد معتبر وارد کن :)")

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('RENDER_EXTERNAL_URL') + API_TOKEN)
    return 'Webhook set!', 200

if __name__ == '__main__':
    app.run(debug=True)
