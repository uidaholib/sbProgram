import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0

#==============================================================================
#for creating an Excel workbook:
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
#==============================================================================
ChosenFiscalYear = []
L1Project = []
L2DataInProject = []
L3NumSbItemsFound = []
L4DataPerFile = []
L5RunningDataTotal = []
L6NestedData = []
L7MissingData = []
L8MissingDataURL = []
L9Exceptions = []
L10Exceptions_IDs = []
#==============================================================================
def main():
    #clears lists in case they are populated from a previous tally
    ChosenFiscalYear[:] = []
    L1Project[:] = []
    L2DataInProject[:] = []
    L3NumSbItemsFound[:] = []
    L4DataPerFile[:] = []
    L5RunningDataTotal[:] = []
    L6NestedData[:] = []
    L7MissingData[:] = []
    L8MissingDataURL[:] = []
    L9Exceptions[:] = []
    L10Exceptions_IDs[:] = []
    print('''
    What task would you like to perform?
    1. Count ScienceBase data
    2. Edit an item
    ''')
    answer = input('> ').lower()
    if '1' in answer or 'count' in answer or 'data' in answer:
        countSomething()
    elif '2' in answer or 'edit' in answer:
        import edit_Item
        edit_Item.main()
    else:
        print('''
    Sorry, I didnt' understand that. Try typing the number or a keyword.''')
        main()

def countSomething():
    print('''
    What do you want to count data in?
    1. A fiscal year
    2. A project
    3. A single ScienceBase item
    ''')
    answer = input('> ').lower()
    if '1' in answer or 'fiscal' in answer or 'year' in answer:
        yearDataCount()
    elif '2' in answer or 'project' in answer:
        projectDataCount()
    elif '3' in answer or 'item' in answer:
        projectDataCount()
    else:
        print('''
    Sorry, I didnt' understand that. Try typing the number or a keyword.''')
        countSomething()


def projectDataCount(): #finish this later... eyekeeper
    # I need to make it so that the program asks the folder, and then asks the year
    # if user doesn't know the year, or, I guess, even the folder, the program
    # should list all the projects in the folder(s). So the user CAN narrow the
    # choices, or select from them all.
    print('''
    Is the project in the NWCSC folder or the SWCSC folder?
    ''')
    answer = input('> ').lower()
    if 'nwcsc' in answer or 'n' in answer:
        import search
        search.searchNWCSC()
    elif 'swcsc' in answer or 's' in answer:
        import search
        search.searchSWCSC()
    else:
        print('''
    I didn't understand that input. Let's try that again...
              ''')
        PubSearch()

def yearDataCount():
    print('''
    Which folder would you like to get the data from?
    NWCSC folder or the SWCSC folder?
    ''')
    answer = input('> ').lower()
    if 'nwcsc' in answer or 'n' in answer:
        r = sb.get_child_ids('4f8c64d2e4b0546c0c397b46')
        chooseFiscalYear(r)
    elif 'swcsc' in answer or 's' in answer:
        r = sb.get_child_ids('4f8c6580e4b0546c0c397b4e')
        chooseFiscalYear(r)
    else:
        print('''
    I didn't understand that input. Let's try that again...
              ''')
        yearDataCount()

def chooseFiscalYear(r):
    #print(sb.is_logged_in())
    pprint(r)
    print('''
    Here are the fiscal year folders to choose from:
    ''')
    num = 1
    for i in r:
        data = sb.get_item(i)
        print(str(num)+'. '+data['title'])
        num += 1
    print('''
    Now, which fiscal year would you like to count data for?
    (Enter number)
    ''')
    answer = input('> ')
    try:
        val = int(float(answer))
        f = val-1
        folder = r[f]
        doubleCheckNWCSC(folder)

    except ValueError:
        print("That's not a number. Let's try this again.")
        chooseFiscalYear(r)


    #q = sb.get_item(r[0])
    #pprint(q)
    #for i in r:
    #    q = sb.get_child_ids(i)
    #    pprint(q)

def doubleCheckNWCSC(folder):
    r = sb.get_item(folder)
    #pprint(r) #Quantico
    print('''
    Ok, so we're counting the data in '''+r['title']+'''.

    Is that right?
    (Y / N)'''
    )
    answer = input('> ')
    if 'yes' in answer or 'Yes' in answer or 'y' in answer or 'Y' in answer:
        FYdataCount(r, folder)
    elif 'no' in answer or 'No' in answer or 'n' in answer or 'N' in answer:
        print('''
    Ok, let's try this again.''')
        yearDataCountNWCSC()
    else:
        print('''
    Sorry, I didn't understand that. Try typing 'Yes' or 'No' or the first letter of your answer.''')
        doubleCheckNWCSC(folder)

if __name__ == '__main__':
    main()
    #yearDataCountNWCSC()


sb.logout()
