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

scale = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

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
            self.connection = sqlite3.connect(filename, check_same_thread=False)
        except Error as e:
            print(e)

    def create_table(self, request):
        try:
            cursor = self.connection.cursor()
            cursor.execute(request)
        except Error as e:
            print(e)
    
    def get_connection(self):
        return self.connection

    def insert_competitor(self, user_id, username, points_to_add):
        exists_request = "SELECT points FROM mousseurs WHERE user_id = ?"
        creation_request = "INSERT INTO mousseurs (user_id, username, points, last_win) VALUES (?,?,?,?)"
        update_request = "UPDATE mousseurs set username = ?, points = ? where user_id = ?"
        update_request_win = "UPDATE mousseurs set username = ?, points = ?, last_win = ? where user_id = ?"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(exists_request, (user_id,))
            player = cursor.fetchone()
            if (player):
                former_points = player[0]
                if (points_to_add == scale[0]):
                    cursor.execute(update_request_win, (username, points_to_add + former_points, datetime.now().strftime('%d/%m/%Y'), user_id))
                else:
                    cursor.execute(update_request, (username, points_to_add + former_points, user_id))
            else:
                new_competitor_data = (user_id, username, points_to_add, datetime.now().strftime('%d/%m/%Y') if points_to_add == scale[0] else None)
                cursor.execute(creation_request, new_competitor_data)
            self.connection.commit()
        except Error as e:
            print(e)

    def __init__(self, filename):
        sql_create_mousseurs_table = """ CREATE TABLE IF NOT EXISTS mousseurs (
                                        user_id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        points integer,
                                        last_win text
                                    ); """
        self.create_connection(filename)
    
        if self.connection is not None:
            self.create_table(sql_create_mousseurs_table)
        else:
            print("Error! cannot create the database connection.")

g_state = SoapState()
g_db = RankingDB('mousseurs.db')

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

def mousse(update, context):
    if g_state.is_race_opened():
        if g_state.get_number_entries() == len(scale): # Add two hours limit
            todays_entries = g_state.get_entries()
            rankings_string = "Here's the ranking of the day:\n"
            for index in range(len(todays_entries)):
                entry = todays_entries[index]
                rankings_string += "P{index} : {username} @ {timestamp}\n".format(index=index + 1,username=entry.username, timestamp=entry.timestamp)
                g_db.insert_competitor(str(entry.user_id), entry.username, scale[index])
            context.bot.send_message(chat_id, text=rankings_string)
            g_state.close_the_race()
        else:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')
            if (update.effective_user.username):
                username = update.effective_user.username
            else:
                username = update.effective_user.first_name
            g_state.add_entry(update.effective_user.id, username, timestamp)
            update.message.reply_text("Your entry was correctly received. Time : " + timestamp)
            pass

# A function to handle "/rankings", which will answer the ranking
def rankings(update, context):
    pass

def help(update, context):
    update.message.reply_text('Rules : Send the command /attentionalamousse once the bot has sent the message.\n' + 
                            'You have 2 hours to send the command as fast as possible\n' + 
                            'P1 25pts, P2 18pts, P3 15pts, P4 12pts, P5 10pts, P6 8pts, P7 6pts, P8 4pts, P9 2pts, P10 1pt]\n' + 
                            'You can also send the command /rankings to see the standings.\n' +
                            'Don\' forget to init me by sending me the command /setthesoap')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # To be removed, only for test purposes
    g_state.open_the_race()

    sqlite_db_connection = g_db.get_connection()

    if (sqlite_db_connection == None):
        exit(1)

    updater = Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("rankings", rankings))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("attentionalamousse", mousse))
    dispatcher.add_handler(CommandHandler('setthesoap', set_timer))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

    if (sqlite_db_connection != None):
        sqlite_db_connection.close()

if __name__ == "__main__":
    main()