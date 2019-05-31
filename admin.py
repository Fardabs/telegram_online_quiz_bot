# -*- coding: utf-8 -*-
import os
import numpy
import xlsxwriter
from pandas import read_excel
import xlrd
import pandas
import database_communication
import sys
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
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
from threading import Timer
import config

time_limit = int(config.conf['time_limit'])

all_ques = []

ques_num = 0

my_score = 0

my_FALSE = 0

my_TRUE = 0

number_of_questions = 0

users = {}

done = 0

start = 0

subjects = {}

# my_user = user.user(user_name= '' , password=randint(100000000, 9999999999) , chat_id=0)

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

        global done

        global start

        my_collection = "questions"

        global all_ques

        global users

        global ques_num

        global my_score

        global my_FALSE

        global my_TRUE

        global subjects

        done = time.time()

        elapsed = done - start

        elapsed = int(elapsed)

        if (msg['text'] == '/start'):
            users[ msg['chat']['id'] ]  = {}
            pprint.pprint(msg)
            my_user = user.user(user_name= msg['chat']['first_name'] , password=randint(100000000, 9999999999) , chat_id=chat_id)

            for num in range(0,len(cls.sheet_names)):
                subjects[cls.sheet_names[num]] = str(num)

            my_keyboard = []
            pprint.pprint(subjects)
            for keys in subjects:
                my_keyboard.append([KeyboardButton(text = keys)])

            print(my_keyboard)

            bot.sendMessage(chat_id = chat_id,text = 'time for answering each question is : ' + str(time_limit) + ' sec')

            bot.sendMessage(chat_id = chat_id,text = 'choose the topic of the exam',
                reply_markup = ReplyKeyboardMarkup(
                keyboard = my_keyboard
                ))
        elif (msg['text'] in subjects.keys()):
            try:
                existed_member = database_communication.database_communication.read_from_db("members",{'chat_id': msg['chat']['id']})
                #this condition below checks if the user has ever participated in this category of exam or not if he hasn't participated the users dictionary will be initialized and the first question will come up
                if msg['text'] not in existed_member['category'].keys():
                    users[ msg['chat']['id'] ] ['cat'] = msg['text']
                    users[ msg['chat']['id'] ] ['qnum'] = 1
                    users[ msg['chat']['id'] ] ['score'] = 0
                    users[ msg['chat']['id'] ] ['true'] = 0
                    users[ msg['chat']['id'] ] ['false'] = 0
                    users[ msg['chat']['id'] ] ['flag'] = 0
                    print('|##|$|$|$|#|$|#|$|#|$|#$|#')
                    prevques = database_communication.database_communication.read_from_db("questions",{'category' : users[ msg['chat']['id'] ] ['cat'] , 'NO' : str(float(users[ msg['chat']['id'] ] ['qnum'])) })
                    try:
                        #using a regex in order to define choices that contain url addresses
                        item  = re.findall("http+.*",prevques['choice1'])
                    except:
                        print('exam is finished!')
                    if (prevques['choice1'] != 'none' and not item):

                        bot.sendMessage(chat_id = chat_id,text = str(prevques['question']),
                        reply_markup = ReplyKeyboardMarkup(
                        keyboard = [[KeyboardButton(text = prevques['choice1']),
                            KeyboardButton(text = prevques['choice2'])],[
                            KeyboardButton(text = prevques['choice3']),
                            KeyboardButton(text = prevques['choice4'])]]
                            ))

                        if (prevques['image'] != 'none'):
                            bot.send_photo(chat_id=chat_id, photo=prevques['image'])

                        start = time.time()

                        time.sleep(time_limit)

                        bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))

                    elif (prevques['choice1'] == 'none'):

                        bot.sendMessage(chat_id = chat_id,text = str(prevques['question']))

                        if (prevques['image'] != 'none'):
                            bot.send_photo(chat_id=chat_id, photo=prevques['image'])

                        bot.sendMessage(chat_id = chat_id,text = "type your answer:" + emojize(":point_down:", use_aliases=True))

                        start = time.time()

                        time.sleep(time_limit)

                        bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))


                    elif (item):

                        bot.sendMessage(chat_id,str(prevques['question']) + emojize(":point_down:", use_aliases=True),
                        reply_markup = ReplyKeyboardMarkup(
                        keyboard = [[KeyboardButton(text = str(float(1))),
                            KeyboardButton(text = str(float(2)))],[
                            KeyboardButton(text = str(float(3))),
                            KeyboardButton(text = str(float(4)))]]
                            ))

                        if (prevques['image'] != 'none'):
                            bot.send_photo(chat_id=chat_id, photo=prevques['image'])

                        for i in range(1,5):
                            image = requests.post(prevques['choice'+str(i)])
                            bot.sendMessage(chat_id = chat_id , text = 'image number' + str(i) + emojize(":point_down:", use_aliases=True))
                            bot.send_photo(chat_id=chat_id, photo=prevques['choice'+str(i)])



                        start = time.time()

                        time.sleep(time_limit)

                        bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))

                else:
                    bot.sendMessage(chat_id = chat_id,text = "Sorry to say that but you've once participated in this category of exam!!" + emojize(":pensive:", use_aliases=True) + emojize(":pensive:", use_aliases=True) + emojize(":pensive:", use_aliases=True) ,reply_markup = ReplyKeyboardRemove(selective=True))

            except:
                users[ msg['chat']['id'] ] ['cat'] = msg['text']
                users[ msg['chat']['id'] ] ['qnum'] = 1
                users[ msg['chat']['id'] ] ['score'] = 0
                users[ msg['chat']['id'] ] ['true'] = 0
                users[ msg['chat']['id'] ] ['false'] = 0
                users[ msg['chat']['id'] ] ['flag'] = 0
                print('|##|$|$|$|#|$|#|$|#|$|#$|#')
                prevques = database_communication.database_communication.read_from_db("questions",{'category' : users[ msg['chat']['id'] ] ['cat'] , 'NO' : str(float(users[ msg['chat']['id'] ] ['qnum'])) })
                try:
                    #using a regex in order to define choices that contain url addresses
                    item  = re.findall("http+.*",prevques['choice1'])
                except:
                    print('exam is finished!')
                if (prevques['choice1'] != 'none' and not item):

                    bot.sendMessage(chat_id = chat_id,text = str(prevques['question']),
                    reply_markup = ReplyKeyboardMarkup(
                    keyboard = [[KeyboardButton(text = prevques['choice1']),
                        KeyboardButton(text = prevques['choice2'])],[
                        KeyboardButton(text = prevques['choice3']),
                        KeyboardButton(text = prevques['choice4'])]]
                        ))

                    if (prevques['image'] != 'none'):
                        bot.send_photo(chat_id=chat_id, photo=prevques['image'])

                    start = time.time()

                    time.sleep(time_limit)

                    bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))

                elif (prevques['choice1'] == 'none'):

                    bot.sendMessage(chat_id = chat_id,text = str(prevques['question']))

                    if (prevques['image'] != 'none'):
                        bot.send_photo(chat_id=chat_id, photo=prevques['image'])

                    bot.sendMessage(chat_id = chat_id,text = "type your answer:" + emojize(":point_down:", use_aliases=True))

                    start = time.time()

                    time.sleep(time_limit)

                    bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))


                elif (item):

                    bot.sendMessage(chat_id,str(prevques['question']) + emojize(":point_down:", use_aliases=True),
                    reply_markup = ReplyKeyboardMarkup(
                    keyboard = [[KeyboardButton(text = str(float(1))),
                        KeyboardButton(text = str(float(2)))],[
                        KeyboardButton(text = str(float(3))),
                        KeyboardButton(text = str(float(4)))]]
                        ))

                    if (prevques['image'] != 'none'):
                        bot.send_photo(chat_id=chat_id, photo=prevques['image'])

                    for i in range(1,5):
                        image = requests.post(prevques['choice'+str(i)])
                        bot.sendMessage(chat_id = chat_id , text = 'image number' + str(i) + emojize(":point_down:", use_aliases=True))
                        bot.send_photo(chat_id=chat_id, photo=prevques['choice'+str(i)])



                    start = time.time()

                    time.sleep(time_limit)

                    bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))

            ##############################################################################################

        #this condition is just used for debugging
        elif(msg['text'] == '/all_users'):
            pprint.pprint(users)

        elif(msg['text'] != '/start' or msg['text'] != '/all_users' or msg['text'] not in subjects.keys() or msg['text'] != '/admin' or msg['text'] != 'CONTINUE EXAM') :
            global number_of_questions
            number_of_questions = database_communication.database_communication.count_entry(my_collection,{ "category" : users[ msg['chat']['id'] ] ['cat']})

            #quesring questions from data base and showing chices to the user
            #quesring on data base ,based on the question number
            if(users[ msg['chat']['id'] ] ['qnum'] < number_of_questions + 1):
                print('{{{{{{{{{{{{{{{{{{{@@@@@@@@@@@@@@}}}}}}}}}}}}}}}}}}}')
                print('flag : ' + str(users[ msg['chat']['id'] ] ['flag']))
                print('msg : ' + str(msg['text']))
                print('{{{{{{{{{{{{{{{{{{{@@@@@@@@@@@@@@}}}}}}}}}}}}}}}}}}}')

                prevques = database_communication.database_communication.read_from_db("questions",{'category' : users[ msg['chat']['id'] ] ['cat'] , 'NO' : str(float(users[ msg['chat']['id'] ] ['qnum'])) })
                nextques = database_communication.database_communication.read_from_db("questions",{'category' : users[ msg['chat']['id'] ] ['cat'] , 'NO' : str(float(users[ msg['chat']['id'] ] ['qnum']+1)) })
                # if users[ msg['chat']['id'] ] ['flag'] == 0:
                #
                #     users[ msg['chat']['id'] ] ['flag'] = 1
                #
                #     users[ msg['chat']['id'] ] ['qnum'] += 1

                if(elapsed <= time_limit):
                    if(msg['text'] == prevques['answer']):
                        pprint.pprint('^^^^^^^^^^^^^^^^^^^^^')
                        users[ msg['chat']['id'] ] ['score'] = users[ msg['chat']['id'] ] ['score'] + 3
                        users[ msg['chat']['id'] ] ['true'] = users[ msg['chat']['id'] ] ['true'] + 1

                    else:
                        pprint.pprint('^@^@^@^@^@^@^@^@^@^@^@^@')
                        users[ msg['chat']['id'] ] ['score'] = users[ msg['chat']['id'] ] ['score'] - 1
                        users[ msg['chat']['id'] ] ['false'] = users[ msg['chat']['id'] ] ['false'] + 1

                else:
                    bot.sendMessage(chat_id=chat_id,text = 'time for answering this question is finished' + emojize(":sob:", use_aliases=True) + emojize(":sob:", use_aliases=True) + emojize(":sob:", use_aliases=True))


                pprint.pprint(users[ msg['chat']['id'] ] ['score'])

                if(users[ msg['chat']['id'] ] ['qnum'] != number_of_questions):
                    try:
                        #using a regex in order to define choices that contain url addresses
                        item  = re.findall("http+.*",nextques['choice1'])
                    except:
                        print('exam is finished!')
                    if (nextques['choice1'] != 'none' and not item):

                        bot.sendMessage(chat_id = chat_id,text = str(nextques['question']),
                        reply_markup = ReplyKeyboardMarkup(
                        keyboard = [[KeyboardButton(text = nextques['choice1']),
                            KeyboardButton(text = nextques['choice2'])],[
                            KeyboardButton(text = nextques['choice3']),
                            KeyboardButton(text = nextques['choice4'])]]
                            ))

                        if (nextques['image'] != 'none'):
                            bot.send_photo(chat_id=chat_id, photo=nextques['image'])



                        start = time.time()

                        time.sleep(time_limit)

                        print('###################')
                        pprint.pprint(msg['text'])
                        print('###################')
                        bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))


                    elif (nextques['choice1'] == 'none'):

                        bot.sendMessage(chat_id = chat_id,text = str(nextques['question']))

                        if (nextques['image'] != 'none'):
                            bot.send_photo(chat_id=chat_id, photo=nextques['image'])

                        bot.sendMessage(chat_id = chat_id,text = "type your answer:" + emojize(":point_down:", use_aliases=True))



                        start = time.time()

                        time.sleep(time_limit)

                        print('###################')
                        pprint.pprint(msg['text'])
                        print('###################')
                        bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))

                    elif (item):

                        bot.sendMessage(chat_id,str(nextques['question']) + emojize(":point_down:", use_aliases=True),
                        reply_markup = ReplyKeyboardMarkup(
                        keyboard = [[KeyboardButton(text = str(float(1))),
                            KeyboardButton(text = str(float(2)))],[
                            KeyboardButton(text = str(float(3))),
                            KeyboardButton(text = str(float(4)))]]
                            ))

                        if (nextques['image'] != 'none'):
                            bot.send_photo(chat_id=chat_id, photo=nextques['image'])


                        for i in range(1,5):
                            image = requests.post(nextques['choice'+str(i)])
                            bot.sendMessage(chat_id = chat_id , text = 'image number' + str(i) + emojize(":point_down:", use_aliases=True))
                            bot.send_photo(chat_id=chat_id, photo=nextques['choice'+str(i)])



                        start = time.time()

                        time.sleep(time_limit)

                        print('###################')
                        pprint.pprint(msg['text'])
                        print('###################')
                        bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'CONTINUE EXAM')]]))

                        # bot.sendMessage(chat_id,text = emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True) + 'Time finished' + emojize(":x:", use_aliases=True) + emojize(":x:", use_aliases=True),reply_markup = ReplyKeyboardRemove(selective=True))

                    ##############################################################################################
                # else:
                #     bot.sendMessage(chat_id = chat_id , text = 'EXAM EXPIRED')

                users[ msg['chat']['id'] ] ['qnum'] = users[ msg['chat']['id'] ] ['qnum'] + 1

            if(users[ msg['chat']['id'] ] ['qnum'] == number_of_questions + 1):
                bot.sendMessage(chat_id,text = 'thank you for taking part in our exam' + emojize(":heart_eyes:", use_aliases=True)+ emojize(" :heart_eyes:", use_aliases=True)+ emojize(" :heart_eyes:", use_aliases=True),reply_markup = ReplyKeyboardRemove(selective=True))
                bot.sendMessage(chat_id,text = 'your score is : ' + str(users[ msg['chat']['id'] ] ['score']) + '/' + str(number_of_questions * 3))
                users[ msg['chat']['id'] ] ['qnum'] = users[ msg['chat']['id'] ] ['qnum'] + 1
                my_user = user.user(user_name= msg['chat']['first_name'] , password=randint(100000000, 9999999999) , chat_id=chat_id)

                my_saved_user = {}

                my_saved_user['category'] = {}

                my_saved_user['category'][users[ msg['chat']['id'] ] ['cat']] = {}

                NOT_ANSWERED = number_of_questions - (users[ msg['chat']['id'] ] ['false'] + users[ msg['chat']['id'] ] ['true'])

                my_saved_user['category'][users[ msg['chat']['id'] ] ['cat']] = {}

                my_saved_user['user_name']  = my_user.user_name
                my_saved_user['password'] = my_user.password
                my_saved_user['category'][users[ msg['chat']['id'] ] ['cat']]['SCORE'] =  users[ msg['chat']['id'] ] ['score']
                my_saved_user['category'][users[ msg['chat']['id'] ] ['cat']]['TRUE'] = users[ msg['chat']['id'] ] ['true']
                my_saved_user['category'][users[ msg['chat']['id'] ] ['cat']]['FALSE'] = users[ msg['chat']['id'] ] ['false']
                my_saved_user['category'][users[ msg['chat']['id'] ] ['cat']]['NOT_ANSWERED'] = NOT_ANSWERED
                my_saved_user['chat_id'] = msg['chat']['id']

                try:
                    database_communication.database_communication.save_user_to_db(my_saved_user)
                except:
                    print('there is a repeated key!!!')

                    existed_member = database_communication.database_communication.read_from_db("members",{'chat_id': my_saved_user['chat_id']})

                    if users[ msg['chat']['id'] ] ['cat'] not in existed_member['category'].keys():

                        myquery = {}

                        newvalues = {}

                        newvalues['category'] = {}

                        myquery['chat_id'] = my_saved_user['chat_id']

                        newvalues['category'] = existed_member['category']
                        print('|||||||||||||||||||||||||||||||||')
                        pprint.pprint(newvalues['category'])
                        print('|||||||||||||||||||||||||||||||||')
                        newvalues['category'][users[ msg['chat']['id'] ] ['cat']] = {'SCORE':users[ msg['chat']['id'] ] ['score'] , 'TRUE':users[ msg['chat']['id'] ] ['true'] , 'FALSE' : users[ msg['chat']['id'] ] ['false'] , 'NOT_ANSWERED' : NOT_ANSWERED}

                        database_communication.database_communication.update(newvalues,myquery)

                return users[ msg['chat']['id'] ]

            # users[ msg['chat']['id'] ] ['qnum'] = users[ msg['chat']['id'] ] ['qnum'] + 1





    @classmethod
    def get_export(cls,bot,msg,chat_id,my_user):

        global users

        existed_member = database_communication.database_communication.read_from_db("members",{'chat_id': msg['chat']['id']})

        my_keyboard = []

        for button in existed_member['category'].keys():
            my_keyboard.append([InlineKeyboardButton(text=button, callback_data=button)])

        keyboard = InlineKeyboardMarkup(inline_keyboard = my_keyboard)

        bot.sendMessage(chat_id, 'Choose desired bilan', reply_markup=keyboard)

    @classmethod
    def calculate(cls,bot,msg,chat_id,desired):

        labels = 'TRUE', 'FALSE', 'NA'

        DESIRED_user = {}

        DESIRED_user [ chat_id ] = database_communication.database_communication.read_from_db("members",{'chat_id': chat_id})

        DESIRED_user [ chat_id ] [ 'TRUE_num' ] = DESIRED_user [ chat_id ] ['category'][desired]['TRUE']

        DESIRED_user [ chat_id ] [ 'FALSE_num' ] = DESIRED_user [ chat_id ] ['category'][desired]['FALSE']

        DESIRED_user [ chat_id ] [ 'NOT_ANSWERED_num' ] = DESIRED_user [ chat_id ] ['category'][desired]['NOT_ANSWERED']

        sizes = [DESIRED_user [ chat_id ] [ 'TRUE_num' ], DESIRED_user [ chat_id ] [ 'FALSE_num' ], DESIRED_user [ chat_id ] [ 'NOT_ANSWERED_num' ]]

        explode = (0.1, 0, 0)

        fig1, ax1 = plt.subplots()

        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)

        ax1.axis('equal')

        plt.savefig('./diagrams/result.png')

        bot.send_photo(chat_id=chat_id,photo=open('./diagrams/result.png' , 'rb'))

        bot.sendMessage(chat_id=chat_id,text='GREEN : NOT_ANSWERED\n\nORANGE : FALSE\n\nBLUE :‌ TRUE\n\n')

        os.remove("./diagrams/result.png")
