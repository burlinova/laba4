import requests
import telebot
from io import BytesIO 
import random

bot = telebot.TeleBot("6709487661:AAHVQBLeuhQ8AXLFhS_5KgZPGYHneKgdh0M") 

channel_id = 428515560



def meme(channel_id):
    client_id = 'wa6mcWkE2xQLi0PCLIzZfg' 
    channel_id = channel_id
    client_secret = 'rg6DVa-9C8vgk5pLbDx3eOZPRPryCw' 
    user_agent = 'IlichSameAsBobAgent (by /u/Hopeful_Hearing_3354)'

    url = 'https://www.reddit.com/r/memes/new.json?limit=100'

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    headers = {'User-Agent': user_agent}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        print("Ответ с кучей картинок получен, пытаемся получить картинку")
        data = response.json()
        posts = data['data']['children'] 

        random_post = random.choice(posts)
        image_url = random_post['data']['url'] 

        if any(extension in image_url.lower() for extension in
               ['.jpg', '.jpeg', '.png', '.gif']): 
            print(f"Ссылка на картинку: {image_url}")
            image_response = requests.get(image_url, headers=headers, auth=auth)
            print("Получили картинку!")
            image_data = BytesIO(
                image_response.content) 
            bot.send_photo(chat_id=channel_id, photo=image_data)
            print("Картинка отправлена в бота")
            return True
        else:
            print(f"Неправильный url картинки :( {image_url}")
            return False
    else:
        print(f"Ошибка {response.status_code}!")
        return False


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    channel_id = message.chat.id
    if message.text == "Привет" or message.text == "Мем!":
        bot.send_message(message.from_user.id, "Я тебя понял, жди мем")
        isSuccess = meme(channel_id)
        while not (isSuccess): isSuccess = meme()
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши 'Привет' или 'Мем!' ")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)




