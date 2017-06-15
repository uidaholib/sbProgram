# -*- coding: utf-8 -*-
"""Initial login script for the ScienceBase MACRO program

This module contains the login functions for the user to log in to ScienceBase
should they need to. It then asks the user whether they are searching
ScienceBase or using other specialty tasks such as parsing and counting of
ScienceBase data and calls the appropriate script.

PEON
Program for Executive/Ease Of and Nuisance
menial executive task
menial assignment and computational relief operator
Macro Architechture for Computational and Reporting/Recording Operations
"""


from pprint import pprint
import requests
import json
import pysb





sb = pysb.SbSession()



def questionLogin():
    print('''
    Would you like to login?
    (Y / N)
    ''')
    answer = input('> ').lower()
    if answer.startswith('y'):
        login()
    elif 'N' in answer or 'n' in answer:
        main()
    else:
        print('''
    I'm sorry, I didn't understand that.''')
        questionLogin()

def login():
    user = input('Username: ')
    sb.loginc(user)
    if sb.is_logged_in(): # if user is logged in. Same as if sb.is_logged_in == True
        print('''
    Login Successful''')
        main()
    else:
        print('''
    Could not log you in to ScienceBase''')

def main():
    print('''
    So what do you want to do?
    1. Search ScienceBase
    2. Other Tasks
    ''')
    answer = input('> ').lower()
    if '1' in answer or 'search' in answer:
        import search
        search.search()
    elif '2' in answer or 'special' in answer:
        import tasks
        tasks.main()
    else:
        print('''
    Sorry, I didnt' understand that.''')
        main()

#===============================================================================

if __name__ == '__main__':
    questionLogin()

sb.logout()
