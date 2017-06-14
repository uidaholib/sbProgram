import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0
projectDictNumber = 11
possibleProjectData = []
exceptionItems = []
exceptionFound = False
lookedForShortcutsBefore = False
lookedForDataBefore = False

def main(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore):
    FY2012 = '5006c2c9e4b0abf7ce733f42'

    projects = sb.get_child_ids(FY2012) # Raised exception?
    print(len(projects))
    print(projects)
    #currentProject = '5006e99ee4b0abf7ce733f58'  # Quantico: Marshes to Mudflats project
    currentProject = projects[projectDictNumber]
    print(currentProject)
    possibleProjectData[:] = []
    # projectItemDictNum = 0

    getProjectData(projectDictNumber, possibleProjectData, projects, currentProject, exceptionItems, exceptionFound,
                   lookedForShortcutsBefore, lookedForDataBefore)


def getProjectData(projectDictNumber, possibleProjectData, projects, currentProject, exceptionItems, exceptionFound,
                   lookedForShortcutsBefore, lookedForDataBefore):
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
        pass #something should happen here
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
            main(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore)
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

    main(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore)


if __name__ == '__main__':
    main(projectDictNumber, possibleProjectData, exceptionItems, exceptionFound, lookedForShortcutsBefore, lookedForDataBefore)

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
