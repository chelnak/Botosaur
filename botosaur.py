#!/usr/bin/env python

import os
import logging
import random
import praw
import requests
from databasemanager import DatabaseManager
from time import sleep
from ConfigParser import SafeConfigParser


def getFact(file):
    content = None
    if os.path.isfile(file):
        with open(file, 'r') as f:
            content = f.readlines()

        return random.choice(content)

def respondToTrigger(comment):
    fact = getFact("facts.txt")
    comment.reply(fact)

def commentProcessed(db,comment_id):
    query = "SELECT comment_id FROM botosaur_log WHERE comment_id='{0}'".format(comment_id)
    result = db.query(query)

    return result.fetchone()

def addToDatabase(db,comment):
    
    db.update("""INSERT INTO botosaur_log(comment_id, comment_author, link_id, replied)
                VALUES('{comment_id}', '{comment_author}', '{link_id}', '{replied}')""".format(
                    comment_id = comment.id,
                    comment_author = comment.author.name,
                    link_id = comment.link_id,
                    replied = 0))

def updateDatabase(db,comment_id):

    query = "UPDATE botosaur_log SET replied = 1 WHERE comment_id='{0}'".format(comment_id)
    db.update(query)

def main():

    #Do requests SSL stuff
    requests.packages.urllib3.disable_warnings()

    #Get configuration  
    parser = SafeConfigParser()
    parser.read('config.ini')
    config = parser._sections['defaults']

    #Configure logging
    logger = logging.getLogger('BOTOSAUR')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(config['log_file'])
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #Initialize commentsDB
    logger.info('Initializing database')   
    db = DatabaseManager('botosaur.db')

    #Initialize reddit client
    logger.info('Initializing reddit API client')
    r = praw.Reddit(user_agent = config['user_agent'])

    #login
    logger.info('Attempting to log in to reddit with credentials from config.ini')
    r.login(config['bot_user'], config['bot_pass'])

    #Get reddit user
    logger.info('Retrieving subreddit: ' + config['subreddit'])
    subreddit = r.get_subreddit(config['subreddit'])

    #Main loop of program
    logger.info('Beginning monitor..')
    logger.info('Retrieving comments with limit of ' + str(config['limit']))
    
    while True:
        
        comments = subreddit.get_comments(limit=int(config['limit']))

        for comment in comments:

            if commentProcessed(db,comment.id) is None:
                
                logger.info('Processing ' + comment.id + ' by user ' + comment.author.name)
                addToDatabase(db, comment)

                if (comment.author.name == config['bot_user'] and config['trigger'] in comment.body):

                    logger.info('Found trigger in ' + comment.id)

                    respondToTrigger(comment)
                    
                    logger.info('Updating replied field')                                    

                    updateDatabase(db, comment.id)

                else:         
                    logger.info('No trigger found. Ignorinng comment')

        sleep(int(config['poll_time']))

if __name__ == "__main__":
    main()

