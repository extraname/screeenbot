import config
import os
import telebot
import validators
from screeninfo import get_monitors
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

bot = telebot.TeleBot(config.token)


def do_screenshot(username, date, url):
    """ Script block """
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)
    for size in get_monitors():
        driver.set_window_size(size.width, size.height)
        el = driver.find_element_by_tag_name('body')
        el.screenshot(filename=os.path.join('media', f'{username}.{date}.png'))
        driver.quit()


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello, I can give you screenshot, just give me link')


# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     """ Main answer block"""
#     if message.text.startswith('http://') or message.text.startswith('https://'):
#         if validators.url(message.text):
#             do_screenshot(message.from_user.first_name, message.date, message.text)
#             with open(f'media/{message.from_user.first_name}.{message.date}.png', 'rb') as photo:
#                 bot.send_photo(message.chat.id, photo=photo)
#         else:
#             bot.send_message(message.chat.id, 'Url is not valid')
#     else:
#         bot.send_message(message.chat.id, 'Please, input correct URL')


@bot.message_handler(content_types=['text'])
def send_text(message):
    """ Main answer block"""

    if validators.url(message.text):
        do_screenshot(message.from_user.first_name, message.date, message.text)
        with open(f'media/{message.from_user.first_name}.{message.date}.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo=photo)
    else:
        bot.send_message(message.chat.id, "Please input correct URL. Thank's you")


if __name__ == '__main__':
    bot.polling()
