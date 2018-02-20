"""This module sorts ScienceBase ids and sends them to appropriate modules"""
import sys
import os
import pysb  # pylint: disable=wrong-import-order

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "DataCounting/"))
import gl  # pylint: disable=C0413
import parseFY  # pylint: disable=C0413
import saveJson  # pylint: disable=E0401,C0413,C0410,C0411
import edit_gpy  # pylint: disable=E0401,C0413,C0410,C0411,W0611

SB = pysb.SbSession()


def main():
    """This function should start the parsing process by taking an array of ids
    from whatever scripted created it, and using that as the basis to parse
    through. It then calls sort_items().

    Args:
        itemToBeParsed (array): This is the list of ScienceBase IDs that need
                                parsed.
    """
    print("Items to Be Parsed: ")  # Quantico
    print(gl.items_to_be_parsed)  # Quantico
    sort_items()
    parse_base()


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


    if gl.items_to_be_parsed == []:
        print("There are no items to be parsed.")
        # import start
        # start.questionLogin()
        sys.exit()
    print("""
    Sorting Items...""")

    # print(gl.items_to_be_parsed)  # Quantico
    for i in gl.items_to_be_parsed:
        try:
            itemsToBeParsed_json = SB.get_item(i)
        except Exception:  # pylint: disable=W0703
            exceptionFound = True
            print("--------Hit upon a 404 exception: parse.sort_items (1)")
            parseFY.exceptionLoop(i)
            itemsToBeParsed_json = SB.get_item(i)
        # pprint(itemsToBeParsed_json)  #Quantico
        print("Place: 1")  # Quantico

        if 'CSC' in itemsToBeParsed_json['title']:
            print("Place: 1.1")  # Quantico
            print("Item is a CSC folder.")  # Quantico
            gl.items_to_be_parsed.remove(i)

            try:
                cscChildren = SB.get_child_ids(i)
            except Exception:  # pylint: disable=W0703
                exceptionFound = True
                print("--------Hit upon a 404 exception: parse.sort_items (1)")
                parseFY.exceptionLoop(i)
                cscChildren = SB.get_child_ids(i)
            for year in cscChildren:
                if year not in gl.fiscalYears:
                    gl.fiscalYears.append(year)
                    if year in gl.projects:
                        gl.projects.remove(year)
                    if year in gl.items:
                        gl.items.remove(year)
            continue

        try: # is it a project?
            if "Project" in itemsToBeParsed_json["browseCategories"]:
                # print("Place: 2")  # Quantico
                if i not in gl.projects:
                    gl.projects.append(i)
                    if i in gl.fiscalYears:
                        gl.fiscalYears.remove(i)
                    if i in gl.items:
                        gl.items.remove(i)
                # print(len(gl.projects))  # Quantico
                # print(gl.projects)  #Quantico
                # print("Place: 3")  # Quantico
            elif itemsToBeParsed_json["hasChildren"] == True:  #Seeing if it is a FY
                # print("Place: 4")  # Quantico

                # children = SB.get_child_ids(i)
                try:
                    children = SB.get_child_ids(i)
                except Exception:  # pylint: disable=W0703
                    exceptionFound = True
                    print("--------Hit upon a 404 exception: parse.sort_items (1)")
                    parseFY.exceptionLoop(i)
                    children = SB.get_child_ids(i)
                for child in children:
                    
                    try:
                        exampleChild_json = SB.get_item(child)
                    except Exception:  # pylint: disable=W0703
                        exceptionFound = True
                        print("--------Hit upon a 404 exception: parse.sort_items (1)")
                        parseFY.exceptionLoop(child)
                        exampleChild_json = SB.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            # print("Place: 5")  # Quantico
                            if i not in gl.fiscalYears:
                                gl.fiscalYears.append(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)
                                if i in gl.items:
                                    gl.items.remove(i)
                            # print(len(gl.fiscalYears))  # Quantico
                            # print(gl.fiscalYears)  #Quantico
                            # print("Place: 6")  # Quantico
                        else:
                            # print("Place: 20")  # Quantico
                            if i not in gl.items:
                                gl.items.append(i) # eyekeeper
                                if i in gl.fiscalYears:
                                    gl.fiscalYears.remove(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)


                    except KeyError:
                        # print("Place: 7")  # Quantico
                        if i not in gl.items:
                            gl.items.append(i)
                            if i in gl.fiscalYears:
                                gl.fiscalYears.remove(i)
                            if i in gl.projects:
                                gl.projects.remove(i)
            else:
                # print("Place: 21")  # Quantico
                gl.items.append(i) # eyekeeper
                if i in gl.fiscalYears:
                    gl.fiscalYears.remove(i)
                if i in gl.projects:
                    gl.projects.remove(i)

        except KeyError:
            if itemsToBeParsed_json["hasChildren"] == True:  #Seeing if it is a FY
                # print("Place: 4")  # Quantico
                try:
                    children = SB.get_child_ids(i)
                except Exception:  # pylint: disable=W0703
                    exceptionFound = True
                    print("--------Hit upon a 404 exception: parse.sort_items (1)")
                    parseFY.exceptionLoop(i)
                    children = SB.get_child_ids(i)

                for child in children:
                    try:
                        exampleChild_json = SB.get_item(child)
                    except Exception:  # pylint: disable=W0703
                        exceptionFound = True
                        print("--------Hit upon a 404 exception: parse.sort_items (2)")
                        parseFY.exceptionLoop(child)
                        exampleChild_json = SB.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            # print("Place: 5.2")  # Quantico
                            if i not in gl.fiscalYears:
                                gl.fiscalYears.append(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)
                                if i in gl.items:
                                    gl.items.remove(i)
                            # print(len(gl.fiscalYears))  # Quantico
                            # print(gl.fiscalYears)  #Quantico
                            # print("Place: 6.2")  # Quantico
                        else:
                            # print("Place: 20.2")  # Quantico
                            if i not in gl.items:
                                gl.items.append(i) # eyekeeper
                                if i in gl.fiscalYears:
                                    gl.fiscalYears.remove(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)


                    except KeyError:
                        # print("Place: 7.2")  # Quantico
                        if i not in gl.items:
                            gl.items.append(i)
                            if i in gl.fiscalYears:
                                gl.fiscalYears.remove(i)
                            if i in gl.projects:
                                gl.projects.remove(i)

    print("""
    Fiscal Years:""")
    print(gl.fiscalYears)
    print("""
    Projects:""")  # Quantico
    print(gl.projects)  # Quantico call getProjectData() for these
    print("""
    Items:""")  # Quantico
    print(gl.items)  # Quantico call parse() for these
    # ^ probably do this first, because the projects will need this variable
    # perhaps make a class for the data and one for the projects
    # I also need to make sure that anything that doesn't meet any of the
    # requirements to be put in the "possible data" variable
    # for these it will be something like:
    # for i in projects:
        # i = Project() # which is a class
    return

