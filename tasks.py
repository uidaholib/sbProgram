import g
import json
import requests
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0

# ==============================================================================
# for creating an Excel workbook:
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
# ==============================================================================
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
# ==============================================================================


def main():
    """The starting function for the "tasks" script that clears the lists
    necessary for parsing and counting data. It asks the user if they want to
    count or edit data.
    """
    # clears lists in case they are populated from a previous tally
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
    2. Edit an item (Not yet supported)
    ''')
    answer = input('> ').lower()
    if '1' in answer or 'count' in answer or 'data' in answer:
        countSomething()
    elif '2' in answer or 'edit' in answer:
        import edit_Item # eyekeeper
        edit_Item.main()
    else:
        print('''
    Sorry, I didnt' understand that. Try typing the number or a keyword.''')
        main()


def countSomething():
    """Should the user want to count data, this function asks for what the user
    would like to count data.
    """
    print('''
    What do you want to count data in?
    1. A fiscal year
    2. A project (Not yet supported)
    3. A single ScienceBase item (Not yet supported)
    4. Excel Spreadsheet (Not yet supported)
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


def projectDataCount():  # finish this later... eyekeeper
    # I need to make it so that the program asks the folder, and then asks the
    # year if user doesn't know the year, or, I guess, even the folder, the
    # program should list all the projects in the folder(s). So the user CAN
    # narrow the choices, or select from them all.
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
        projectDataCount()


def yearDataCount():
    """Function asks what CSC folder the user wants to count data for and uses
    that answer to set the variable "r" to an array containing the child item
    ids of the selected folder. It then calls the function chooseFiscalYear()
    and passes it the "r" variable.
    """
    print('''
    Which folder would you like to get the data from:
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
    """This function prints out the available fiscal years for the chosen CSC
    and asks the user to pick the one to be parsed and whose data will be
    counted. After a choice is made, it calls doubleCheckFY(), passing it "r" and
    the new variable "folder" that is the item ID of the selected fiscal year.
    """
    # print(sb.is_logged_in()) # Quantico
    # pprint(r) # Quantico
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
        folder = []  # This has to be a list to parse correctly
        folder.append(r[f])
        g.itemsToBeParsed.append(r[f])
        doubleCheckFY(r, folder)

    except ValueError:
        print("That's not a number. Let's try this again.")
        chooseFiscalYear(r)


def doubleCheckFY(old_r, folder):
    """This function confirms the fiscal year choice from the previous function.
    If confirmed, it calls the parse.py script to begin parsing the data. If
    unconfirmed, it calls chooseFiscalYear() again.
    """
    r = sb.get_item(folder[0])
    # pprint(r) #Quantico
    print('''
    Ok, so we're counting the data in '''+r['title']+'''.

    Is that right?
    (Y / N)
    ''')
    answer = input('> ').lower()
    if 'yes' in answer or 'y' in answer:
        print("What I'm sending over: ")  # Quantico
        print(folder)  # Quantico
        print(g.itemsToBeParsed)
        import parse
        parse.main()
    elif 'no' in answer or 'n' in answer:
        print('''
    Ok, let's try this again.''')
        chooseFiscalYear(old_r)
    else:
        print('''
    Sorry, I didn't understand that. Try typing 'Yes' or 'No' or the first''' +
              ''' letter of your answer.''')
        doubleCheckFY(old_r, folder)


if __name__ == '__main__':
    main()
    # yearDataCountNWCSC()


sb.logout()
