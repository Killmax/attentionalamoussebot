class SoapState:
    entries = []
    is_open_for_race = False

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

    def has_user_entered(self, user_id):
        return any(elem.user_id == user_id for elem in self.entries)
