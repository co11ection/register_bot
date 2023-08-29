import telebot
import requests
from decouple import config

BOT_TOKEN = config('TOKEN')
API_BASE_URL = config('API_BASE_URL')

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для регистрации. Отправь мне /register чтобы начать.")

@bot.message_handler(commands=['register'])
def register(message):
    user_data[message.chat.id] = {'step': 'fullname'}
    bot.send_message(message.chat.id, "Пожалуйста, введите ФИО")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'fullname')
def process_fullname(message):
    user_data[message.chat.id]['fullname'] = message.text
    user_data[message.chat.id]['step'] = 'phone_number'
    bot.send_message(message.chat.id, "Теперь введите ваш номер телефона.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'phone_number')
def process_phone_number(message):
    user_data[message.chat.id]['phone_number'] = message.text
    user_data[message.chat.id]['step'] = 'email'
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш адрес электронной почты.")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'email')
def process_email(message):
    user_data[message.chat.id]['email'] = message.text
    user_data[message.chat.id]['step'] = 'password'
    bot.send_message(message.chat.id, "Пожалуйста, введите ваш пороль. Он должен состоять как минимум из 8 символов")
    
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'password')
def process_password(message):
    user_data[message.chat.id]['password'] = message.text

    data = {
        'full_name': user_data[message.chat.id]['fullname'],
        'phone_number': user_data[message.chat.id]['phone_number'],
        'email': user_data[message.chat.id]['email'],
        'password': user_data[message.chat.id]['password'],
    }
    response = requests.post(f'{API_BASE_URL}/register/', data=data)
    if response.status_code == 201:
        bot.send_message(message.chat.id, "Регистрация успешно завершена!")
        
    elif response.status_code == 400:
        try: 
            email_error = response.json().get('email')[0]
            if email_error == 'custom user with this email already exists.':
                bot.send_message(message.chat.id, 'Email с таким пользователем уже существует')
            
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так при регистрации. Попробуйте позже.")
        try:
            password_error = response.json().get('password')[0]
            if password_error == "Ensure this field has at least 8 characters.":
                bot.send_message(message.chat.id, 'Пороль должен состоять как минимум из 8 символов')
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так при регистрации. Попробуйте позже.")   
    
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так при регистрации. Попробуйте позже.")   
    
        

    user_data.pop(message.chat.id, None)

if __name__ == '__main__':
    bot.polling()
