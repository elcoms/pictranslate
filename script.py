from dotenv import load_dotenv
from random import randint
from telegram.ext import Updater, CommandHandler
from googleapiclient.discovery import build
from google_images_download import google_images_download
from os import getenv, listdir, path
from tempfile import TemporaryDirectory

load_dotenv(dotenv_path='.env')

service = build('translate', 'v2', developerKey=getenv('GOOGLE_API_KEY'))


def start(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id,
                  text="Send me some weird characters.")


def translateOnly(bot, update):
  try:
    text = update.message["text"].split(' ', 1)
    response = service.translations().list(
      target='en',
      q=' '.join(text[1:])
    ).execute()
  except Exception as e:
    print(e)

  bot.sendMessage(chat_id=update.message.chat_id,
                  text=response['translations'][0]['translatedText'])


def pictranslate(bot, update):
  try:
    text = update.message["text"].split(' ', 1)
    response = service.translations().list(
      target='en',
      q=' '.join(text[1:])
    ).execute()
  except Exception as e:
    print(e)

  try:
    imageClient = google_images_download.googleimagesdownload()
    keywords = response['translations'][0]['translatedText']

    with TemporaryDirectory() as temp_dir: 
      imageClient.download({
        'keywords': keywords,
        'limit': 20,
        'print_urls': True,
        'output_directory': temp_dir
      })

      images_dir = path.join(temp_dir, keywords)
      files = listdir(images_dir)
      chosen_photo = files[randint(0, len(files) - 1)]

      bot.sendPhoto(chat_id=update.message.chat_id, photo=open(path.join(images_dir, chosen_photo), 'rb'),
                caption=response['translations'][0]['translatedText'])
  except Exception as e:
    print(e)


updater = Updater(token=getenv('TELEGRAM_BOT_TOKEN'))
start_handler = CommandHandler('start', start)
translate_handler = CommandHandler('translate', translateOnly)
pictranslate_handler = CommandHandler('pictranslate', pictranslate)

dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(pictranslate_handler)
dispatcher.add_handler(translate_handler)

updater.start_polling(timeout=10)
