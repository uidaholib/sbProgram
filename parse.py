import g
import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()


def main():
    """This function should start the parsing process by taking an array of ids
    from whatever scripted created it, and using that as the basis to parse
    through. It then calls sort_items().

    Args:
        itemToBeParsed (array): This is the list of ScienceBase IDs that need
                                parsed.
    """
    print("Items to Be Parsed: ")  # Quantico
    print(g.itemsToBeParsed)  # Quantico
    sort_items()


def sort_items():
    """This function first creates an array called "projects". It then takes
    the array itemToBeParsed and checks if it contains only one ID or if it
    contains multiple. If only one, it checks to see if the item is a project.
    If it is, it is added to the "projects" array and getProjectData() is
    called. If it is not a project, the array is appended to
    possibleProjectData and parse() is called.

    If it contains multiple IDs,
    they are all checked

    Args:
        projectDictNumber (int): the dictionary position within the "projects"
                                 array that changes throughout the script to
                                 parse from one project to another.
        possibleProjectData (array): all IDs that possibly contain data within
                                     the current project.
        exceptionItems (array): list of all item IDs that raised exceptions
                                when attempting to get their information.
        exceptionFound (boolean): Automatically set to "False", it changes to
                                  "True" if any exceptions are raised when
                                  attempting to get information on an item.
        lookedForShortcutsBefore (boolean): Set to "False" by default, this
                                            changes to "True" if
                                            findShortcuts() has been called
                                            before for the particular project.
        lookedForDataBefore (boolean): Set to "False" by default, it changes to
                                       "True" if getProjectData() has been
                                       called before.


    """


    if g.itemsToBeParsed == []:
        print("There are no items to be parsed.")
        import start
        start.questionLogin()
    print("""
    Sorting Items...""")

    # print(g.itemsToBeParsed)  # Quantico
    for i in g.itemsToBeParsed:
        itemsToBeParsed_json = sb.get_item(i)
        # pprint(itemsToBeParsed_json)  #Quantico
        print("Place: 1")  # Quantico

        if 'CSC' in itemsToBeParsed_json['title']:
            print("Place: 1.1")  # Quantico
            print("Item is a CSC folder.")  # Quantico
            g.itemsToBeParsed.remove(i)
            cscChildren = sb.get_child_ids(i)
            for year in cscChildren:
                if year not in g.fiscalYears:
                    g.fiscalYears.append(year)
                    if year in g.projects:
                        g.projects.remove(year)
                    if year in g.items:
                        g.items.remove(year)
            continue

        try: # is it a project?
            if "Project" in itemsToBeParsed_json["browseCategories"]:
                # print("Place: 2")  # Quantico
                if i not in g.projects:
                    g.projects.append(i)
                    if i in g.fiscalYears:
                        g.fiscalYears.remove(i)
                    if i in g.items:
                        g.items.remove(i)
                # print(len(g.projects))  # Quantico
                # print(g.projects)  #Quantico
                # print("Place: 3")  # Quantico
            elif itemsToBeParsed_json["hasChildren"] == True:  #Seeing if it is a FY
                # print("Place: 4")  # Quantico
                children = sb.get_child_ids(i)

                for child in children:
                    exampleChild_json = sb.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            # print("Place: 5")  # Quantico
                            if i not in g.fiscalYears:
                                g.fiscalYears.append(i)
                                if i in g.projects:
                                    g.projects.remove(i)
                                if i in g.items:
                                    g.items.remove(i)
                            # print(len(g.fiscalYears))  # Quantico
                            # print(g.fiscalYears)  #Quantico
                            # print("Place: 6")  # Quantico
                        else:
                            # print("Place: 20")  # Quantico
                            if i not in g.items:
                                g.items.append(i) # eyekeeper
                                if i in g.fiscalYears:
                                    g.fiscalYears.remove(i)
                                if i in g.projects:
                                    g.projects.remove(i)


                    except KeyError:
                        # print("Place: 7")  # Quantico
                        if i not in g.items:
                            g.items.append(i)
                            if i in g.fiscalYears:
                                g.fiscalYears.remove(i)
                            if i in g.projects:
                                g.projects.remove(i)
            else:
                # print("Place: 21")  # Quantico
                g.items.append(i) # eyekeeper
                if i in g.fiscalYears:
                    g.fiscalYears.remove(i)
                if i in g.projects:
                    g.projects.remove(i)

        except KeyError:
            if itemsToBeParsed_json["hasChildren"] == True:  #Seeing if it is a FY
                # print("Place: 4")  # Quantico
                children = sb.get_child_ids(i)

                for child in children:
                    exampleChild_json = sb.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            # print("Place: 5.2")  # Quantico
                            if i not in g.fiscalYears:
                                g.fiscalYears.append(i)
                                if i in g.projects:
                                    g.projects.remove(i)
                                if i in g.items:
                                    g.items.remove(i)
                            # print(len(g.fiscalYears))  # Quantico
                            # print(g.fiscalYears)  #Quantico
                            # print("Place: 6.2")  # Quantico
                        else:
                            # print("Place: 20.2")  # Quantico
                            if i not in g.items:
                                g.items.append(i) # eyekeeper
                                if i in g.fiscalYears:
                                    g.fiscalYears.remove(i)
                                if i in g.projects:
                                    g.projects.remove(i)


                    except KeyError:
                        # print("Place: 7.2")  # Quantico
                        if i not in g.items:
                            g.items.append(i)
                            if i in g.fiscalYears:
                                g.fiscalYears.remove(i)
                            if i in g.projects:
                                g.projects.remove(i)

    print("""
    Fiscal Years:""")
    print(g.fiscalYears)
    print("""
    Projects:""")  # Quantico
    print(g.projects)  # Quantico call getProjectData() for these
    print("""
    Items:""")  # Quantico
    print(g.items)  # Quantico call parse() for these
    # ^ probably do this first, because the projects will need this variable
    # perhaps make a class for the data and one for the projects
    # I also need to make sure that anything that doesn't meet any of the
    # requirements to be put in the "possible data" variable
    # for these it will be something like:
    # for i in projects:
        # i = Project() # which is a class
    parse_base()

