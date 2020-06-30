import config
import os
import telebot
import validators
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from io import BytesIO
from PIL import Image

bot = telebot.TeleBot(config.token)


def do_screenshot(username, date, url):
    """ Script  """
    # init driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # use manager
    with driver:
        driver.get(url)

        img_li = []
        offset = 0

        height = driver.execute_script('return Math.max('
                                       'document.documentElement.clientHeight, '
                                       'window.innerHeight);')

        max_window_height = driver.execute_script('return Math.max('
                                                  'document.body.scrollHeight, '
                                                  'document.body.offsetHeight, '
                                                  'document.documentElement.clientHeight, '
                                                  'document.documentElement.scrollHeight, '
                                                  'document.documentElement.offsetHeight);')
        # set width
        driver.set_window_size(1980, height)
        # start to add parts of height
        while offset < max_window_height:
            # Scroll to height
            driver.execute_script(f'window.scrollTo(0, {offset});')
            img = Image.open(BytesIO((driver.get_screenshot_as_png())))
            print(img.size)
            img_li.append(img)
            offset += height

        # Stitch image into one
        # Set up the full screen frame
        img_frame_height = sum([img_frag.size[1] for img_frag in img_li])
        img_frame = Image.new('RGB', (img_li[0].size[0], img_frame_height))

        offset = 0
        for img_frag in img_li:
            img_frame.paste(img_frag, (0, offset))
            offset += img_frag.size[1]
        img_frame.save(os.path.join('media', f'{username}.{date}.png'))


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    """ Start , help block"""
    bot.send_message(message.chat.id, 'Hello, I can give you screenshot, just give me link')


@bot.message_handler(content_types=['text'])
def send_text(message):
    """ Main answer block"""

    if validators.url(message.text):
        do_screenshot(message.from_user.first_name, message.date, message.text)
        with open(f'media/{message.from_user.first_name}.{message.date}.png', 'rb') as photo:
            # use file sending instead of photo because the file is too large
            bot.send_document(message.chat.id, data=photo)
    else:
        bot.send_message(message.chat.id, "Please input correct URL. Thank's you")


if __name__ == '__main__':
    bot.polling()
