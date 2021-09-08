import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
from bs4 import BeautifulSoup
from os import getenv

token = getenv('token')

updater = Updater(
    token=token)

dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    """Sends a welcome message when calling the /start command

    Args:
        update: Contains the information of the current request
        context: CallbackContext
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hi human")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def medium_new(update, context):
    """Processes the update to send a url as a message when the
    getnew command is called

    Args:
        update: Contains the information of the current request
        context: CallbackContext
    """
    link = scrapping_medium()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=link)


start_handler = CommandHandler('getnew', medium_new)
dispatcher.add_handler(start_handler)

updater.start_polling()


def scrapping_medium():
    """Performs webscraping to the medium site to bring the
    latest news concerning the programming tag
    
    Return: The message sent by the bot to the chat with the
    command getnew
    """

    URL = 'https://medium.com/tag/programming'
    page = requests.get(URL)
    if (page.status_code == 200):
        try:
            soup = BeautifulSoup(page.content, 'html.parser')

            div_elements = soup.find(
                'div', {'class': 'hk l'})

            for elements in div_elements:
                link = elements['href']

            return link

        except BaseException:
            return '''Sorry, I am unable to deliver
                    the resource to you at this time.'''

    return 'At this moment medium is not available'