def parse_base():

    if gl.fiscalYears != []:
        for i in gl.fiscalYears:
            edit_gpy.clear_memory()
            parseFY.main(i)
            saveJson.main()
        print("--------------Done parsing Fiscal Years.")
    else:
        # get rid of this and uncomment the code below if/when project and item hard search is implemented.
        print("Cannot parse items that are not fiscal years yet")
    print("Done parsing all items!")  # eyekeeper I need to return to whatever called parse.py or something.


def parseOnTheFly():
    oldgFiscalYears = []
    for i in gl.fiscalYears:
        oldgFiscalYears.append(i)
    oldgProjects = []
    for i in gl.projects:
        oldgProjects.append(i)
    oldgItems = []
    for i in gl.items:
        oldgItems.append(i)

    if gl.on_the_fly_parsing == []:
        print("There are no items to be parsed.")
        return
    print("""
    Sorting Items...""")

    print(gl.on_the_fly_parsing)  # Quantico

    for i in gl.on_the_fly_parsing:
        onTheFlyParsing_json = SB.get_item(i)
        # pprint(onTheFlyParsing_json)  # Quantico
        print("Place: 1")  # Quantico
        if 'CSC' in onTheFlyParsing_json['title']:
            print("Place: 1.1")  # Quantico
            print("Item is a CSC folder.")  # Quantico
            gl.on_the_fly_parsing.remove(i)
            cscChildren = SB.get_child_ids(i)
            for year in cscChildren:
                if year not in gl.fiscalYears:
                    gl.fiscalYears.append(year)
                    if year in gl.projects:
                        gl.projects.remove(year)
                    if year in gl.items:
                        gl.items.remove(year)
            continue
        try: # is it a project?
            if "Project" in onTheFlyParsing_json["browseCategories"]:
                print("Place: 2")  # Quantico
                if i not in gl.projects:
                    gl.projects.append(i)
                    if i in gl.fiscalYears:
                        gl.fiscalYears.remove(i)
                    if i in gl.items:
                        gl.items.remove(i)
                # print(len(gl.projects))  # Quantico
                # print(gl.projects)  #Quantico
                print("Place: 3")  # Quantico
            elif onTheFlyParsing_json["hasChildren"] == True:  #Seeing if it is a FY
                print("Place: 4")  # Quantico
                children = SB.get_child_ids(i)

                for child in children:
                    exampleChild_json = SB.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 5")  # Quantico
                            if i not in gl.fiscalYears:
                                gl.fiscalYears.append(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)
                                if i in gl.items:
                                    gl.items.remove(i)
                            # print(len(gl.fiscalYears))  # Quantico
                            # print(gl.fiscalYears)  #Quantico
                            print("Place: 6")  # Quantico
                        else:
                            print("Place: 20")  # Quantico
                            if i not in gl.items:
                                gl.items.append(i) # eyekeeper
                                if i in gl.fiscalYears:
                                    gl.fiscalYears.remove(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)


                    except KeyError:
                        print("Place: 7")  # Quantico
                        if i not in gl.items:
                            gl.items.append(i)
                            if i in gl.fiscalYears:
                                gl.fiscalYears.remove(i)
                            if i in gl.projects:
                                gl.projects.remove(i)
            else:
                print("Place: 21")  # Quantico
                gl.items.append(i) # eyekeeper
                if i in gl.fiscalYears:
                    gl.fiscalYears.remove(i)
                if i in gl.projects:
                    gl.projects.remove(i)

        except KeyError:
            if onTheFlyParsing_json["hasChildren"] == True:  #Seeing if it is a FY
                print("Place: 4")  # Quantico
                children = SB.get_child_ids(i)

                for child in children:
                    exampleChild_json = SB.get_item(child)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 5.2")  # Quantico
                            if i not in gl.fiscalYears:
                                gl.fiscalYears.append(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)
                                if i in gl.items:
                                    gl.items.remove(i)
                            # print(len(gl.fiscalYears))  # Quantico
                            # print(gl.fiscalYears)  #Quantico
                            print("Place: 6.2")  # Quantico
                        else:
                            print("Place: 20.2")  # Quantico
                            if i not in gl.items:
                                gl.items.append(i) # eyekeeper
                                if i in gl.fiscalYears:
                                    gl.fiscalYears.remove(i)
                                if i in gl.projects:
                                    gl.projects.remove(i)


                    except KeyError:
                        print("Place: 7.2")  # Quantico
                        if i not in gl.items:
                            gl.items.append(i)
                            if i in gl.fiscalYears:
                                gl.fiscalYears.remove(i)
                            if i in gl.projects:
                                gl.projects.remove(i)

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
    print(gl.fiscalYears)
    print("""
    Projects:""")  # Quantico
    print(gl.projects)  # Quantico call getProjectData() for these
    print("""
    Items:""")  # Quantico
    print(gl.items)  # Quantico call parse() for these
    question(oldgItems, oldgProjects, oldgFiscalYears)

def question(oldgItems, oldgProjects, oldgFiscalYears):
    print("""
    Would you like to keep the old or new lists?
    Type "exit" to exit the program.
    """)
    answer = input("> ").lower()
    if "old" in answer or "previous" in answer:
        gl.fiscalYears = oldgFiscalYears
        gl.projects = oldgProjects
        gl.items = oldgItems
        gl.on_the_fly_parsing[:] = []
        print("Done. Didn't keep changes")
        print("======================================================")
        print(gl.fiscalYears)  # Quantico
        print(gl.projects)  # Quantico
        print(gl.items)  # Quantico
        return
    elif "new" in answer:
        gl.on_the_fly_parsing[:] = []
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

SB.logout()
