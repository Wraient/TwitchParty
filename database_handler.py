import sqlite3

class AnimeDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS anime
                          (id TEXT PRIMARY KEY, name TEXT, episode INTEGER, time_watched TEXT, nickname TEXT NULL)''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def insert_anime(self, id, name, episode, time_watched, nickname=None):
        self.cursor.execute("INSERT OR REPLACE INTO anime (id, name, episode, time_watched, nickname) VALUES (?, ?, ?, ?, ?)", (id, name, episode, time_watched, nickname))
        self.conn.commit()

    def fetch_all_anime(self):
        self.cursor.execute("SELECT * FROM anime")
        return self.cursor.fetchall()

    def search_anime_by_name(self, name):
        self.cursor.execute("SELECT id, name, episode, time_watched, nickname FROM anime WHERE name LIKE ? OR nickname LIKE ?", ('%'+name+'%', '%'+name+'%'))
        return self.cursor.fetchall()

    def add_nickname_by_id(self, id, nickname):
        self.cursor.execute("UPDATE anime SET nickname=? WHERE id=?", (nickname, id))
        self.conn.commit()

    def get_nickname_by_id(self, id):
        self.cursor.execute("SELECT nickname FROM anime WHERE id=?", (id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
