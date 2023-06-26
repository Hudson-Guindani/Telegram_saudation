import telebot
import datetime

bot = telebot.TeleBot('token')

users = {}

characters_to_replace = ['@', '#', '$', ',', '.', '!', '?']

ignore = ('obrigado', 'obrigada', 'brigado', 'brigadoo', 'brigadooo', 'brigadão', 'obg',
          'valeu', 'valeuu', 'valeuuu', 'vlw', 'ok',  'beleza', 'belezinha', 'blz')

# People that answer requests
entidades = ('people_id')

retorno = ('Percebi que não houve menção ao setor responsável em sua mensagem. '
           'Por favor, não esqueça de mencioná-lo abaixo para que sua solicitação '
           'seja atendida com mais agilidade. Obrigado!')

print('Bot Saudação trabalhando...')


def identify_user(message):
    global users
    current_time = datetime.datetime.now()
    expired_users = [user_id for user_id, time in users.items() if current_time - time > datetime.timedelta(minutes=10)]
    for user_id in expired_users:
        del users[user_id]
    user_id = message.from_user.id
    message_time = datetime.datetime.fromtimestamp(message.date)
    return user_id, message_time


@bot.message_handler(content_types=["photo"])
def process_photo(message):
    user_id, message_time = identify_user(message)
    # verify if the message is a photo, has a mention and that is in the list entidades
    if user_id not in users and message.from_user.username not in entidades:
        if message.caption is not None:
            caption_words = message.caption.split()
            for word in caption_words:
                for char in characters_to_replace:
                    word = word.replace(char, '')
                if word in entidades:
                    users[user_id] = message_time
                    break
            else:
                bot.reply_to(message, retorno)
                users[user_id] = message_time
        else:
            bot.reply_to(message, retorno)
            users[user_id] = message_time


@bot.message_handler(content_types=["document"])
def process_photo(message):
    user_id, message_time = identify_user(message)
    # verify if the message is a document, has a mention and that is in the list entidades
    if user_id not in users and message.from_user.username not in entidades:
        if message.caption is not None:
            caption_words = message.caption.split()
            for word in caption_words:
                for char in characters_to_replace:
                    word = word.replace(char, '')
                if word in entidades:
                    users[user_id] = message_time
                    break
            else:
                bot.reply_to(message, retorno)
                users[user_id] = message_time
        else:
            bot.reply_to(message, retorno)
            users[user_id] = message_time


@bot.message_handler(func=lambda message: message.from_user.username not in entidades)
def process_message(message):
    user_id, message_time = identify_user(message)
    if user_id not in users:
        # verify if the message has a mention and that is in the list entidades
        if message.entities is not None:
            entities = message.text.split()
            for word in entities:
                for char in characters_to_replace:
                    word = word.replace(char, '')
                if word in entidades:
                    users[user_id] = message_time
                    break
            else:
                bot.reply_to(message, retorno)
                users[user_id] = message_time
        else:
            if any(palavra in message.text.lower() for palavra in ignore):
                text = message.text.lower()
                for char in characters_to_replace:
                    text = text.replace(char, '')
                    pass
            else:
                bot.reply_to(message, retorno)
                users[user_id] = message_time


bot.infinity_polling()

print('Encerrado')
