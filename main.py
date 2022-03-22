import telebot
from telebot import types

#  5140658956:AAFNDhEPeZk6WIRGZMN5i6ic4bwmcXqppUs
name = ''
surname = ''
age = 0
bot = telebot.TeleBot("5140658956:AAFNDhEPeZk6WIRGZMN5i6ic4bwmcXqppUs")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Howdy, how are you doing?')


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Whats your surname?')
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Whats your age?')
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age
    if message.text.isdigit():
        age = int(message.text)
        question = 'Age: ' + str(age) + '\nName: ' + name + '\nSurname: ' + surname
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='yes', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='no', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Wrong input! Age should be a number, try again')
        bot.register_next_step_handler(message, reg_age)


@bot.message_handler(commands=['reg'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Hi, lets have a talk! Whats your name?')
    bot.register_next_step_handler(message, reg_name)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    if call.data=='yes':
        bot.send_message(call.message.chat.id, 'Nice to meet ya!')
    elif call.data=='no':
        bot.send_message(call.message.chat.id, 'Lets try again!')
        bot.send_message(call.message.chat.id, 'Hi, lets have a talk! Whats your name?')
        bot.register_next_step_handler(call.message, reg_name)


bot.polling()
