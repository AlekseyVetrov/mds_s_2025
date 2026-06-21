import os
import logging
import telebot
from dotenv import load_dotenv
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "http://localhost:8000"

if not BOT_TOKEN:
    raise ValueError(" BOT_TOKEN не найден в .env")
bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
        "Привет, я ИИ-ассистент!\n\n"
        "Просто напиши мне любой вопрос.\n"
        "Я помню историю диалога.\n\n"
        "Команды:\n"
        "/clear - очистить историю диалога\n"
        "/help - показать это сообщение",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['clear'])
def clear_history(message):
    user_id = str(message.from_user.id)
    try:
        response = requests.post(f"{API_URL}/clear", json={"user_id": user_id})
        if response.status_code == 200:
            bot.reply_to(message, " История диалога очищена!")
        else:
            bot.reply_to(message, " Ошибка при очистке истории.")
    except Exception as e:
        bot.reply_to(message, f" Ошибка: {e}")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = str(message.from_user.id)
    prompt = message.text
    
    bot.send_chat_action(message.chat.id, "typing")
    
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"user_id": user_id, "prompt": prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            
            if len(answer) > 4000:
                for x in range(0, len(answer), 4000):
                    bot.send_message(message.chat.id, answer[x:x+4000])
            else:
                bot.reply_to(message, answer)
        else:
            bot.reply_to(message, f" Ошибка API: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, 
            " Не удалось подключиться к серверу.\n"
            "Убедитесь, что бэкенд запущен: uvicorn backend.api:app --reload"
        )
    except requests.exceptions.Timeout:
        bot.reply_to(message, " Превышено время ожидания ответа от сервера.")
    except Exception as e:
        bot.reply_to(message, f" Ошибка: {e}")

if __name__ == "__main__":
    print("Телеграм-бот запущен")
    bot.infinity_polling()