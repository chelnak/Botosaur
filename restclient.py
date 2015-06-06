#!/usr/bin/env python
import requests
import json
import sys
import datetime
import random

def checkResponse(r):
    """
    Quick logic to check the http response code.
    
    Parameters:
        r = http response object.
    """

    acceptedResponses = [200,201,204]
    if not r.status_code in acceptedResponses:
        print "STATUS: {status} ".format(status=r.status_code)
        print "ERROR: " + r.text
        sys.exit(r.status_code)

class RestClient(object):
    def __init__(self, host):

        self.host = host

    def isCommentProcessed(self, comment_id):

        host = self.host
        headers = {'Content-Type': 'application/json'}

        filters = [dict(name='comment_id', op='eq', val=comment_id)]
        params = dict(q=json.dumps(dict(filters=filters)))

        url = 'http://' + host + '/bot/api/log'
        r = requests.get(url, params=params, headers=headers)
        checkResponse(r)
        result = r.json()['num_results']
        
        return result
        
    def insertRecord(self, comment):

        host = self.host
        headers = {'Content-Type': 'application/json', 'Accept' : 'application/json'}

        payload = {"comment_id" : comment.id, 
                   "comment_author" : comment.author.name,
                   "link_id" : comment.link_id,
                   "replied" : 0,
                   "created_on" : datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
 
        url = 'http://' + host + '/bot/api/log'
        r = requests.post(url = url, data = json.dumps(payload), headers = headers)
        checkResponse(r)

        return r.json()

    def updateRecord(self, record_id, fact_id):

        host = self.host
        headers = {'Content-Type': 'application/json'}
        print fact_id
        payload = {"fact_id": fact_id,
                   "replied": 1
        }

        url = 'http://' + host + '/bot/api/log/{id}'.format(id=str(record_id))
        r = requests.put(url, data=json.dumps(payload), headers=headers)
        checkResponse(r)

        return r.json()

    def deleteRecord(self, id):

        host = self.host
        headers = {'Content-Type': 'application/json'}

        url = 'http://' + host + '/bot/api/log/{id}'.format(id=str(id))
        r = requests.delete(url, headers=headers)
        checkResponse(r)

        return r.json()


    def getRandom(self):

        host = self.host
        headers = {'Content-Type': 'application/json'}

        url = 'http://' + host + '/bot/api/fact'
        r = requests.get(url, headers=headers)
        checkResponse(r)

        numResults = r.json()['num_results']
        randomId = random.randint(1, numResults)

        url = 'http://' + host + '/bot/api/fact/{fact_id}'.format(fact_id=randomId)
        r = requests.get(url, headers=headers)
        checkResponse(r)
        
        return r.json()
        


"""
UNIT TEST


print datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

c = RestClient('chelnak.co.uk')

random = c.getRandom()
print random['fact']

if c.isCommentProcessed() is 0:
    print "it was none"

print c.isCommentProcessed()

print "inserting record"
record = c.insertRecord()
print "Record id is " + str(record['id'])

print "updating record"
update = c.updateRecord(123,record['id'])
print update

print "delete record"
delete = c.deleteRecord(record['id'])
print delete

"""
