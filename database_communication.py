#-*. coding: utf:8 -*-
import sys
import time
import requests
import pymongo
from pymongo import *

#setting the database pre-prerequirements
class database_communication():
    connection_params = {
    'user' : 'mohamad-aref',
    'password' : '37788570b',
    'host' : 'ds121624.mlab.com',
    'port': 21624,
    'namespace' : 'users'
    }

    #the request that should be made to connect to our mongo database

    connection = MongoClient(
    'mongodb://{user}:{password}@{host}:'
    '{port}/{namespace}'.format(**connection_params)
    )

    db = connection.users

    #a function for saving datas in database

    #a function as a class constructor
    def __init__(self,connection_params,connection,db):
        self.connection_params = connection_params
        self.connection = connection
        self.db = db


    @classmethod
    def save_to_db(cls,user):
        cls.db.members.insert(user)
