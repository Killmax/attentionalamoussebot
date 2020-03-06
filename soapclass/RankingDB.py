import sqlite3
from datetime import datetime

scale = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

class RankingDB:
    def create_connection(self, filename):
        self.connection = None
        try:
            self.connection = sqlite3.connect(filename, check_same_thread=False)
        except sqlite3.Error as e:
            print(e)

    def create_table(self, request):
        try:
            cursor = self.connection.cursor()
            cursor.execute(request)
        except sqlite3.Error as e:
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
        except sqlite3.Error as e:
            print(e)

    def get_rankings(self):
        ranking_requests = "SELECT * FROM mousseurs ORDER BY points DESC"
        ranking_string = ""
        try:
            cursor = self.connection.cursor()
            cursor.execute(ranking_requests)
            rows = cursor.fetchall()
            index = 1
            if (len(rows) == 0):
                return "No races yet."
            for row in rows:
                username = row[1]
                points = row[2]
                last_win = row[3]
                ranking_string += "P{index} : {username} - {points} pt(s) ".format(index=index,username=username, points=points)
                index += 1
                if (last_win):
                    ranking_string += "- Last win : {last_win}\n".format(last_win=last_win)
                else:
                    ranking_string += "- No win\n"
            cursor.close()
        except sqlite3.Error as e:
            print(e)
        
        return ranking_string

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