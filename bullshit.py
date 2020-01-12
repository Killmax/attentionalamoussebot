import telegram
import time
import os
import random
from dotenv import load_dotenv

load_dotenv()
bot = telegram.Bot(token=os.getenv("bot_token"))
chat_id = os.getenv("chat_id")
script_path = os.path.dirname(__file__)

def k_hole():
    bot.send_message(chat_id=chat_id, text="KOGHONTA 🗝️")

def elbow_fall():
    downfall = open(os.path.join(script_path, "static/img/descente.jpg"), "rb")
    bot.send_photo(chat_id=chat_id, photo=downfall, caption="Attention à la descente du coude !")

def dridri_fdp():
    bot.send_message(chat_id=chat_id, text="/adrofdp")

def where_is_he():
    bot.send_sticker(chat_id=chat_id, sticker="CAADBAADTQADLq1zBa43XuIzrsdsFgQ")

def pay_respects():
    mike = open(os.path.join(script_path, "static/img/mike.jpg"), "rb")
    bot.send_photo(chat_id=chat_id, photo=mike, caption="Une pensée pour Mike, petit ange parti trop gros... /f")

def gaziers_unite():
    downfall = open(os.path.join(script_path, "static/img/gaziers.jpg"), "rb")
    bot.send_photo(chat_id=chat_id, photo=downfall, caption="GAZIERS ASSEMBLE !")

def guerville_triggered():
    bot.send_message(chat_id=chat_id, text="Coucou @Sadzeih")
    bot.send_sticker(chat_id=chat_id, sticker="CAADAgADXQIAAkk0iALDUBZYv_VCUxYE")

if __name__ == "__main__":
    bullshit = [
        elbow_fall,
        k_hole,
        dridri_fdp,
        where_is_he,
        pay_respects,
        gaziers_unite,
        guerville_triggered
    ]
    random.choice(bullshit)()