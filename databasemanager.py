import sqlite3

class DatabaseManager(object):
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS botosaur_log(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            comment_id CHAR(10) NOT NULL,
                            comment_author CHAR(50) NOT NULL,
                            link_id CHAR(10) NOT NULL,
                            replied INTEGER NOT NULL)""")

        self.conn.commit()

    def update(self, arg):
        try:
            self.cur.execute(arg)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e


    def query(self, arg):
        try:
            self.cur.execute(arg)
            self.conn.commit()
            return self.cur
        except Exception as e:
            raise e

    def __del__(self):
        self.conn.close()
