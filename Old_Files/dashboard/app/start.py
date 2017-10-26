import pysb

SB = pysb.SbSession()

def questionlogin():
    """This function checks to see if you want to login"""
    print('''
    Would you like to login?
    (Y / N)
    ''')
    answer = input('> ').lower()
    if answer.startswith('y'):
        login()
    elif answer.startswith('n'):
        main()
    else:
        print('''
    I'm sorry, I didn't understand that.''')
        questionlogin()

def login():
    """ This function takes your username and password and transmits using the ScienceBase API. """
    user = input('Username: ')
    SB.loginc(user)
    if SB.is_logged_in():
        print('''
    Login Successful''')
        main()
    else:
        print('''
    Could not log you in to ScienceBase''')

def main():
    """ This function initiates the workflow of either searching or reading specific records """
    print('''
    So what do you want to do?
    1. Search ScienceBase
    2. Specialty tasks
    ''')
    answer = input('> ').lower()
    if answer == '1' or answer == 'search':
        print('You chose search')
        main()
    elif answer == '2' or answer == 'special':
        import specialtyTasks_working3
        specialtyTasks_working3.main()
    else:
        print('''
    Sorry, I didnt' understand that.''')
        main()

#===============================================================================

if __name__ == '__main__':
    questionlogin()

SB.logout()
