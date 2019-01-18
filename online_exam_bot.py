#-*. coding: utf:8 -*-
import sys
import time
import datetime
import telepot
import requests
import pymongo
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup,InlineKeyboardButton
from pprint import pprint
import numpy
import matplotlib.pyplot
import xlsxwriter
import pandas
import database_communication
import admin
import user

# Token gotten from telegram botfather

Token = '722321256:AAHZYQTTVlopUXAuTQTIHVvjKa5iIbLZ5fQ'

# Welcome Message

welcome_message = 'خوش آمدید'

#the command for creating the bot based on the Token that bot father gave us

bot = telepot.Bot(Token)

#to understand that bot is working correctly

print(bot.getMe(),'\n')
print('Listening...\n')

userss = {}
my_question = {}
collection = "members"
searched = {'id' : '37788570'}
userss['id'] = '37788570'
userss['user_name'] = 'mohamad_aref'
userss['password'] = '37788570bb'
try:
    database_communication.database_communication.save_user_to_db(userss)
except:
    print("there is a repeated key!!!")
admin.admin.import_questions()
database_communication.database_communication.read_from_db(collection,searched)
user_name = input('enter your username:')
password = input('enter your password:')
usr = user.user(user_name,password,score = 0)
usr.sign_in()
