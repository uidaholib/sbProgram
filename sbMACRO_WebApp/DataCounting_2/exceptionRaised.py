import gl
import requests
import json
import pysb
import sys
import time

from pprint import pprint

sb = pysb.SbSession()

worked = None
waitTries = 0

def main(ProblemID):
    global waitTries
    waitTries = 0
    question(ProblemID)

def question(ProblemID):
    global waitTries
    global worked
    print('''
    Process time:
    ''')
    print(time.process_time())
    print('''
    It looks like we found something that raised a 404 exception. This '''+
    '''is usually caused when too many requests are made of a server in too'''+
    ''' short of a time. What would you like to do?
    1. Try waiting 5 minutes (This often solves the problem.)
    2. Try waiting for user-specified time.
    3. Try logging out
    4. Try loggin in
    5. Add item to a list of items that raised exceptions to be delt with'''+
    ''' later
    6. Try accessing item again
    (Type number)
    ''')
    # answer = input("> ").lower()
    if waitTries < 2:
        answer = '1'
    else:
        answer = '5'
    if '1' in answer:
        tryWaiting(ProblemID)
    elif '2' in answer:
        tryWaiting2(ProblemID)
    elif '3' in answer:
        tryLogOut(ProblemID)
    elif '4' in answer:
        tryLogIn(ProblemID)
    elif '5' in answer:
        if ProblemID not in g.Exceptions:
            g.Exceptions.append(ProblemID)
            print('Item added to the Exceptions List.')
        else:
            print("Item already in the Exceptions List.")
        worked = False
        return
    elif '6' in answer:
        try:
            sb.get_item(ProblemID)
            print("It worked!")
            worked = True
            return
        except Exception:
            print('''
        Looks like that didn't work. Here are your options again.''')
            question(ProblemID)
    else:
        print('''
    I didn't get that. Please type a number from the list.''')
        question(ProblemID)


def tryWaiting(ProblemID):
    global waitTries
    global worked
    waitTries += 1
    print("--------Waiting for 404 to reset...")
    #time.sleep(300)
    t = 300
    countdown(t)
    try:
        sb.get_item(ProblemID)
        print("It worked!")
        worked = True
        return
    except Exception:
        print('''
    Looks like that didn't work. Here are your options again.''')
        question(ProblemID)


def tryWaiting2(ProblemID):
    global worked
    print('''
    How long would you like to wait (in minutes)?
    ''')
    try:
        minutes = float(str(input('> ')))
    except ValueError:
        print('Please type a number.')
        tryWaiting2(ProblemID)
    print("--------Waiting for 404 to reset...")
    #time.sleep(300)
    t = int(minutes * 60)
    countdown(t)
    try:
        sb.get_item(ProblemID)
        print("It worked!")
        worked = True
        return
    except Exception:
        print('''
    Looks like that didn't work. Here are your options again.''')
        question(ProblemID)

def countdown(t): # in seconds
    for remaining in range(t, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rComplete!            \n")


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
    sb.logout()
    time.sleep(10)
    try:
        sb.get_item(ProblemID)
        print("It worked!")
        return
    except Exception:
        print('''
    Looks like that didn't work. Here are your options again.''')
        question(ProblemID)

def tryLogIn(ProblemID):
    user = input('Username: ')
    sb.loginc(user)
    if sb.is_logged_in():
        print('''
    Login Successful''')
        try:
            sb.get_item(ProblemID)
            print("It worked!")
            return
        except Exception:
            print('''
        Looks like that didn't work. Here are your options again.''')
            question(ProblemID)
    else:
        print('''
    Could not log you in to ScienceBase''')
        try:
            sb.get_item(ProblemID)
            print("It worked anyway!")
            return
        except Exception:
            print('''
        Looks like that didn't work. Here are your options again.''')
            question(ProblemID)

if __name__ == '__main__':
    ProblemID = "561bf56fe4b0cdb063e5837f"
    main(ProblemID)
    #t = 300
    #countdown(t)
