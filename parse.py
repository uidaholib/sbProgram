import g
import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0
projectDictNumber = 0
possibleProjectData = []
exceptionItems = []
exceptionFound = False
lookedForShortcutsBefore = False
lookedForDataBefore = False


def main(itemToBeParsed):
    """This function should start the parsing process by taking an array of ids
    from whatever scripted created it, and using that as the basis to parse
    through. It then calls startUp().

    Args:
        itemToBeParsed (array): This is the list of ScienceBase IDs that need
                                parsed.
    """
    print("Item to Be Parsed: ")  # Quantico
    print(itemToBeParsed)  # Quantico
    startUp(projectDictNumber, possibleProjectData, exceptionItems,
            exceptionFound, lookedForShortcutsBefore, lookedForDataBefore,
            itemToBeParsed)


def startUp(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore, itemToBeParsed):
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
        itemToBeParsed (array): This is the list of ScienceBase IDs that need
                                parsed. Sent from previous scripts.

    """
    projects = []
    possibleProjectData[:] = []
    if len(itemToBeParsed) > 1:
        print(len(itemToBeParsed))  # Quantico
        print(itemToBeParsed)  # Quantico
        itemToBeParsedDictNum = 0
        for i in itemToBeParsed:
            itemToBeParsed_json = sb.get_item(itemToBeParsed)
            print("Place: 1")  # Quantico
            try:
                if "Project" in itemToBeParsed_json["browseCategories"]:
                    print("Place: 2")  # Quantico
                    projects.append(itemToBeParsed)
                    print(len(projects))  # Quantico
                    print(projects)  #Quantico
                    currentProject = projects[projectDictNumber]
                    print(currentProject)
                    print("Place: 3")  # Quantico
                elif itemToBeParsed_json["hasChildren"] == True:  #Seeing if it is a FY
                    print("Place: 4")  # Quantico
                    children = sb.get_child_ids(itemToBeParsed)
                    exampleChild = children[0]
                    exampleChild_json = sb.get_item(exampleChild)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 5")  # Quantico
                            projects.append(children)
                            print(len(projects))  # Quantico
                            print(projects)  #Quantico
                            currentProject = projects[projectDictNumber]
                            print(currentProject)
                            print("Place: 6")  # Quantico
                        else:
                            print("Place: 20")  # Quantico
                            possibleProjectData.append(itemToBeParsed) # eyekeeper


                    except KeyError:
                        print("Place: 7")  # Quantico
                        possibleProjectData.append(itemToBeParsed)
                else:
                    print("Place: 21")  # Quantico
                    possibleProjectData.append(itemToBeParsed) # eyekeeper

            except KeyError:
                if itemToBeParsed_json["hasChildren"] == True:  #Seeing if it is a FY
                    print("Place: 4")  # Quantico
                    children = sb.get_child_ids(itemToBeParsed)
                    exampleChild = children[0]
                    exampleChild_json = sb.get_item(exampleChild)
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 5")  # Quantico
                            projects.append(children)
                            print(len(projects))  # Quantico
                            print(projects)  #Quantico
                            currentProject = projects[projectDictNumber]
                            print(currentProject)
                            print("Place: 6")  # Quantico
                        else:
                            print("Place: 20")  # Quantico
                            possibleProjectData.append(itemToBeParsed) # eyekeeper


                    except KeyError:
                        print("Place: 7")  # Quantico
                        possibleProjectData.append(itemToBeParsed)


    elif len(itemToBeParsed) == 1:
        print(len(itemToBeParsed))  # Quantico
        print(itemToBeParsed)  # Quantico
        print("Place: 8")  # Quantico
        itemToBeParsed_json = sb.get_item(itemToBeParsed[0])
        try:
            if "Project" in itemToBeParsed_json["browseCategories"]:
                print("Place: 9")  # Quantico
                projects.append(itemToBeParsed)
                print(len(projects))  # Quantico
                print(projects)  #Quantico
                # currentProject = '5006e99ee4b0abf7ce733f58'  # Quantico: Marshes to Mudflats project
                currentProject = projects[projectDictNumber]
                print(currentProject)
                print("Place: 10")  # Quantico
            else:
                if itemToBeParsed_json["hasChildren"] == True:  #Seeing if it is an FY
                    print("Place: 11.1")  # Quantico
                    children = sb.get_child_ids(itemToBeParsed[0])
                    exampleChild = children[0]
                    print('exampleChild: ')
                    print(exampleChild)  # Quantico
                    exampleChild_json = sb.get_item(exampleChild)
                    print(exampleChild_json["browseCategories"])
                    try:
                        if "Project" in exampleChild_json["browseCategories"]:
                            print("Place: 12.1")  # Quantico
                            print("children: ")  # Quantico
                            print(children)  # Quantico
                            for i in children:
                                projects.append(i)
                            print(len(projects))  # Quantico
                            print(projects)  #Quantico
                            currentProject = projects[projectDictNumber]
                            print(currentProject)
                            print("Place: 13.1")  # Quantico
                    except KeyError:
                        print("Not Fiscal Year")  # Quantico
                        possibleProjectData.append(itemToBeParsed) # eyekeeper

                else:
                    print("Place: 14.1")  # Quantico
                    possibleProjectData.append(itemToBeParsed)


        except KeyError:
            if itemToBeParsed_json["hasChildren"] == True:  #Seeing if it is an FY
                print("Place: 11.2")  # Quantico
                children = sb.get_child_ids(itemToBeParsed[0])
                exampleChild = children[0]
                print('exampleChild: ')
                print(exampleChild)  # Quantico
                exampleChild_json = sb.get_item(exampleChild)
                print(exampleChild_json["browseCategories"])
                try:
                    if "Project" in exampleChild_json["browseCategories"]:
                        print("Place: 12.2")  # Quantico
                        print("children: ")  # Quantico
                        print(children)  # Quantico
                        for i in children:
                            projects.append(i)
                        print(len(projects))  # Quantico
                        print(projects)  #Quantico
                        currentProject = projects[projectDictNumber]
                        print(currentProject)
                        print("Place: 13.2")  # Quantico
                except KeyError:
                    print("Not Fiscal Year (2)")  # Quantico
                    possibleProjectData.append(itemToBeParsed)  # eyekeeper

            else:
                print("Place: 14.2")  # Quantico
                possibleProjectData.append(itemToBeParsed)

    else:
        print("There are no items to parse.")

    print("projects: ")  # Quantico
    print(projects)  # Quantico call getProjectData() for these
    print("possibleProjectData: ")  # Quantico
    print(possibleProjectData)  # Quantico call parse() for these
    # ^ probably do this first, because the projects will need this variable
    # perhaps make a class for the data and one for the projects
    # I also need to make sure that anything that doesn't meet any of the
    # requirements to be put in the "possible data" variable
    # for these it will be something like:
    # for i in projects:
        # i = Project() # which is a class



def getProjectData(projectDictNumber, possibleProjectData, projects, currentProject, exceptionItems, exceptionFound,
                   lookedForShortcutsBefore, lookedForDataBefore):
    print("Place: 15")  # Quantico
    projectItems = sb.get_child_ids(currentProject)
    currentProjectJson = sb.get_item(currentProject)
    if lookedForDataBefore is False:
        print("""

        Currently searching '"""+str(currentProjectJson['title'])+"'.")
        lookedForDataBefore = True
        for i in projectItems:
            currentProjectItemJson = sb.get_item(i)
            print(currentProjectItemJson['title'])
            if currentProjectItemJson['title'] == "Approved DataSets":
                possibleProjectData_Set = set()
                possibleProjectData_Set.update(possibleProjectData)
                ancestors = sb.get_ancestor_ids(i)
                for item in ancestors:
                    if item not in possibleProjectData_Set:
                        possibleProjectData_Set.add(item)
                        possibleProjectData.append(item)
                    else:
                        pass
                print('First look at Possible Project Data:')
                print(possibleProjectData)
                print('Total Items:')
                print(len(possibleProjectData))
            else:
                pass
    parse(projectDictNumber, possibleProjectData, projects, currentProject, exceptionItems, exceptionFound,
                       lookedForShortcutsBefore, lookedForDataBefore)

