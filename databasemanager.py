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
        self.db.update("""INSERT INTO log(comment_id, comment_author, link_id, replied,created_on)
                    VALUES('{comment_id}', '{comment_author}', '{link_id}', '{replied}', '{created_on}')""".format(
                        comment_id = comment.id,
                        comment_author = comment.author.name,
                        link_id = comment.link_id,
                        replied = 0,
                        created_on = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))

    def updateRecord(self,comment,fact_id):
        query = "UPDATE log SET replied = 1, fact_id ={0}  WHERE comment_id='{1}'".format(fact_id, comment.id)
        self.db.update(query)

    def getRandomFact(self):
        query = "SELECT id, fact from fact ORDER BY RANDOM() LIMIT 1;"
        result = self.db.query(query)   
        return result.fetchone()
    
