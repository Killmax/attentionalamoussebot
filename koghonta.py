import telegram
import time
import os
from dotenv import load_dotenv
load_dotenv()

def answer_ketamine_call():
    bot.send_message(chat_id=chat_id, text="KOGHONTA 🗝️")

if __name__ == "__main__":
    bot = telegram.Bot(token=os.getenv('bot_token'))
    chat_id = os.getenv('chat_id')
    answer_ketamine_call()