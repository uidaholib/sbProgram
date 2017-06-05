



import requests
import json
import pysb

from pprint import pprint



sb = pysb.SbSession()



def questionLogin():
    print('''
    Would you like to login?
    (Y / N)
    ''')
    answer = input('> ')
    if 'Y' in answer or 'y' in answer:
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
    if sb.is_logged_in() == True:
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
    2. Specialty tasks
    ''')
    answer = input('> ')
    if '1' in answer or 'Search' in answer or 'search' in answer:
            import search
            search.search()
    elif '2' in answer or 'Special' in answer or 'special' in answer:
        import specialtyTasks_working2
        specialtyTasks_working2.main()
    else:
        print('''
    Sorry, I didnt' understand that.''')
        main()

#===============================================================================

if __name__ == '__main__':
    questionLogin()

sb.logout()
