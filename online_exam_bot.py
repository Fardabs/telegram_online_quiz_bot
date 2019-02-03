#-*. coding: utf:8 -*-
import sys
import time
import datetime
import telepot
import telegram
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
from telegram import TelegramObject
from random import randint
import pprint
import copy


# Token gotten from telegram botfather

Token = '722321256:AAHZYQTTVlopUXAuTQTIHVvjKa5iIbLZ5fQ'

# Welcome Message

welcome_message = 'خوش آمدید'

#the command for creating the bot based on the Token that bot father gave us

bot = telepot.Bot(Token)

telegrambotapi  = telegram.Bot(token=Token)

#a list for saving the subjects of quizes

subjects = ['daily',
            'psychology',
            'sport',
            'coocking',
            'electrical_engineering',
            ]

my_user = user.user(user_name= '' , password=randint(100000000, 9999999999) , chat_id=0)

#to understand that bot is working correctly

print(bot.getMe(),'\n')
print('Listening...\n')

def handle(msg):
    global all_ques_of_type
    global my_user
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)
    # my_user = user.user(user_name= msg['chat']['username'] , password=randint(100000000, 9999999999) , chat_id=chat_id)

    if(msg['text'] == '/admin'):
        entry_user_pass(telegrambotapi,chat_id)
        admin.admin.import_questions(telegrambotapi,chat_id)

    if content_type == 'text':
        my_admin = admin.admin()

        if(msg['text'] != '/get_export'):
            my_user = my_admin.display_questions_check_answers(telegrambotapi,chat_id,msg)

            # print(my_user)

        elif(msg['text'] == '/get_export'):
            my_admin.get_export(my_user)
            print('=+=+=+=+=+=+=+=+=+=+')






########################################################################################
########################################################################################
def import_admin():                                                                   ##
    userss['id'] = '37788570'                                                         ##
    userss['user_name'] = 'mohamad_aref'                                              ##
    userss['password'] = '37788570bb'                                                 ##
    try:                                                                              ##
        database_communication.database_communication.save_user_to_db(userss)         ##
    except:                                                                           ##
        print("there is a repeated key!!!")                                           ##
########################################################################################
########################################################################################


def entry_user_pass(telegrambotapi,chat_id):
    my_username = input('enter your username:')
    my_password = input('enter your password:')
    usr = user.user(my_username,my_password,score=0,chat_id = chat_id)
    if(usr.sign_in(telegrambotapi,chat_id) == 0):
        entry_user_pass(telegrambotapi,chat_id)


MessageLoop(bot,handle).run_as_thread()

while 1:
    time.sleep(0.05)