def parse_base():

    if g.fiscalYears != []:
        import parseFY
        parseFY.main()
        print("--------------Done parsing Fiscal Years.")
    if g.projects != []:
        import parseProjects
        parseProjects.main()
        print("--------------Done parsing projects.")
    if g.items != []:
        import parseItems
        parseItems.main()
        print("--------------Done parsing items.")

    print("Done parsing all items!")


def parseOnTheFly():
    oldgFiscalYears = []
    for i in g.fiscalYears:
        oldgFiscalYears.append(i)
    oldgProjects = []
    for i in g.projects:
        oldgProjects.append(i)
    oldgItems = []
    for i in g.items:
        oldgItems.append(i)

    if g.onTheFlyParsing == []:
        print("There are no items to be parsed.")
        return
    print("""
    Sorting Items...""")

    print(g.onTheFlyParsing)  # Quantico

    for i in g.onTheFlyParsing:
        onTheFlyParsing_json = sb.get_item(i)
        # pprint(onTheFlyParsing_json)  # Quantico
        print("Place: 1")  # Quantico
        if 'CSC' in onTheFlyParsing_json['title']:
            print("Place: 1.1")  # Quantico
            print("Item is a CSC folder.")  # Quantico
            g.onTheFlyParsing.remove(i)
            cscChildren = sb.get_child_ids(i)
            for year in cscChildren:
                if year not in g.fiscalYears:
                    g.fiscalYears.append(year)
                    if year in g.projects:
                        g.projects.remove(year)
                    if year in g.items:
                        g.items.remove(year)
            continue
        try: # is it a project?
            if "Project" in onTheFlyParsing_json["browseCategories"]:
                print("Place: 2")  # Quantico
                if i not in g.projects:
                    g.projects.append(i)
                    if i in g.fiscalYears:
                        g.fiscalYears.remove(i)
                    if i in g.items:
                        g.items.remove(i)
                # print(len(g.projects))  # Quantico
                # print(g.projects)  #Quantico
                print("Place: 3")  # Quantico
            elif onTheFlyParsing_json["hasChildren"] == True:  #Seeing if it is a FY
                print("Place: 4")  # Quantico
                children = sb.get_child_ids(i)

                for child in children:
                    exampleChild_json = sb.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 5")  # Quantico
                            if i not in g.fiscalYears:
                                g.fiscalYears.append(i)
                                if i in g.projects:
                                    g.projects.remove(i)
                                if i in g.items:
                                    g.items.remove(i)
                            # print(len(g.fiscalYears))  # Quantico
                            # print(g.fiscalYears)  #Quantico
                            print("Place: 6")  # Quantico
                        else:
                            print("Place: 20")  # Quantico
                            if i not in g.items:
                                g.items.append(i) # eyekeeper
                                if i in g.fiscalYears:
                                    g.fiscalYears.remove(i)
                                if i in g.projects:
                                    g.projects.remove(i)


                    except KeyError:
                        print("Place: 7")  # Quantico
                        if i not in g.items:
                            g.items.append(i)
                            if i in g.fiscalYears:
                                g.fiscalYears.remove(i)
                            if i in g.projects:
                                g.projects.remove(i)
            else:
                print("Place: 21")  # Quantico
                g.items.append(i) # eyekeeper
                if i in g.fiscalYears:
                    g.fiscalYears.remove(i)
                if i in g.projects:
                    g.projects.remove(i)

        except KeyError:
            if onTheFlyParsing_json["hasChildren"] == True:  #Seeing if it is a FY
                print("Place: 4")  # Quantico
                children = sb.get_child_ids(i)

                for child in children:
                    exampleChild_json = sb.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 5.2")  # Quantico
                            if i not in g.fiscalYears:
                                g.fiscalYears.append(i)
                                if i in g.projects:
                                    g.projects.remove(i)
                                if i in g.items:
                                    g.items.remove(i)
                            # print(len(g.fiscalYears))  # Quantico
                            # print(g.fiscalYears)  #Quantico
                            print("Place: 6.2")  # Quantico
                        else:
                            print("Place: 20.2")  # Quantico
                            if i not in g.items:
                                g.items.append(i) # eyekeeper
                                if i in g.fiscalYears:
                                    g.fiscalYears.remove(i)
                                if i in g.projects:
                                    g.projects.remove(i)


                    except KeyError:
                        print("Place: 7.2")  # Quantico
                        if i not in g.items:
                            g.items.append(i)
                            if i in g.fiscalYears:
                                g.fiscalYears.remove(i)
                            if i in g.projects:
                                g.projects.remove(i)

    print("""
    Here are the old lists:
    """)
    print("""
    Previous Fiscal Years:""")
    print(oldgFiscalYears)
    print("""
    Previous Projects:""")  # Quantico
    print(oldgProjects)  # Quantico call getProjectData() for these
    print("""
    Previous Items:""")  # Quantico
    print(oldgItems)  # Quantico call parse() for these

    print("""

    Here are the new lists:
    """)
    print("""
    Fiscal Years:""")
    print(g.fiscalYears)
    print("""
    Projects:""")  # Quantico
    print(g.projects)  # Quantico call getProjectData() for these
    print("""
    Items:""")  # Quantico
    print(g.items)  # Quantico call parse() for these
    question(oldgItems, oldgProjects, oldgFiscalYears)

def question(oldgItems, oldgProjects, oldgFiscalYears):
    print("""
    Would you like to keep the old or new lists?
    Type "exit" to exit the program.
    """)
    answer = input("> ").lower()
    if "old" in answer or "previous" in answer:
        g.fiscalYears = oldgFiscalYears
        g.projects = oldgProjects
        g.items = oldgItems
        g.onTheFlyParsing[:] = []
        print("Done. Didn't keep changes")
        print("======================================================")
        print(g.fiscalYears)  # Quantico
        print(g.projects)  # Quantico
        print(g.items)  # Quantico
        return
    elif "new" in answer:
        g.onTheFlyParsing[:] = []
        print("Done. Kept Changes.")
        print("======================================================")
        return
    elif "exit" in answer:
        exit()
    else:
        print("Sorry, I didn't get that.")
        question(oldgItems, oldgProjects, oldgFiscalYears)




if __name__ == '__main__':

    main()

sb.logout()
