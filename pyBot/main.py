
"""

Задание

Напишите Telegram-бота, в котором будет реализован следующий функционал:

        1. Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
        2. При написании бота необходимо использовать библиотеку pytelegrambotapi.
        3. Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты,
         в которой надо узнать цену первой валюты> <количество первой валюты>.
        4. При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
        5. При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.
        6. Для получения курса валют необходимо использовать API и отправлять к нему запросы с помощью библиотеки Requests.
        7. Для парсинга полученных ответов использовать библиотеку JSON.
        8. При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число)
         вызывать собственно написанное исключение APIException с текстом пояснения ошибки.
        9. Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
        10. Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента и возвращает нужную сумму в валюте:
            имя валюты, цену на которую надо узнать, — base;
            имя валюты, цену в которой надо узнать, — quote;
            количество переводимой валюты — amount.
        11. Токен Telegram-бота хранить в специальном конфиге (можно использовать .py файл).
        12. Все классы спрятать в файле extensions.py.


"""
import telebot
from config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)




# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = " Чтобы начать работу введите комманду в следующем формате: \n<имя валюты>  <в какую валюту перевести>  " \
           "<количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


# Обрабатывается все все сообщения, содержащие команду '/values'
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i, key in enumerate(keys.keys()):
        text += f'\n{i+1}) {key}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        total_base = Converter.get_price(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        quote, base, amount = values
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        # text = f'Цена {amount} {quote} в {base} - {total_base*amount}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True, interval=0)



