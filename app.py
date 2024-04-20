import telebot
from config import token, keys
from extensions import APIException, Exchange

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = (f'Привет {message.from_user.first_name} {message.from_user.last_name}!'
            '\nЯ Бот-Конвертер валют и я могу:'
            '\n- Произвести конвертацию валюты через команду <имя валюты> <в какую валюту перевести>'
            '<количество переводимой валюты>'
            '\nПример: рубль евро 1000'
            '\n- Показать список доступных валют через команду /values'
            '\n- Напомнить что я могу - через команду /help')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    text = ('Чтобы произвести конвертацию, введите команду боту в следующем формате:'
            '\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>'
            '\nПример: рубль евро 1000'
            '\nЧтобы увидеть список всех доступных валют, введите команду /values')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')

        if len(values_) != 3:
            raise APIException('Введите команду или 3 параметра')

        quote, base, amount = values_
        quote = quote.lower()
        base = base.lower()
        total_base = Exchange.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
