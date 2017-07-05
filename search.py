# -*- coding: utf-8 -*-
"""Base-level Search script for the ScienceBase MACRO program

This module contains the search functions for the user to search ScienceBase in
either the NWCSC folder or the SWCSC folder and print the results of that
search. It gives the user several options to choose from after executing a
search.

1. It allows the user to conduct a different search
2. It can call another script to get more information on a particular result
3. It allows them to go back and login.
4/5. It allows the user to page forward and backward through results, should
those results exist.
6. It offers to call a script to count the data within a result (which first
requires parsing of that result).
7. If the user is logged in, it offers to call a script to edit a result.
"""

import g
import requests
import json
import pysb

from pprint import pprint



sb = pysb.SbSession()



searchUrl = 'http://www.sciencebase.gov/catalog/items?s=Search&q='

searchFormat = '&format=json'
getFormat = '?format=json'
searchFields = '&fields=title'
searchFolderID_NWCSC = '&folderId=4f8c64d2e4b0546c0c397b46'
searchFolderID_SWCSC = '&folderId=4f8c6580e4b0546c0c397b4e'
totalSearchURL = ''

def search():
    if sb.is_logged_in(): # if user is logged in. Same as if sb.is_logged_in == True
        print('''
        Great, let's privately search ScienceBase.
        Do you want to search the NWCSC folder, or the SWCSC folder?''')
        answer = input('> ').lower()
        if 'nwcsc' in answer or 'n' in answer:
            searchNWCSC()
        elif 'swcsc' in answer or 's' in answer:
            searchSWCSC()
        else:
            print('''
        I didn't understand that input. Let's try that again...''')
            search()
    else:
        print('''
        Great, let's publically search ScienceBase.
        Do you want to search the NWCSC folder, or the SWCSC folder?''')
        answer = input('> ').lower()
        if 'nwcsc' in answer or 'n' in answer:
            searchNWCSC()
        elif 'swcsc' in answer or 's' in answer:
            searchSWCSC()
        else:
            print('''
        I didn't understand that input. Let's try that again...''')
            search()

def searchNWCSC():
    print('''
    Alright, we'll search the NWCSC folder.
    What should we search for?''')
    search = input('> ')
    totalSearchURL = searchUrl+search+searchFields+searchFolderID_NWCSC+searchFormat
    searchGET(search, totalSearchURL)

def searchSWCSC():
    print('''
    Alright, we'll search the SWCSC folder.
    What should we search for?''')
    search = input('> ')
    totalSearchURL = searchUrl+search+searchFields+searchFolderID_SWCSC+searchFormat
    searchGET(search, totalSearchURL)

def searchGET(search, totalSearchURL):

    r = requests.get(totalSearchURL)#, auth=(username, password))
    print(str(totalSearchURL))

    print('''
    The server gave me this status code: '''+str(r.status_code))

    parsed_r = r.json()
    # pprint(parsed_r) #Quantico

    total = parsed_r['total']
    print('''
    There are '''+str(total)+''' items that match your search parameters.
    ''')
    searchResults = [] #remember this
    page = 0
    titles = 0
    num = 1
    if total > 20:
        while titles < 20:
            result = sb.get_json(parsed_r['items'][titles]['link']['url'])
            #pprint(result) #Quantico
            if result['hasChildren'] == True:
                try:
                    print(str(num)+'. (Folder)'+str(parsed_r['items'][titles]
                                                    ['title']))
                    searchResults.insert(titles, parsed_r['items'][titles]['link']
                                             ['url'])
                    titles += 1
                    num += 1
                except UnicodeEncodeError:
                    print(str(num)+'. (Folder) [Title Unprintable]')
                    titles += 1
                    num += 1

            elif result['hasChildren'] == False:
                try:
                    print(str(num)+'. (File)'+str(parsed_r['items'][titles]
                                                  ['title']))
                    searchResults.insert(titles, parsed_r['items'][titles]['link']
                                             ['url'])
                    titles += 1
                    num += 1
                except UnicodeEncodeError:
                    print(str(num)+'. (File) [Title Unprintable]')
                    titles += 1
                    num += 1

            else:
                try:
                    print(str(num)+'. (Unknown)'+str(parsed_r['items'][titles]
                                                     ['title']))
                    searchResults.insert(titles, parsed_r['items'][titles]['link']
                                             ['url'])
                    titles += 1
                    num += 1
                except UnicodeEncodeError:
                    print(str(num)+'. (Unknown) [Title Unprintable]')
                    titles += 1
                    num += 1


    else:
        while titles < total:
            result = sb.get_json(parsed_r['items'][titles]['link']['url'])
            #pprint(result) #Quantico
            if result['hasChildren'] == True:
                try:
                    print(str(num)+'. (Folder)'+str(parsed_r['items'][titles]
                                                    ['title']))
                    searchResults.insert(titles, parsed_r['items'][titles]['link']
                                             ['url'])
                    titles += 1
                    num += 1
                except UnicodeEncodeError:
                    print(str(num)+'. (Folder) [Title Unprintable]')
                    titles += 1
                    num += 1

            elif result['hasChildren'] == False:
                try:
                    print(str(num)+'. (File)'+str(parsed_r['items'][titles]
                                                  ['title']))
                    searchResults.insert(titles, parsed_r['items'][titles]['link']
                                             ['url'])
                    titles += 1
                    num += 1
                except UnicodeEncodeError:
                    print(str(num)+'. (File) [Title Unprintable]')
                    titles += 1
                    num += 1

            else:
                try:
                    print(str(num)+'. (Unknown)'+str(parsed_r['items'][titles]
                                                     ['title']))
                    searchResults.insert(titles, parsed_r['items'][titles]['link']
                                             ['url'])
                    titles += 1
                    num += 1
                except UnicodeEncodeError:
                    print(str(num)+'. (Unknown) [Title Unprintable]')
                    titles += 1
                    num += 1
    # print(searchResults) #Quantico
    nowWhat(parsed_r, total, page, searchResults)



