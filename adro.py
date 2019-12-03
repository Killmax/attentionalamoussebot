import telegram
import time
import os
from dotenv import load_dotenv
load_dotenv()

def say_the_truth():
    bot.send_message(chat_id=chat_id, text="N'oubliez pas, Adrien est le genre de personne à prendre du tofu à Chipotle. /adrolefdp")

if __name__ == "__main__":
    bot = telegram.Bot(token=os.getenv('bot_token'))
    chat_id = os.getenv('chat_id')
    say_the_truth()