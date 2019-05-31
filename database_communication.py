#-*. coding: utf:8 -*-
import sys
import time
import requests
import pymongo
from pymongo import *
import pprint
import config


#setting the database pre-prerequirements
class database_communication():

    connection_params = {
    'user' : config.conf['user'],
    'password' : config.conf['password'],
    'host' : config.conf['host'],
    'port': int(config.conf['port']),
    'namespace' : config.conf['namespace']
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
            pprint.pprint(searched)

            try:
                for my_question in cls.db.questions.find(searched):
                    pprint.pprint(my_question)
                    return my_question
            except:
                print('Not found 404 :)))')
        if collection == "members":
            pprint.pprint(searched)

            try:
                for user in cls.db.members.find(searched):
                    pprint.pprint(user)
                    return user
            except:
                print('Not found 404 :)))')

    @classmethod
    def count_entry(cls,collection,entry):
        if collection == "questions":
            num = cls.db.questions.count_documents(entry)
            return num


    @classmethod
    def update(cls,new_entry,my_query):
        new_value = {}
        new_value['$set'] = new_entry
        cls.db.members.update_one(my_query,new_value)
