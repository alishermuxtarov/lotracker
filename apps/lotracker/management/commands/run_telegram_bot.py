import logging
import re

from django.core.management import base
from django.conf import settings

import telebot
from telebot.apihelper import ApiException
from authentication.models import User

telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(token=settings.TOKEN)
try:
    bot.remove_webhook()
except ApiException:
    pass


def validate_mobile(value):
    rule = re.compile(r'^(?:\+?998)?\d{9,13}$')
    if not rule.search(value):
        return False
    return True


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = telebot.types.KeyboardButton(text="Отправить номер", request_contact=True)
    keyboard.add(reg_button)
    msg = bot.send_message(
        message.chat.id,
        "Добро пожаловать!\nДля регистрации, необходимо ввести или отправить номер телефона",
        reply_markup=keyboard)
    bot.register_next_step_handler(msg, process_registration)


def process_registration(message):
    phone = message.contact.phone_number if hasattr(message.contact, 'phone_number') else message.text
    phone = '+{}'.format(phone.lstrip('+'))
    if not validate_mobile(phone):
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        reg_button = telebot.types.KeyboardButton(text="Отправить номер", request_contact=True)
        keyboard.add(reg_button)
        msg = bot.send_message(message.chat.id, "Неверно введен номер телефона!",reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_registration)
        return

    user = User.objects.filter(phone=phone)
    hide_keyboard = telebot.types.ReplyKeyboardRemove()
    if not user.exists():
        msg = bot.send_message(
            message.chat.id,
            "Вы не пользуетесь нашим приложением или веб-сайтом.\n"
            "Для того что бы получать уведомления, вам необходимо пройти регистрацию на сайте или в приложении, "
            "а так же задать фильтра, для отслеживания обновлений по ним. "
            "После того как вы выполните все необходимые действия, "
            "вы можете приступить к настройке бота набрав команду /start",
            reply_markup=hide_keyboard
        )
        bot.register_next_step_handler(msg, send_welcome)
        return
    msg = bot.send_message(
        message.chat.id,
        "Введите СМС код, который был выслан к вам на телефон",
        reply_markup=hide_keyboard)
    bot.register_next_step_handler(msg, process_sms, user.first().pk)


def process_sms(message, user_id):
    User.objects.filter(pk=user_id).update(telegram_uid=message.chat.id)

    bot.send_message(
        message.chat.id, 'Спасибо. Проверка прошла успешно.\n'
                         'Теперь вы будете получать уведомления по вашим фильтрам.')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith('/'):
        return send_welcome(message)
    bot.send_message(message.chat.id, 'Неизвестная команда!')


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling()
