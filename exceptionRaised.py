import g
import requests
import json
import pysb
import sys
import time

from pprint import pprint

sb = pysb.SbSession()

numOfTries = 0

def main(ProblemID):
    print('''
    Process time:
    ''')
    print(time.process_time())
    print('''
    It looks like we found something that raised a 404 exception. What '''+
    '''would you like to do?
    1. Try waiting
    2. Try logging out
    3. Try loggin in
    4. Add item to a list of items that raised exceptions to be delt with'''+
    ''' later
    (Type number)
    ''')
    answer = input("> ").lower()
    if '1' in answer:
        tryWaiting(ProblemID)
    elif '2' in answer:
        tryLogOut(ProblemID)
    elif '3' in answer:
        tryLogIn(ProblemID)
    elif '4' in answer:
        g.Exceptions.append(ProblemID)
        return
    else:
        print('''
    I didn't get that. Please type a number from the list.''')
        main(ProblemID)


def tryWaiting(ProblemID):
    global numOfTries
    numOfTries += 1
    print("--------Waiting for 404 to reset...")
    time.sleep(300)
    try:
        sb.get_item(ProblemID)
        return
    except Exception:
        print('''
    Looks like that didn't work. Here are your options.''')
        main(ProblemID)

def again(ProblemID):
    print('''
    That did not work.
    We have tried '''+str(numOfTries)+''' time(s). Try again?
    (Y / N)''')
    answer = input("> ").lower()
    if 'y' in answer:
        tryWaiting(ProblemID)
    elif 'n' in answer:
        tryLogOut(ProblemID)
    else:
        print('''
    Sorry, I didn't get that. Please type 'y' or 'n'.
              ''')
        again(ProblemID)

def tryLogOut(ProblemID):
    print('''
    Should we try logging out?
    (Y / N)
    ''')
    answer = input("> ").lower()
    if 'y' in answer:
        sb.logout()
        try:
            sb.get_item(ProblemID)
            print("It worked!")
            return
        except Exception:
            again2(ProblemID)
    elif 'n' in answer:
        tryLogOut(ProblemID)
    else:
        print('''
    Sorry, I didn't get that. Please type 'y' or 'n'.
              ''')
        tryLogOut(ProblemID)

def again2(ProblemID):
    print('''
    Logging out did not work.
    We have tried '''+str(numOfTries)+''' time(s). Try again?
    (Y / N)''')


def addToList(ProblemID):
