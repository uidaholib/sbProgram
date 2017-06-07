import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0
projectDictNumber = 0
possibleProjectData = []


def main(projectDictNumber, possibleProjectData):
    FY2012 = '5006c2c9e4b0abf7ce733f42'

    projects = sb.get_child_ids(FY2012)
    print(len(projects))
    print(projects)
    currentProject = '5006e99ee4b0abf7ce733f58'  # Quantico
    # currentProject = projects[projectDictNumber]
    print(currentProject)
    possibleProjectData[:] = []
    # projectItemDictNum = 0
    lookedForShortcutsBefore = False
    getProjectData(projects, projectDictNumber, currentProject,
                   possibleProjectData, lookedForShortcutsBefore)


def getProjectData(projects, projectDictNumber, currentProject,
                   possibleProjectData, lookedForShortcutsBefore):
    projectItems = sb.get_child_ids(currentProject)
    currentProjectJson = sb.get_item(currentProject)
    for i in projectItems:
        currentProjectItemJson = sb.get_item(i)
        print(currentProjectItemJson['title'])
        if currentProjectItemJson['title'] == "Approved DataSets":
            possibleProjectData_Set = set(possibleProjectData)
            ancestors = sb.get_ancestor_ids(i)
            for item in ancestors:
                if item not in possibleProjectData_Set:
                    possibleProjectData_Set.add(sb.get_ancestor_ids(i))
                    possibleProjectData.append(sb.get_ancestor_ids(i))
                else:
                    pass
            print('Possible Project Data:')
            print(possibleProjectData)
            print('Total Items:')
            print(len(possibleProjectData))
        else:
            pass

    findShortcuts(projects, projectDictNumber, currentProject,
                  possibleProjectData, projectItems, currentProjectJson,
                  lookedForShortcutsBefore)


def findShortcuts(projects, projectDictNumber, currentProject,
                  possibleProjectData, projectItems, currentProjectJson,
                  lookedForShortcutsBefore):
    print("Looking for shortcuts in any items...")
    foundShortcutsThisTime = False
    if lookedForShortcutsBefore == False:
        for i in projectItems:
            currentProjectItemJson = sb.get_item(i)
            print(currentProjectItemJson['title'])
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
                    print(possibleProjectData)
                    print('Total Items:')
                    print(len(possibleProjectData))
                else:
                    print("Something went wrong. Current function: "
                          + "getProjectData (1)")
                    exit()
            else:
                pass
    elif lookedForShortcutsBefore == True:
        pass
    else:
        print("Something went wrong. Current function: getProjectData (2)")
        exit()
    allShortcuts = []
    for i in possibleProjectData:
        allShortcuts += sb.get_shortcut_ids(i)
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
        print("Something went wrong. Current function: getProjectData (3)")
        exit()

    if foundShortcutsThisTime == True:
        getProjectData(projects, projectDictNumber, currentProject,
                       possibleProjectData, lookedForShortcutsBefore)
    elif foundShortcutsThisTime == False:
        print('''
        I am done looking through the \''''+str(currentProjectJson['title']) +
              '''' project folder.''')
        projectDictNumber += 1
        whatNext(projects, projectDictNumber)

    # projectItemDictNum += 1
    # if projectItemDictNum > len(projectItems):


def whatNext(projects, projectDictNumber):
    print("Continue? (Y / N)")
    answer = input("> ")
    if 'y' in answer or 'Y' in answer:
        if projectDictNumber > len(projects):
            print("You have finished. No more available Projects")
            print('Goodbye')
            exit()
        elif projectDictNumber <= len(projects):
            print("Ok, let\'s start on project "+str(projectDictNumber+1) +
                  " of "+str(len(projects))+".")
            main(projectDictNumber)
    elif 'n' in answer or 'N' in answer:
        print('Goodbye')
        exit()
    else:
        print("Please type an 'N' or 'Y'.")
        whatNext(projects, projectDictNumber)

    # elif projectItemDictNum <= len(projectItems):
    #    getProjectData(currentProject, projectItemDictNum)
    # else:
    #    print('Something is wrong. Current function: getProjectData')


def nextFunction():

    main(projectDictNumber, possibleProjectData)


if __name__ == '__main__':
    main(projectDictNumber, possibleProjectData)

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
