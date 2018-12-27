import numpy
import xlsxwriter
from pandas import read_excel
import xlrd
import pandas

# data = xlrd.open_workbook('data/questions_and_choices.xlsx')
# row_num = 0
# col_num = 0
# sh1 = data.sheet_by_index(0)
# print(sh1.ncols)

class admin():
    data = xlrd.open_workbook('data/questions_and_choices.xlsx')


    #a function for importing admin sorted questions
    @classmethod
    def import_questions(cls):
        row_num = 1
        col_num = 0
        sh1 = cls.data.sheet_by_index(0)
        for col_num in range(0,sh1.ncols):
            if(sh1.cell(row_num,col_num).value != 'none'):
                print(sh1.cell(row_num,col_num).value)
            else:
                pass
            




admin.import_questions()