def parse(projectDictNumber, possibleProjectData, projects, currentProject, exceptionItems, exceptionFound,
                   lookedForShortcutsBefore, lookedForDataBefore):
    for i in possibleProjectData:
        possibleProjectData_Set = set()
        possibleProjectData_Set.update(possibleProjectData)
        try:
            ancestors = sb.get_ancestor_ids(i)
        except Exception:
            exceptionItems.append(i)
            exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(i)+" (1)")
        for item in ancestors:
            if item not in possibleProjectData_Set:
                possibleProjectData_Set.add(item)
                possibleProjectData.append(item)
            elif item in possibleProjectData_Set:
                pass
            else:
                print("Something went wrong. Current function: "
                      + "getProjectData (1)")
    print('Double checked Possible Project Data:')
    print(possibleProjectData)
    print('Total Items:')
    print(len(possibleProjectData))

    findShortcuts(projects, projectDictNumber, currentProject, exceptionItems, exceptionFound,
                  possibleProjectData, projectItems, currentProjectJson,
                  lookedForShortcutsBefore, lookedForDataBefore)


def findShortcuts(projects, projectDictNumber, currentProject, exceptionItems, exceptionFound,
                  possibleProjectData, projectItems, currentProjectJson,
                  lookedForShortcutsBefore, lookedForDataBefore):
    print("Looking for shortcuts in any items...")
    foundShortcutsThisTime = False
    if lookedForShortcutsBefore is False:
        for i in projectItems:
            try:
                currentProjectItemJson = sb.get_item(i)
                if currentProjectItemJson['title'] == "Approved DataSets":
                    shortcuts = sb.get_shortcut_ids(i)
                    print(shortcuts)
                    if shortcuts == []:
                        lookedForShortcutsBefore = True
                        print("No shortcuts in \"Approved DataSets\".")
                    elif shortcuts != []:
                        lookedForShortcutsBefore = True
                        foundShortcutsThisTime = True
                        possibleProjectData += shortcuts
                        print("We found some shortcuts and added them to the " +
                              "Possible Project Data:")
                        print(shortcuts)
                        print('Total Items added:')
                        print(len(shortcuts))
                        print("New Possible Project Data:")
                        print(possibleProjectData)
                        print("Current Item total:")
                        print(len(possibleProjectData))
                    else:
                        print("Something went wrong. Current function: "
                              + "findShortcuts (1)")
                        exit()
                else:
                    pass
            except Exception:
                exceptionItems.append(i)
                exceptionFound = True
                print("--------Hit upon a 404 exception: "+str(i)+" (2)")

    elif lookedForShortcutsBefore is True:
        pass #something should happen here. eyekeeper
    else:
        print("Something went wrong. Current function: findShortcuts (2)")
        exit()
    allShortcuts = []
    for i in possibleProjectData:
        try:
            allShortcuts += sb.get_shortcut_ids(i)
        except Exception:
            exceptionItems.append(i)
            exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(i)+" (3)")
    print(allShortcuts)
    if allShortcuts == []:
        print("No shortcuts in \"Possible Project Data\".")
    elif allShortcuts != []:
        foundShortcutsThisTime = True
        possibleProjectData += allShortcuts
        print("We found some shortcuts and added them to the Possible Project "
              + "Data:")
        print(possibleProjectData)
        print('Total Items:')
        print(len(possibleProjectData))
    else:
        print("Something went wrong. Current function: findShortcuts (3)")
        exit()

    if foundShortcutsThisTime is True:
        print("-------- Found shortcuts this time!")
        getProjectData(projectDictNumber, possibleProjectData, projects, currentProject, exceptionItems, exceptionFound,
                           lookedForShortcutsBefore, lookedForDataBefore)
        # getProjectData(projects, projectDictNumber, currentProject,
        #               possibleProjectData, lookedForShortcutsBefore,
        #               lookedForDataBefore)
    elif foundShortcutsThisTime is False:
        print("-------- Didn't find any Shortcuts this time!") # Quantico
        if exceptionFound is False:
            print('''
            I am done looking through the \''''+str(currentProjectJson['title']) +
                  '''' project folder.''')
            projectDictNumber += 1
            whatNext(projects, projectDictNumber, exceptionItems, exceptionFound)
        elif exceptionFound is True:
            diagnostics(projects, projectDictNumber, exceptionItems, exceptionFound, currentProjectJson)

    # projectItemDictNum += 1
    # if projectItemDictNum > len(projectItems):

