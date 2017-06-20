# -*- coding: utf-8 -*-
"""Initial login script for the ScienceBase MACRO/PEON program

This module contains the login functions for the user to log in to ScienceBase
should they need to. It then asks the user whether they are searching
ScienceBase or using other specialty tasks such as parsing and counting of
ScienceBase data and calls the appropriate script.

PEON
Program for Executive/Ease Of and Nuisance
Programmatic Executive and Organization/Operations via Network
Program for Executive Operations via Network
menial executive task
menial assignment and computational relief operator
Macro Architechture for Computational and Reporting/Recording Operations
"""


from pprint import pprint
import json
import requests
import pysb


sb = pysb.SbSession()


def questionLogin():
    """Function asks whether the user wants to log in. If so, it calls login(),
    if not it skips the login and calls main().
    """
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
    """Login function used to prompt the user for a username and password for
    ScienceBase, and using the pysb function loginc() to login to ScienceBase.
    """
    user = input('Username: ')
    sb.loginc(user)
    if sb.is_logged_in():
        print('''
    Login Successful''')
        main()
    else:
        print('''
    Could not log you in to ScienceBase''')


def main():
    """The function that is the main fork from which many of the operations of
    the program can be accessed. It asks if the user wants to search
    ScienceBase or choose from a variety of other tasks.
    """
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

# ===============================================================================


if __name__ == '__main__':
    questionLogin()

sb.logout()
