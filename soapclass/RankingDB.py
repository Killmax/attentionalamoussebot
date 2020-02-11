import sqlite3
from sqlite3 import Error
from datetime import datetime

scale = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

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