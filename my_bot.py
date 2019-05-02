import telebot
import deadline
import datetime as dt
from main_table import *


bot = telebot.TeleBot("834326878:AAHUik-zWIGZ0s0AY0WR0juKOgImqiCitN0")
deadline_type = ''
deadline_subject = ''
deadline_name = ''
deadline_estimate_time = ''
deadline_dead_time = ''
deadline_status = 'Unfinished'

database = Database()


def get_type(message):
    global deadline_type
    try:
        deadline_type = int(message.text)
        if deadline_type == 1:
            deadline_type = 'home'
        else:
            deadline_type = 'study'
        bot.send_message(message.chat.id, "К какому предмету "
                                          "относится задание?")
        bot.register_next_step_handler(message, get_subject)
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_type)


def get_subject(message):
    global deadline_subject
    deadline_subject = message.text
    bot.send_message(message.chat.id, "Как назвать задание?")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global deadline_name
    deadline_name = message.text
    bot.send_message(message.chat.id, "Сколько часов понадобится на выполнение"
                                      " задания?")
    bot.register_next_step_handler(message, get_estimate_time)


def get_estimate_time(message):
    global deadline_estimate_time
    try:
        deadline_estimate_time = int(message.text)
        bot.send_message(message.chat.id, "Сколько часов осталось до "
                                          "дедлайна по заданию?")
        bot.register_next_step_handler(message, get_finish_time)
    except (TypeError, ValueError):
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_estimate_time)


def get_finish_time(message):
    global deadline_dead_time
    global deadline_estimate_time
    try:
        deadline_hours = int(message.text)
        cur_datetime = dt.datetime.now()
        deadline_dead_time = dt.datetime(cur_datetime.year, cur_datetime.month,
                                         cur_datetime.day,
                                         cur_datetime.hour + deadline_hours,
                                         cur_datetime.minute)

        print("Estimate: ", deadline_estimate_time)
        print("Finish: ", deadline_dead_time)
        bot.send_message(message.chat.id, "Я добавил) Напиши мне что-нибудь,"
                                      " чтобы я закончил")
        bot.register_next_step_handler(message, insert_deadline)

    except (TypeError, ValueError):
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_finish_time)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, я буду помогать тебе! "
                                      "Я могу хранить твои задания. "
                                      "Чтобы добавить новое, введи /insert, а "
                                      "чтобы увидеть добавленные, введи /print")


@bot.message_handler(commands=['insert'])
def get_deadline(message):
    bot.send_message(message.chat.id, 'К какой категории относится задание? '
                                      'Введи 1, если относится к дому и 2, '
                                      'если к учебе')
    bot.register_next_step_handler(message, get_type)


def insert_deadline(message):
    global deadline_type
    global deadline_subject
    global deadline_name
    global deadline_estimate_time
    global deadline_dead_time
    global deadline_status
    global database
    new_deadline = deadline.Deadline(deadline_type, deadline_subject,
                                     deadline_name, deadline_estimate_time,
                                     deadline_dead_time, deadline_status)
    database.insert_deadline(message.chat.id, new_deadline)


@bot.message_handler(commands=['print'])
def get_all_deadlines(message):
    global database
    deadlines_list = database.get_all_deadlines(message.chat.id)
    bot.send_message(message.chat.id, 'У вас запланированы следующие дела:')
    for deadline in deadlines_list:
        bot.send_message(message.chat.id,
                         'Задание "{}" из категории "{}" , '
                         'которое займет {} часов. При этом дата '
                         'окончания:{}'.format(deadline[0], deadline[1],
                                               deadline[2], deadline[3]))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, message.text)


bot.polling()
