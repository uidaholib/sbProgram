



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
    answer = input('> ').lower()
    if '1' or 'search' in answer:
            import search
            search.search()
    elif '2' or 'special' in answer:
        import specialtyTasks_working3
        specialtyTasks_working3.main()
    else:
        print('''
    Sorry, I didnt' understand that.''')
        main()

#===============================================================================

if __name__ == '__main__':
    questionLogin()

sb.logout()
