#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler
import logging
import time
import os
import sqlite3
from sqlite3 import Error
from datetime import datetime, date
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()
# chat_id = os.getenv('chat_id')
chat_id = "68878627"
bot_token=os.getenv('bot_token')
script_path = os.path.dirname(__file__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class SoapState:
    class Entry:
        def __init__(self, user_id, username, timestamp):
            self.username = username
            self.user_id = user_id
            self.timestamp = timestamp

    def open_the_race(self):
        self.is_open_for_race = True
        self.entries = []
    
    def close_the_race(self):
        self.is_open_for_race = False

    def add_entry(self, user_id, username, timestamp):
        self.entries.append(self.Entry(user_id, username, timestamp))
            
    def get_entries(self):
        return self.entries
    
    def is_race_opened(self):
        return self.is_open_for_race
    
    def get_number_entries(self):
        return len(self.entries)

class RankingDB:
    def create_connection(self, filename):
        self.connection = None
        try:
            self.connection = sqlite3.connect(filename)
        except Error as e:
            print(e)

    def create_table(self, request):
        try:
            cursor = self.connection.cursor()
            cursor.execute(request)
        except Error as e:
            print(e)

    def __init__(self, filename):
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
        # create a database connection
        self.create_connection(filename)
    
        # create tables
        if self.connection is not None:
            self.create_table(sql_create_projects_table)
        else:
            print("Error! cannot create the database connection.")

g_state = SoapState()

def send_the_soap(context):
    job = context.job
    mousse = open(os.path.join(script_path, "static/sound/mousse.mp3"), "rb")
    context.bot.send_audio(job.context, audio=mousse, title="ATTENTION A LA MOUSSE !", performer="Le mousseur fou", caption="ATTENTION A LA MOUSSE ! /attentionalamousse")
    g_state.open_the_race()

def set_timer(update, context):
    paris_tz = timezone('Europe/Paris')
    today_date = date.today()
    timer_datetime = datetime(today_date.year, today_date.month, today_date.day, 16, 0, 0, 0, tzinfo=paris_tz)

    if 'job' in context.chat_data:
        # Add a condition in order to be impossible to set the timer one hour before 4pm
        update.message.reply_text('INFO : Removing the former timer')
        old_job = context.chat_data['job']
        old_job.schedule_removal()

    new_job = context.job_queue.run_daily(send_the_soap, timer_datetime.replace(tzinfo=None), context=chat_id)
    context.chat_data['job'] = new_job
    
    update.message.reply_text('Ready to send the soap.')

def mousse(update, context, db_instance):
    if g_state.is_race_opened():
        if g_state.get_number_entries() == 3:
            todays_entries = g_state.get_entries()
            rankings_string = "Here's the ranking of the day:\n"
            for index in range(len(todays_entries)):
                rankings_string += "P{index} : {username} @ {timestamp}\n".format(index=index + 1,username=todays_entries[index].username, timestamp=todays_entries[index].timestamp)
            context.bot.send_message(chat_id, text=rankings_string)
            # Update DB and close the race
            g_state.close_the_race()
        else:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')
            g_state.add_entry(update.effective_user.id, update.effective_user.username, timestamp)
            update.message.reply_text("Your entry was correctly received. Time : " + timestamp)
            pass

# A function to handle "/rankings", which will answer the ranking
def rankings(update, context):
    pass

def help(update, context):
    update.message.reply_text('Rules : Send the command /attentionalamousse once the bot has sent the message.\n' + 
                            'The first person will earn 10 points, the second one 5 points and the third one 1 point\n' + 
                            'You can also send the command /rankings to see the standings.\n' +
                            'Don\' forget to init me by sending me the command /setthesoap')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # To be removed
    g_state.open_the_race()
    updater = Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("rankings", rankings))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("attentionalamousse", mousse))
    dispatcher.add_handler(CommandHandler('setthesoap', set_timer))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()