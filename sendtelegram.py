import telegram

TOKEN = '1702826905:AAERhXq1iVv4u2mr-FS0LOMerzY731TA1gY'

def send_telegram_message(txt):
    bot = telegram.Bot(TOKEN)
    if bot.get_updates():
        chat_id = bot.get_updates()[-1].message.chat_id
        bot.send_message(chat_id,txt)
    else:
        print("Empty list. Please, chat with the bot")

def send_telegram_photo(pic):
    bot = telegram.Bot(TOKEN)
    if bot.get_updates():
        chat_id = bot.get_updates()[-1].message.chat_id
        bot.send_photo(chat_id,photo=open(pic, 'rb'))
    else:
        print("Empty list. Please, chat with the bot")