def nowWhat(parsed_r, total, page, searchResults): #EXAMINE LATER

    if sb.is_logged_in():
        if total > 20:
            print('''
    Now what would you like to do?
    1. Search again
    2. Get more info about a result (Not yet supported)
    3. Go back to log in
    4. See more results (if total results > 20)
    5. Go back a page of results (if available)
    6. Count Data in a result (Not yet supported)
    7. Edit a result (Not yet supported)
    (Type number)
        ''')
    elif not sb.is_logged_in():
        print('''
    Now what would you like to do?
    1. Search again
    2. Get more info about a result (Not yet supported)
    3. Go back to log in
    4. See more results (if total results > 20)
    5. Go back a page of results (if available)
    6. Count Data in a result (Not yet supported)
    (Type number)
    ''')
    answer = input('> ')
    if '1' in answer:
        search()
    elif '2' in answer:
        investigateResult(parsed_r)
    elif '3' in answer:
        import start
        start.questionLogin()
    elif '4' in answer:
        more(parsed_r, total, page)
    elif '5' in answer:
        back(parsed_r, total, page)
    elif '6' in answer:
        import specialtyTasks
        specialtyTasks.resultDataCount(parsed_r)
    elif '7' in answer and sb.is_logged_in():
        editResult(parsed_r)
    else:
        print('''
    I don't understand what you meant. Please type a number provided.
    ''')
        nowWhat(parsed_r, total, page, searchResults)

def investigateResult(parsed_r):
    print('''
    Which result would you like to delve into?
    (Type the number of the result)
    ''')
    Answer = input('> ')
    investNum = int(Answer)-1
    investUrl = parsed_r['items'][investNum]['link']['url']+getFormat
    print(str(investUrl))
    r_i = requests.get(investUrl)#, auth=(username, password))

    print('''
    The server gave me this status code: '''+str(r_i.status_code))
    parsed_r_i = r_i.json()
    pprint(parsed_r_i)



