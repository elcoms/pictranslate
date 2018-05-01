from configparser import RawConfigParser
from random import randint
from telegram.ext import Updater, CommandHandler
from google.cloud import translate
from google_images_download import google_images_download

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Send me some weird characters.")

def translateOnly(bot, update):
    try:
        client = translate.Client.from_service_account_json("C:\Python27\PicTranslate-0f848a4ac055.json")
        text = update.message["text"].split(' ', 1)
        result = client.translate(text[1])
    except Exception as e:
        print(e)

    bot.sendMessage(chat_id=update.message.chat_id, text=result["translatedText"])


def pictranslate(bot, update):
    try:
        client = translate.Client.from_service_account_json("C:\Python27\PicTranslate-0f848a4ac055.json")
        text = update.message["text"].split(' ', 1)
        result = client.translate(text[1])
    except Exception as e:
        print(e)

    try:
        imageClient = google_images_download.googleimagesdownload()
        imageURL = imageClient.download(
            {
                "keywords": result["translatedText"],
                "limit": randint(1,21),
                "print_urls": True
            })
    except Exception as e:
        print(e)

    bot.sendPhoto(chat_id=update.message.chat_id, photo=imageURL, caption=result["translatedText"])

def getToken():
    config = RawConfigParser()
    config.read("config.ini")
    return config.get('Token', 'telegram')

updater = Updater(token=getToken())
start_handler = CommandHandler('start', start)
translate_handler = CommandHandler('translate', translateOnly)
pictranslate_handler = CommandHandler('pictranslate', pictranslate)

dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(pictranslate_handler)
dispatcher.add_handler(translate_handler)

updater.start_polling(timeout=10)