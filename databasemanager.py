import sqlite3
import datetime

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

class DatabaseFunctions(object):
    def __init__(self, db):
        
        self.db = db

    def isCommentProcessed(self,comment):
        query = "SELECT comment_id FROM log WHERE comment_id='{0}'".format(comment.id)
        result = self.db.query(query)
        return result.fetchone()

    def insertRecord(self,comment):

        self.db.update("""INSERT INTO log(comment_id, comment_author, link_id, replied)
                    VALUES('{comment_id}', '{comment_author}', '{link_id}', '{replied}')""".format(
                        comment_id = comment.id,
                        comment_author = comment.author.name,
                        link_id = comment.link_id,
                        replied = 0,
                        timestamp = datetime.datetime.utcnow()))

    def updateRecordReplied(self,comment):
        query = "UPDATE log SET replied = 1 WHERE comment_id='{0}'".format(comment.id)
        self.db.update(query)
