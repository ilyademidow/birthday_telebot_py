import time
import os
from lang.ru import msg_array
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import date, datetime
import pickledb
import schedule


def handle_message(update, context):
    message = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"You said: {message}")


def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="This is a simple Telegram bot.")


def add_bd(update, context):
    entity = update.message.text.replace("/addbd", "").split("-")
    try:
        # Verify if command format correct
        if len(entity) < 2 or entity[0].strip() == "" or '@' not in entity[0]:
            raise Exception('Wrong add format')
        if entity[1].strip() == "" or len(entity[1].strip()) != 5 or len(entity[1].strip().split(".")) != 2:
            raise Exception('Wrong add format')
        if not is_valid_date(entity[1].strip()):
            raise ValueError

        hero_model = {'name': entity[0].strip().upper(), 'date': entity[1].strip()}

        if db.exists(hero_model['name']):
            new_hero_list = db.getall().mapping
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{msg_array['add_existed_item_msg']} {new_hero_list}")
        else:
            db.set(hero_model['name'], hero_model['date'])
            new_hero_list = db.getall().mapping
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{msg_array['suc_new_list_msg']} {new_hero_list}")
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{msg_array['wrong_date_msg']}")
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{msg_array['wrong_add_format_msg']}")


def get_bd_list(update, context):
    result = db.getall()
    logging.info(result.mapping)
    if len(result) > 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{result.mapping}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg_array['empty_list_msg'])


def del_bd(update, context):
    hero_name = update.message.text.replace("/delbd", "").strip().upper()
    if db.exists(hero_name):
        db.rem(hero_name)
        result = db.getall().mapping
        logging.info(result)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{msg_array['suc_new_list_msg']} {result}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{msg_array['no_such_hero_msg']} {db.getall().mapping}")


def check_date():
    # Get today's date
    today = date.today().strftime("%d.%m")

    # Check if today's date matches any of the keys in the database
    for key in db.getall():
        if today == db.get(key):
            logging.info(f"Congrats HP {key}")
            updater.bot.send_message(chat_id=os.environ['EFFECTIVE_CHAT_ID'], text=f"{key} {msg_array['congrats_msg']}")


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%d.%m")
        return True
    except ValueError:
        return False


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

db = pickledb.load('bd-tg-bot-database.db', True)

congrat_time = '08:00'
if os.environ.get('CONGRAT_TIME'):
    congrat_time = os.environ['CONGRAT_TIME']
# Schedule the job to run every day at 8 AM
schedule.every().day.at(congrat_time).do(check_date)


dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('addbd', add_bd))
dispatcher.add_handler(CommandHandler('delbd', del_bd))
dispatcher.add_handler(CommandHandler('listbd', get_bd_list))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))


def main() -> None:
    logging.info("starting...")
    updater.start_polling()
    logging.info("started")

    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == "__main__":
    main()
