import telegram
import time
import os
from dotenv import load_dotenv
load_dotenv()

def send_the_soap():
    bot.send_message(chat_id=chat_id, text="ATTENTION A LA MOUSSE ! /attentionalamousse")

if __name__ == "__main__":
    bot = telegram.Bot(token=os.getenv('bot_token'))
    chat_id = os.getenv('chat_id')
    send_the_soap()