def diagnostics(projects, projectDictNumber, exceptionItems, exceptionFound, currentProjectJson):
    print("There appear to have been exceptions raised for the following items:")
    print(exceptionItems)
    print('''

    I am done looking through the \''''+str(currentProjectJson['title']) +
          '''' project folder.''')
    projectDictNumber += 1
    whatNext(projects, projectDictNumber, exceptionItems, exceptionFound)


def whatNext(projects, projectDictNumber, exceptionItems, exceptionFound):
    print("Continue? (Y / N)")
    answer = input("> ")
    if 'y' in answer or 'Y' in answer:
        if projectDictNumber >= len(projects):
            print("You have finished. No more available Projects.")
            print('Goodbye')
            exit()
        elif projectDictNumber < len(projects):
            print("Ok, let\'s start on project "+str(projectDictNumber+1) +
                  " of "+str(len(projects))+".")
            lookedForShortcutsBefore = False
            lookedForDataBefore = False
            startUp(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore, itemToBeParsed)
    elif 'n' in answer or 'N' in answer:
        print('Goodbye')
        exit()
    else:
        print("Please type an 'N' or 'Y'.")
        whatNext(projects, projectDictNumber, exceptionItems, exceptionFound)

    # elif projectItemDictNum <= len(projectItems):
    #    getProjectData(currentProject, projectItemDictNum)
    # else:
    #    print('Something is wrong. Current function: getProjectData')


def nextFunction():

    startUp(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore, itemToBeParsed)


if __name__ == '__main__':
    itemToBeParsed = []
    itemToBeParsed.append("5006c2c9e4b0abf7ce733f42")
    main(itemToBeParsed)

sb.logout()


# ancestor = sb.get_ancestor_ids(parentid)
# print(ancestor)

# trying = '5536dbe1e4b0b22a15808467'
# tryThis = sb.get_item_file_info(trying)
# print("TryThis:")
# print(tryThis)
# List file info from the newly found items
# print("Starting count...")
# for i in ancestor:
#    ret = sb.get_item_file_info(i)
#    print('ret created')
#    print(ret)
#    for fileinfo in ret:
#        print("File " + fileinfo["name"] + ", " + str(fileinfo["size"]) +
#              "bytes, download URL " + fileinfo["url"])
