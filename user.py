from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup,InlineKeyboardButton
import pprint
import database_communication


class user():
    user_name = ''
    password = ''
    score = 0

    @classmethod
    def __init__(cls,user_name,password,score):
        cls.user_name = user_name
        cls.password = password
        cls.score = score


    @classmethod
    def sign_in(cls):
        user_info = {}
        # pprint.pprint("***************")
        # pprint.pprint(database_communication.database_communication.read_from_db("members",cls.user_name))
        # pprint.pprint("***************")
        # print(type(database_communication.database_communication.read_from_db("members",cls.user_name)))
        user_info = database_communication.database_communication.read_from_db("members",cls.user_name)
        pprint.pprint(type(user_info))
        if(str(type(user_info)) != "<class 'NoneType'>"):
            if (cls.password == user_info["password"]):
                print('signed in successfully')
            else :
                print('username or password is wrong please try again')
        else:
                print('username or password is wrong please try again')


    @classmethod
    def answer():
        pass