def more(parsed_r, total, page):

    try:
        print(parsed_r['nextlink']['url'])
        parsed_r['nextlink']
    except KeyError:
        morePages = False
    else:
        morePages = True
    if morePages is True:
        r = requests.get(parsed_r['nextlink']['url'])#, auth=(username, password)))

        print('''
        The server gave me this status code: '''+str(r.status_code))
        #with open(r.json()) as f:
        #    z = json.load(r.json()).read()
        parsed_r = r.json()
        #pprint(parsed_r) #Quantico
        #print '"items":', parsed_r['"title"']
        total = parsed_r['total']
        print('''
        There are '''+str(total)+''' items that match your search parameters.
        ''')
        searchResults = [] #remember this
        page += 1
        titles = 0
        num = 1
        if page > 0:
            num += (page*20)

        if total > ((page*20)+20):
            while titles < 20:
                result = sb.get_json(parsed_r['items'][titles]['link']['url'])
                #pprint(result) #Quantico
                if result['hasChildren'] is True:
                    try:
                        print(str(num)+'. (Folder)'+str(parsed_r['items'][titles]
                                                        ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Folder) [Title Unprintable]')
                        titles += 1
                        num += 1

                elif result['hasChildren'] == False:
                    try:
                        print(str(num)+'. (File)'+str(parsed_r['items'][titles]
                                                      ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (File) [Title Unprintable]')
                        titles += 1
                        num += 1

                else:
                    try:
                        print(str(num)+'. (Unknown)'+str(parsed_r['items'][titles]
                                                         ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Unknown) [Title Unprintable]')
                        titles += 1
                        num += 1

        else:
            while titles < (total-(page*20)):
                result = sb.get_json(parsed_r['items'][titles]['link']['url'])
                #pprint(result) #Quantico
                if result['hasChildren'] == True:
                    try:
                        print(str(num)+'. (Folder)'+str(parsed_r['items'][titles]
                                                        ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Folder) [Title Unprintable]')
                        titles += 1
                        num += 1

                elif result['hasChildren'] == False:
                    try:
                        print(str(num)+'. (File)'+str(parsed_r['items'][titles]
                                                      ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (File) [Title Unprintable]')
                        titles += 1
                        num += 1

                else:
                    try:
                        print(str(num)+'. (Unknown)'+str(parsed_r['items'][titles]
                                                         ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Unknown) [Title Unprintable]')
                        titles += 1
                        num += 1
        #print searchResults #Quantico
        nowWhat(parsed_r, total, page, searchResults)
    elif morePages is False:
        print('''
    I'm sorry, there don't appear to be any more items''')
        nowWhat(parsed_r, total, page, searchResults)
    else:
        '''
    Whoops. Something went wrong.'''
        nowWhat(parsed_r, total, page, searchResults)


def back(parsed_r, total, page):

    try:
        print(parsed_r['prevlink']['url'])
        parsed_r['prevlink']
    except KeyError:
        morePages = False
    else:
        morePages = True
    if morePages is True:
        r = requests.get(parsed_r['prevlink']['url'])#, auth=(username, password)))

        print('''
        The server gave me this status code: '''+str(r.status_code))
        #with open(r.json()) as f:
        #    z = json.load(r.json()).read()
        parsed_r = r.json()
        #pprint(parsed_r) #Quantico
        #print '"items":', parsed_r['"title"']
        total = parsed_r['total']
        print('''
        There are '''+str(total)+''' items that match your search parameters.
        ''')
        searchResults = [] #remember this
        page -= 1
        titles = 0
        num = 1
        if page > 0:
            num += (page*20)

        if total > ((page*20)+20):
            while titles < 20:
                result = sb.get_json(parsed_r['items'][titles]['link']['url'])
                #pprint(result) #Quantico
                if result['hasChildren'] == True:
                    try:
                        print(str(num)+'. (Folder)'+str(parsed_r['items'][titles]
                                                        ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Folder) [Title Unprintable]')
                        titles += 1
                        num += 1

                elif result['hasChildren'] == False:
                    try:
                        print(str(num)+'. (File)'+str(parsed_r['items'][titles]
                                                      ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (File) [Title Unprintable]')
                        titles += 1
                        num += 1

                else:
                    try:
                        print(str(num)+'. (Unknown)'+str(parsed_r['items'][titles]
                                                         ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Unknown) [Title Unprintable]')
                        titles += 1
                        num += 1

        else:
            while titles < (total-(page*20)):
                result = sb.get_json(parsed_r['items'][titles]['link']['url'])
                #pprint(result) #Quantico
                if result['hasChildren'] == True:
                    try:
                        print(str(num)+'. (Folder)'+str(parsed_r['items'][titles]
                                                        ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Folder) [Title Unprintable]')
                        titles += 1
                        num += 1

                elif result['hasChildren'] == False:
                    try:
                        print(str(num)+'. (File)'+str(parsed_r['items'][titles]
                                                      ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (File) [Title Unprintable]')
                        titles += 1
                        num += 1

                else:
                    try:
                        print(str(num)+'. (Unknown)'+str(parsed_r['items'][titles]
                                                         ['title']))
                        searchResults.insert(titles, parsed_r['items'][titles]['link']
                                                 ['url'])
                        titles += 1
                        num += 1
                    except UnicodeEncodeError:
                        print(str(num)+'. (Unknown) [Title Unprintable]')
                        titles += 1
                        num += 1
        #print searchResults #Quantico
        nowWhat(parsed_r, total, page, searchResults)
    elif morePages is False:
        print('''
    Sorry, you are already on the first 20 results, there are no more before this.''')
        nowWhat(parsed_r, total, page, searchResults)

    else:
        '''
    Whoops. Something went wrong.'''
        nowWhat(parsed_r, total, page, searchResults)


def editResult(parsed_r):
    pass

if __name__ == '__main__':
    search()

sb.logout()
