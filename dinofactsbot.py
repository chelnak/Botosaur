#!/usr/bin/env python

import os
import logging
import random
import praw
import requests
from databasemanager import DatabaseManager, DatabaseFunctions
from time import sleep
from ConfigParser import SafeConfigParser
from logging.handlers import TimedRotatingFileHandler

def getFact(file):
    content = None
    if os.path.isfile(file):
        with open(file, 'r') as f:
            content = f.readlines()

        return random.choice(content)


def respondWithFact(fact, comment):
    comment.reply(fact)
      
def botInfo(comment):
    
    reply = """Hi, i'm botosaur. I reply to certain comments with useless facts about Dinosaurs!\n\n

               USAGE: Call me by mentioning my username +fact. E.g. /u/phalosaurus_ +fact\n\n

               My code can be found here: https://github.com/chelnak/Botosaur"""

    comment.reply(reply)

def main():

    #Do requests SSL stuff
    requests.packages.urllib3.disable_warnings()

    #Get configuration  
    parser = SafeConfigParser()
    parser.read('/etc/dinofactsbot/config.ini')
    config = parser._sections['defaults']

    #Configure logging
    logger = logging.getLogger('BOTOSAUR')
    logger.setLevel(logging.INFO)
#    handler = TimedRotatingFileHandler('test.log',when='midnight')
    handler = TimedRotatingFileHandler(config['log_file'],when='midnight')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #Initialize commentsDB
    logger.info('Initializing database')   
    db = DatabaseManager(config['database'])
    dbcmd = DatabaseFunctions(db)

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
        
        try:
        
            comments = subreddit.get_comments(limit=int(config['limit']))

            for comment in comments:

                if dbcmd.isCommentProcessed(comment) is None:
                
                    logger.info('Processing ' + comment.id + ' by user ' + comment.author.name)
                    dbcmd.insertRecord(comment)

                    if (config['trigger'] in comment.body):
                    
                        logger.info('Found trigger in ' + comment.id)
                        fact = dbcmd.getRandomFact()
                        logger.info('Retrieved fact: ' + str(fact[1]))
                        respondWithFact(str(fact[1]), comment)                
                        logger.info('Updating replied field')                                    
                        dbcmd.updateRecord(comment, int(fact[0]))

                    else:         

                        logger.info('No trigger found. Ignorinng comment')

            sleep(int(config['poll_time']))

        except Exception as e:
                    
            logger.error(e)


if __name__ == "__main__":
    main()

