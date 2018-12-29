#-*. coding: utf:8 -*-
import sys
import time
import requests
import pymongo
from pymongo import *
import pprint

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


    collection = ""

    #a function for saving datas in database

    #a function as a class constructor
    def __init__(self,connection_params,connection,db,collection):
        self.connection_params = connection_params
        self.connection = connection
        self.db = db
        self.collection = collection

    #a function for saving members in the database
    @classmethod
    def save_user_to_db(cls,user):
        cls.db.members.insert(user)
        return


    #a function for saving questions in the database
    @classmethod
    def save_questions_to_db(cls,my_question):
        cls.db.questions.insert(my_question)
        return

    #a function for reading data from database
    @classmethod
    def read_from_db(cls,collection,searched):
        if collection == "questions":
            pprint.pprint(cls.db.questions.find_one(searched))
        if collection == "members":
            pprint.pprint(cls.db.members.find_one(searched))
        return
