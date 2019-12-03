import telegram
import time
import os
import random

from dotenv import load_dotenv
load_dotenv()
bot = telegram.Bot(token=os.getenv("bot_token"))
chat_id = os.getenv("chat_id")

def send_the_bullshit(bullshit):
    bot.send_message(chat_id=chat_id, text=bullshit)

if __name__ == "__main__":
    sentences = [
        "/adrofdp",
        "KOGHONTA 🗝️",
        "TG Raphi @Raphicci"
    ]
    send_the_bullshit(random.choice(sentences))