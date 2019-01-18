import numpy
import xlsxwriter
from pandas import read_excel
import xlrd
import pandas
import database_communication

class admin():
    data = xlrd.open_workbook('data/questions_and_choices.xlsx')


    #a function for importing admin sorted questions
    @classmethod
    def import_questions(cls):
        row_num = 1
        col_num = 0
        titles = ['NO','question','choice1','choice2','choice3','choice4','answer','image']
        sh1 = cls.data.sheet_by_index(0)
        for row_num in range(1,sh1.nrows):
            my_question = {}
            for col_num in range(0,sh1.ncols):
                my_question[titles[col_num]] = str(sh1.cell(row_num,col_num).value)

            # print(my_question)
            col_num = 0
            row_num = row_num + 1
            try:
                database_communication.database_communication.save_questions_to_db(my_question)
            except:
                print("there is a repeated key!!!")

            del my_question
