# -*- coding: utf-8 -*-
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup,InlineKeyboardButton
import pprint
import database_communication
from emoji import emojize


class user():
    user_name = ''
    password = ''
    score = 0

    @classmethod
    def __init__(cls,user_name,password,chat_id):
        cls.user_name = user_name
        cls.password = password
        cls.score = 0
        cls.chat_id = chat_id
        cls.TRUE = 0
        cls.FALSE = 0
        cls.NOT_ANSWERED = 0

    @classmethod
    def set_score(cls,value):
        cls.score = value

    @classmethod
    def set_TRUE(cls,value):
        cls.TRUE = value

    @classmethod
    def set_FALSE(cls,value):
        cls.FALSE = value

    @classmethod
    def sign_in(cls,bot,chat_id):
        user_info = {}
        user_info = database_communication.database_communication.read_from_db("members",{'user_name' : cls.user_name})
        pprint.pprint(type(user_info))
        if(str(type(user_info)) != "<class 'NoneType'>"):
            if (cls.password == user_info["password"]):
                print('signed in successfully')
                bot.sendMessage(chat_id,text = 'signed in successfully' + emojize(":heart_eyes:", use_aliases=True))
                return 1
            else :
                print('username or password is wrong please try again')
                bot.sendMessage(chat_id,text = 'username or password is wrong please try again'+ emojize(":cry:", use_aliases=True))
                return 0
        else:
                print('username or password is wrong please try again')
                bot.sendMessage(chat_id,text = 'username or password is wrong please try again'+ emojize(":cry:", use_aliases=True))
                return 0


    @classmethod
    def __str__(cls):
        return (cls.user_name+'\n'+str(cls.password)+'\n'+str(cls.score)+'\n'+str(cls.chat_id)+'\n'+str(cls.TRUE)+'\n'+str(cls.FALSE)+'\n'+str(cls.NOT_ANSWERED)+'\n')
