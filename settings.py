# Project: Lab 6 Client and Server Using Eve on Linux, CURL, CRUD with MongoDB
# Purpose Details: Initial utilization of CRUD with MongoDB through eve
# Course: IST 411
# Author: Sciophobia (Timothy)
# Date Developed: 10/1/2021
# Last Date Changed: 10/3/2021
# Rev: 1

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'db'

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

LogSchema = {
    'activityID': {
        'type': 'string',
        'required': True,
        'unique': True,
    },
    # Title of APP
    'nodeName':{
        'type': 'string',
        'required': True,
    },
    # Description of Activity
    'activityDescription':{
        'type': 'string',
        'required': True,
    },
    # Time and Date
    'timestamp':{
        'type': 'datetime',
        'required': True,
    },
}

Logs = {
    'item_title': 'Log',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'ActivityID'
    },
    
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'NodeName'
    },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST', 'DELETE'],

    'schema': LogSchema
}

DOMAIN = {
    'Log': Logs,
}

