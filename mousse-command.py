#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler
import logging
import time
import os
import datetime
import pytz
import dotenv
import random
import soapclass.RankingDB as RankingDBModule
import soapclass.SoapState as SoapStateModule

dotenv.load_dotenv()
chat_id = os.getenv('chat_id')
bot_token = os.getenv('bot_token')
admin_userid = os.getenv('admin_userid')
script_path = os.path.dirname(__file__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

scale = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

light_strings = [
    "⚫ ⚫ ⚫\n⚫ ⚫ ⚫",
    "⚫ ⚫ 🔴\n⚫ ⚫ 🔴",
    "⚫ 🔴 🔴\n⚫ 🔴 🔴",
    "🔴 🔴 🔴\n🔴 🔴 🔴",
    "⚫ ⚫ ⚫\n⚫ ⚫ ⚫"
]

g_state = SoapStateModule.SoapState()
g_db = RankingDBModule.RankingDB('mousseurs.db')

def end_the_race(context):
    todays_entries = g_state.get_entries()
    rankings_string = "Here's the ranking of the day:\n"
    for index in range(len(todays_entries)):
        entry = todays_entries[index]
        rankings_string += "P{index} : {username} @ {timestamp}\n".format(index=index + 1,username=entry.username, timestamp=entry.timestamp)
        g_db.insert_competitor(str(entry.user_id), entry.username, scale[index])
    context.bot.send_message(chat_id, text=rankings_string)
    g_state.close_the_race()

def send_the_soap(context):
    job = context.job
    sleep_time = random.uniform(0.4, 0.8)
    for index in range(len(light_strings)):
        light_text = light_strings[index]
        if index == 0:
            light_message = context.bot.send_message(job.context, text=light_text)
        else:
            context.bot.edit_message_text(chat_id=light_message.chat_id, message_id=light_message.message_id, text=light_text)
        if index < len(light_strings) - 1:
            time.sleep(sleep_time)

    mousse = open(os.path.join(script_path, "static/sound/mousse.mp3"), "rb")
    context.bot.send_audio(job.context, audio=mousse, title="ATTENTION A LA MOUSSE !", performer="Le mousseur fou", caption="ATTENTION A LA MOUSSE ! /attentionalamousse")
    g_state.open_the_race()

def stop_the_soap(context):
    if g_state.is_race_opened():
        end_the_race(context)

def set_timer(context):
    paris_tz = pytz.timezone('Europe/Paris')

    random_hours = random.randint(10, 18)
    random_minutes = random.randint(0, 59)
    random_seconds = random.randint(0, 59)
    random_microseconds = random.randint(0, 999999)

    start_time = datetime.time(random_hours, random_minutes, random_seconds, random_microseconds, tzinfo=paris_tz)
    end_time = datetime.time(random_hours + 2, random_minutes, random_seconds, random_microseconds, tzinfo=paris_tz)

    context.job_queue.run_once(callback=send_the_soap, when=start_time.replace(tzinfo=None), context=chat_id)
    context.job_queue.run_once(callback=stop_the_soap, when=end_time.replace(tzinfo=None), context=chat_id)


def init_scheduler(update, context):
    if str(update.effective_user.id) != admin_userid:
        # update.message.reply_text('You cannot set the timer. Only an impressive programmer can do it.')
        pass
    else:
        if 'soap_scheduler' in context.chat_data:
            update.message.reply_text('INFO : Removing the former scheduler')
            old_job = context.chat_data['soap_scheduler']
            old_job.schedule_removal()

        paris_tz = pytz.timezone('Europe/Paris')

        start_time = datetime.time(4, 0, 0, 0, tzinfo=paris_tz)

        scheduler_job = context.job_queue.run_daily(callback=set_timer, time=start_time.replace(tzinfo=None), context=chat_id)
        context.chat_data['soap_scheduler'] = scheduler_job
        update.message.reply_text('The scheduler job has been set.')


def mousse(update, context):
    if g_state.is_race_opened():
        if g_state.has_user_entered(update.effective_user.id):
            # update.message.reply_text("You've already entered the race. Skipping your entry...")
            pass
        else:
            paris_tz = pytz.timezone('Europe/Paris')
            utc_tz = pytz.timezone('UTC')
            timestamp = utc_tz.localize(update.message.date).astimezone(paris_tz)
            if (update.effective_user.username):
                username = update.effective_user.username
            else:
                username = update.effective_user.first_name
            g_state.add_entry(update.effective_user.id, username, timestamp.strftime('%H:%M:%S.%f'))
            # update.message.reply_text("Your entry was correctly received. Time : " + timestamp)
            if g_state.get_number_entries() == len(scale):
                end_the_race(context)
            pass

def rankings(update, context):
    update.message.reply_text(g_db.get_rankings())

def help(update, context):
    update.message.reply_text('Rules : Click on "/attentionalamousse" once the bot has sent the message.\n' + 
                            'You have 2 hours to send the command as fast as possible\n' + 
                            'P1 25pts, P2 18pts, P3 15pts, P4 12pts, P5 10pts, P6 8pts, P7 6pts, P8 4pts, P9 2pts, P10 1pt\n' + 
                            'You can also send the command /rankings to see the standings.\n' +
                            'If you jump start (or exploit bugs and glitches), you will be disqualified.')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

    sqlite_db_connection = g_db.get_connection()

    if (sqlite_db_connection == None):
        exit(1)

    updater = Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("rankings", rankings))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("attentionalamousse", mousse))
    dispatcher.add_handler(CommandHandler('init', init_scheduler))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

    if (sqlite_db_connection != None):
        sqlite_db_connection.close()

if __name__ == "__main__":
    main()