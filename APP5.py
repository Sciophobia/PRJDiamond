import datetime
import uuid

from pymongo import MongoClient, ASCENDING


class App5:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.team6DB
        self.logCollection = self.db.Log
        self.logCollection.ensure_index([("timestamp", ASCENDING)])
        self.log("App5", "Connection to Mongo Collection Successful!")

    '''All workflow actions are logged into the MongoClient's log collection. Time is determined using datetime with
    Greenwich Mean Time. '''
    def log(self, node, activitydescription):
        self.client = MongoClient()
        self.db = self.client.team6DB
        self.logCollection = self.db.Log
        self.logCollection.ensure_index([("timestamp", ASCENDING)])
        entry = {'activityID': uuid.uuid4(), 'nodeName': node, 'activityDescription': activitydescription,
                 'timestamp': datetime.datetime.utcnow()}
        self.logCollection.insert(entry)
        return {'nodeName': node, 'activityDescription': activitydescription}
