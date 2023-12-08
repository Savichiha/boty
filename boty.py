from emoji import emojize
from glob import glob
import logging
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import setting

logging.basicConfig(filename='boty.log', level=logging.INFO, encoding="utf-8")


def greet_user(update, context):
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет! {context.user_data['emoji']}")
    #print(update) - данные о юзере

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text 
    print(text)
    update.message.reply_text(text)

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(setting.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    else:
        return user_data['emoji']   

def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        messege = f'Твое число {user_number}, я загадал {bot_number}, - твоя победа!'
    elif user_number == bot_number:
        messege = f'Твое число {user_number}, я загадал {bot_number}, - ничья!'
    else:
        messege = f'Твое число {user_number}, я загадал {bot_number}, - моя победа!'
    return messege

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = f'ваще число {play_random_numbers(user_number)}'
        except (TypeError, ValueError):
            message = 'Введите целое число!'    
    else:
        message = "Введи число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id = chat_id, photo=open(cat_photo_filename, 'rb'))

def main():
    mybot = Updater(setting.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler('cat', send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()   