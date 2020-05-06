import telegram
import time
import os
from dotenv import load_dotenv

load_dotenv()
bot = telegram.Bot(token=os.getenv('bot_token'))
chat_id = os.getenv('chat_id')
script_path = os.path.dirname(__file__)

def send_the_soap():
    mousse = open(os.path.join(script_path, "static/sound/mousse.mp3"), "rb")
    bot.send_audio(chat_id=chat_id, audio=mousse, title="ATTENTION A LA MOUSSE !", performer="Le mousseur fou", caption="ATTENTION A LA MOUSSE ! /attentionalamousse")

if __name__ == "__main__":
    send_the_soap()