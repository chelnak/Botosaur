import sqlite3

class DatabaseManager(object):
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

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
