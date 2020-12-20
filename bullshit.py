import telegram
import os
import random

def k_hole(context, script_path):
    job = context.job
    context.bot.send_sticker(job.context, sticker="CAACAgQAAxkBAAIkCl4-wMNJmwOEcnMC1XXOJzrR8JJOAAJdAAMurXMFoVrlM5sfuNcYBA")
    context.bot.send_message(job.context, text="KOGHONTA 🗝️ /pleinlepif")

def elbow_fall(context, script_path):
    job = context.job
    downfall = open(os.path.join(script_path, "static/img/descente.jpg"), "rb")
    context.bot.send_photo(job.context, photo=downfall, caption="Attention à la descente du coude ! /souslepavelaket")

def dridri_fdp(context, script_path):
    job = context.job
    context.bot.send_sticker(job.context, sticker="CAACAgQAAxkBAAIkDF4-wP8smpTDJqw_uSPM6NP9Q_uiAAI7AAMurXMFsFxOoUHqFN8YBA")
    context.bot.send_message(job.context, text="/adrofdp")

def pay_respects(context, script_path):
    job = context.job
    mike = open(os.path.join(script_path, "static/img/mike.jpg"), "rb")
    context.bot.send_photo(job.context, photo=mike, caption="Une pensée pour Mike, petit ange parti trop gros... /f")

def gaziers_unite(context, script_path):
    job = context.job
    gang = open(os.path.join(script_path, "static/img/gaziers.jpg"), "rb")
    gazier = open(os.path.join(script_path, "static/sound/gaziers.mp3"), "rb")
    context.bot.send_audio(job.context, audio=gazier, title="GAZIERS ASSEMBLE !", performer="Les gaziers", caption="GAZIERS ASSEMBLE !")
    context.bot.send_photo(job.context, photo=gang, caption="GAZIERS ASSEMBLE ! /assemble")

