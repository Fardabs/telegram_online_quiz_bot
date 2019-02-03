# -*- coding: utf-8 -*-
import numpy
import xlsxwriter
from pandas import read_excel
import xlrd
import pandas
import database_communication
import sys
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import time
import re
import requests
from telegram import *
from emoji import emojize
import pprint
from xlrd import *
import matplotlib.pyplot as plt
import user
from random import randint
# from openpyxl import load_workbook
# from PDFWriter import PDFWriter
# from pylovepdf.ilovepdf import ILovePdf

time_limit = 5

all_ques = []

ques_num = 0

my_score = 0

my_FALSE = 0

my_TRUE = 0

number_of_questions = 0

my_user = user.user(user_name= '' , password=randint(100000000, 9999999999) , chat_id=0)

class admin():

    #openning our book of .xlsx
    data = xlrd.open_workbook('data/questions_and_choices.xlsx')


    #a list of all of the sheets' names in the book
    sheet_names = data.sheet_names()

    #a function for importing admin sorted questions
    @classmethod
    def import_questions(cls,bot,chat_id):
        row_num = 1

        col_num = 0

        titles = ['NO','question','choice1','choice2','choice3','choice4','answer','image']

        #a dictionary for saving the subjects and their indexes
        subjects = {}

        for num in range(0,len(cls.sheet_names)):
            subjects[cls.sheet_names[num]] = str(num)
        print(subjects)
        for keys in subjects:
            print(keys)
            sh1 = cls.data.sheet_by_name(keys)
            for row_num in range(1,sh1.nrows):
                my_question = {}
                for col_num in range(0,sh1.ncols):
                    my_question[titles[col_num]] = str(sh1.cell(row_num,col_num).value)
                    if(col_num+1 == sh1.ncols):
                        my_question['category'] = keys

                col_num = 0
                row_num = row_num + 1
                try:
                    database_communication.database_communication.save_questions_to_db(my_question)
                except:
                    print("there is a repeated key!!!")

                del my_question

    @classmethod
    def display_questions_check_answers(cls,bot,chat_id,msg):
        my_admin = admin()

        my_collection = "questions"

        global all_ques

        global ques_num

        global my_score

        global my_FALSE

        global my_TRUE

        global my_user

        subjects = {'daily' : 0,
                    'psychology' : 1,
                    'sport' : 2,
                    'coocking' : 3,
                    'electrical_engineering' : 4
                    }

        if (msg['text'] == '/start'):
            pprint.pprint(msg)
            my_user = user.user(user_name= msg['chat']['first_name'] , password=randint(100000000, 9999999999) , chat_id=chat_id)

            subjects = {'daily' : 0,
                        'psychology' : 1,
                        'sport' : 2,
                        'coocking' : 3,
                        'electrical_engineering' : 4
                        }

            my_keyboard = []

            for keys in subjects:
                my_keyboard.append([KeyboardButton(text = keys)])

            print(my_keyboard)

            bot.sendMessage(chat_id = chat_id,text = 'choose the topic of the exam',
                reply_markup = ReplyKeyboardMarkup(
                keyboard = my_keyboard
                ))
        elif (msg['text'] in subjects.keys()):
            my_entry = {'category' : msg['text']}
            global number_of_questions
            number_of_questions = database_communication.database_communication.count_entry(my_collection,my_entry)
            print(number_of_questions)
            #quesring questions from data base and showing chices to the user
            for num in range(1,number_of_questions+1):
                #quesring on data base ,based on the question number
                my_entry = {'category' : msg['text'] , 'NO' : str(float(num))}

                ques = database_communication.database_communication.read_from_db("questions",my_entry)

                all_ques.append(ques)

                pprint.pprint(all_ques)

                print('******************')
                pprint.pprint(ques)
                print('+++++++++---------')
                #using a regex in order to define choices that contain url addresses
                item  = re.findall("http+.*",ques['choice1'])

                if (ques['choice1'] != 'none' and not item):

                    bot.sendMessage(chat_id = chat_id,text = str(ques['question']),
                    reply_markup = ReplyKeyboardMarkup(
                    keyboard = [[KeyboardButton(text = ques['choice1']),
                        KeyboardButton(text = ques['choice2'])],[
                        KeyboardButton(text = ques['choice3']),
                        KeyboardButton(text = ques['choice4'])]]
                        ))

                    if (ques['image'] != 'none'):
                        bot.send_photo(chat_id=chat_id, photo=ques['image'])

                    time.sleep(time_limit)
                    print('###################')
                    pprint.pprint(msg['text'])
                    print('###################')
                    bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardRemove(selective=True))

                elif (ques['choice1'] == 'none'):

                    bot.sendMessage(chat_id = chat_id,text = str(ques['question']))

                    if (ques['image'] != 'none'):
                        bot.send_photo(chat_id=chat_id, photo=ques['image'])

                    bot.sendMessage(chat_id = chat_id,text = "type your answer:" + emojize(":point_down:", use_aliases=True))

                    time.sleep(time_limit)
                    print('###################')
                    pprint.pprint(msg['text'])
                    print('###################')
                    bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardRemove(selective=True))

                elif (item):

                    bot.sendMessage(chat_id,str(ques['question']) + emojize(":point_down:", use_aliases=True),
                    reply_markup = ReplyKeyboardMarkup(
                    keyboard = [[KeyboardButton(text = str(float(1))),
                        KeyboardButton(text = str(float(2)))],[
                        KeyboardButton(text = str(float(3))),
                        KeyboardButton(text = str(float(4)))]]
                        ))

                    if (ques['image'] != 'none'):
                        bot.send_photo(chat_id=chat_id, photo=ques['image'])

                    for i in range(1,5):
                        image = requests.post(ques['choice'+str(i)])
                        bot.sendMessage(chat_id = chat_id , text = 'image number' + str(i) + emojize(":point_down:", use_aliases=True))
                        bot.send_photo(chat_id=chat_id, photo=ques['choice'+str(i)])



                    time.sleep(time_limit)
                    print('###################')
                    pprint.pprint(msg['text'])
                    print('###################')
                    bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardRemove(selective=True))

                ##############################################################################################

            bot.sendMessage(chat_id,text = 'thank you for taking part in our exam' + emojize(":heart_eyes:", use_aliases=True)+ emojize(" :heart_eyes:", use_aliases=True)+ emojize(" :heart_eyes:", use_aliases=True))
        elif(msg['text'] != '/get_export'):
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            pprint.pprint(msg['text'])
            # print(str(all_ques[ques_num]['answer']))
            if(msg['text'] == all_ques[ques_num]['answer']):
                my_score = my_score + 3
                my_TRUE = my_TRUE + 1
            else:
                my_score = my_score - 1
                my_FALSE = my_FALSE + 1

            ques_num = ques_num + 1

            my_user.set_score(my_score)
            my_user.set_TRUE(my_TRUE)
            my_user.set_FALSE(my_FALSE)

            print(my_user.user_name,': his score : -------->>>>>>>>>>>>>>>>>>>>>',my_user.score,'<<<<<<<<<<<<<<<<----------')
            print('..............',my_user.FALSE,'................')
            print('..............',my_user.TRUE,'................')
            # print('..............',my_user.NOT_ANSWERED,'................')
            print(my_user)
            return my_user



    @classmethod
    def get_export(cls,my_user):

        my_saved_user = {}

        labels = 'TRUE', 'FALSE', 'NA'

        my_user.NOT_ANSWERED = number_of_questions - (my_user.FALSE + my_user.TRUE)

        my_saved_user['user_name']  = my_user.user_name
        my_saved_user['password'] = my_user.password
        my_saved_user['score'] = my_user.score
        my_saved_user['chat_id'] = my_user.chat_id
        my_saved_user['TRUE'] = my_user.TRUE
        my_saved_user['FALSE'] = my_user.FALSE
        my_saved_user['NOT_ANSWERED'] = my_user.NOT_ANSWERED
        try:
            database_communication.database_communication.save_user_to_db(my_saved_user)
        except:
            print('there is a repeated key!!!')
        sizes = [my_user.TRUE, my_user.FALSE, my_user.NOT_ANSWERED]

        explode = (0.1, 0, 0)

        fig1, ax1 = plt.subplots()

        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)

        ax1.axis('equal')

        plt.show()