def guerville_triggered(context, script_path):
    job = context.job
    stickers_id = [
        "CAACAgIAAxkBAAIjxF4-vNlx5_ivb2SnBtrTJMpJ5M3uAAI9AgACSTSIAkM8zYDgtBYyGAQ",
        "CAACAgIAAxkBAAIjxV4-vNoi8JIwj-MNkYigoHiua21KAAI-AgACSTSIAi2Y6W_6cPf2GAQ",
        "CAACAgIAAxkBAAIjxl4-vNv1ZnumtpKc0fWUS1vcPx60AAI_AgACSTSIAohY5CAkmq8lGAQ",
        "CAACAgIAAxkBAAIjyl4-vPMzMp0mTOJkz-nfDuBeJzDmAAJAAgACSTSIAtxuQgpw1CFFGAQ",
        "CAACAgIAAxkBAAIjy14-vPSndUFh5BoGjxIIfyM6hEV4AAJBAgACSTSIAmgBGzufPWDTGAQ",
        "CAACAgIAAxkBAAIjzF4-vPQs-P2LNDmD2mrYM0EFD29wAAJCAgACSTSIAg8PdQAB5HoWZRgE",
        "CAACAgIAAxkBAAIjzl4-vPUb-9EEz8Z03NeMyzLo8wWNAAJDAgACSTSIApZczFMoFnETGAQ",
        "CAACAgIAAxkBAAIjz14-vPXeC98FOvkoYWkfwMDeqtVYAAJEAgACSTSIApxy-AZ9qZx_GAQ",
        "CAACAgIAAxkBAAIj0F4-vPbfCvTMmPpNccOtH_MAAfsMoAACRQIAAkk0iAIdHlUUPpzk7xgE",
        "CAACAgIAAxkBAAIj0V4-vPZ0PzOZ9JoUftPJT4rxzR-3AAJGAgACSTSIAnLdShwf_NfDGAQ",
        "CAACAgIAAxkBAAIj014-vPY5RqNBkBGW2c8Oo35KM2qVAAJHAgACSTSIAsyXpEBXsaldGAQ",
        "CAACAgIAAxkBAAIj1F4-vPfnNaRY_k_JHu_A_rb762-IAAJIAgACSTSIArCIpKNwbO8qGAQ",
        "CAACAgIAAxkBAAIj114-vPcayOeE-WGFbHqj57KTY15dAAJJAgACSTSIAjzLrNHGLJ2IGAQ",
        "CAACAgIAAxkBAAIj2V4-vPgVcd7R-eLUdW3xrPr38l1fAAJKAgACSTSIAusyCl0qv_trGAQ",
        "CAACAgIAAxkBAAIj214-vPgNu9ajLt_zJ3y_mgZlwfgoAAJLAgACSTSIAqH9qB2QDbXlGAQ",
        "CAACAgIAAxkBAAIj314-vPnTsHnrFPk-mF8obcHw5NZOAAJMAgACSTSIAiQpfTwyrDmsGAQ",
        "CAACAgIAAxkBAAIj414-vPqlWsQqC8pkcoLUgpR0RKB9AAJNAgACSTSIAoZJ4QHaSl65GAQ",
        "CAACAgIAAxkBAAIj5V4-vPtXLHxoawTTcZpwYH1YFNH1AAJOAgACSTSIAvHuvk7_qnlIGAQ",
        "CAACAgIAAxkBAAIj5l4-vPtB8qeVC5p4pMYUh35_iLp0AAJPAgACSTSIAozz1guiLduRGAQ",
        "CAACAgIAAxkBAAIj6l4-vQGbK6-WW44nNq-TK6mBNIeFAAJQAgACSTSIAm_cr8HmUKpNGAQ",
        "CAACAgIAAxkBAAIj614-vQJqvpJQifhiH5CnA4S9K-G8AAJRAgACSTSIAtTIiywCoq7ZGAQ",
        "CAACAgIAAxkBAAIj7F4-vQOzts_VdOxBV0ASuzSbgy9WAAJSAgACSTSIAjYjVJjmMs3wGAQ",
        "CAACAgIAAxkBAAIj7l4-vQRBFkJ5sUN4bFt0bXQWwNATAAJTAgACSTSIAvQhQ3mh6gABRRgE",
        "CAACAgIAAxkBAAIj714-vQQfREGJisfwMiXNigx71kIgAAJVAgACSTSIAki_VBMIPFB1GAQ",
        "CAACAgIAAxkBAAIj9F4-vQYtdOyr6eB9zciWI7NiRfp6AAJXAgACSTSIAgIu0kvEhnO9GAQ",
        "CAACAgIAAxkBAAIj8V4-vQX-efKglE8VbCig5aEDAv4fAAJWAgACSTSIAiSnPVoGWygkGAQ",
        "CAACAgIAAxkBAAIj9l4-vQdmx7LhqX1X8f0LnQcuHO8eAAJYAgACSTSIAiV2zq35TR-hGAQ",
        "CAACAgIAAxkBAAIj914-vQf8dVBFwVMkayI4aZ-ATKSSAAJZAgACSTSIApvJXq2Y21ZQGAQ",
        "CAACAgIAAxkBAAIj-l4-vQiKKVtGCzU9IZKD5Oyc9nYPAAJdAgACSTSIAsNQFli_9UJTGAQ",
        "CAACAgIAAxkBAAIj-l4-vQiKKVtGCzU9IZKD5Oyc9nYPAAJdAgACSTSIAsNQFli_9UJTGAQ",
        "CAACAgIAAxkBAAIj_l4-vQnpAZpAd17r4TgjY0Ex28qFAAJbAgACSTSIAvNYgvUAASerxxgE",
        "CAACAgIAAxkBAAIkAAFePr0KyCSsdmP0dgJ9iRaXbcEGTgACWgIAAkk0iAKY-LmGoQABJjkYBA",
        "CAACAgIAAxkBAAIkAl4-vQvYsPRvSrkdIWmdLqwUDtzuAAJeAgACSTSIAiVpNVoUcIlxGAQ"
    ]
    
    context.bot.send_sticker(job.context, sticker=random.choice(stickers_id))

def yellow_vest(context, script_path):
    job = context.job
    context.bot.send_sticker(job.context, sticker="CAACAgQAAxkBAAIkDl4-wmYk7fVQ0ttgH51PMjHfyFJeAAJcAAMurXMFEMftarxz0IsYBA")
    context.bot.send_message(job.context, text="MICRON DEMISSION ! /acab")

def bullshit_sender(context):
    script_path = os.path.dirname(__file__)
    bullshit = [
        elbow_fall,
        k_hole,
        dridri_fdp,
        pay_respects,
        gaziers_unite,
        guerville_triggered,
        yellow_vest
    ]
    random.choice(bullshit)(context, script_path)