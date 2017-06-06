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
    currentProject = '5006e99ee4b0abf7ce733f58' #Quantico
    #currentProject = projects[projectDictNumber]
    print(currentProject)
    possibleProjectData[:] = []
    #projectItemDictNum = 0
    getProjectData(projects, projectDictNumber, currentProject, possibleProjectData)

def getProjectData(projects, projectDictNumber, currentProject, possibleProjectData):
    projectItems = sb.get_child_ids(currentProject)
    currentProjectJson = sb.get_item(currentProject)
    for i in projectItems:
        currentProjectItemJson = sb.get_item(i)
        print(currentProjectItemJson['title'])
        if currentProjectItemJson['title'] == "Approved DataSets":
            possibleProjectData += sb.get_ancestor_ids(i)
            print('Possible Project Data:')
            print(possibleProjectData)
            print('Total Items:')
            print(len(possibleProjectData))
        else:
            pass
    findShortcuts(projects, projectDictNumber, currentProject,
                        possibleProjectData, projectItems, currentProjectJson)

def findShortcuts(projects, projectDictNumber, currentProject,
                    possibleProjectData, projectItems, currentProjectJson):
    print("Looking for shortcuts in any items...")
    for i in projectItems:
        currentProjectItemJson = sb.get_item(i)
        print(currentProjectItemJson['title'])
        if currentProjectItemJson['title'] == "Approved DataSets":
            shortcuts = sb.get_shortcut_ids(i)
            print(shortcuts)
            if shortcuts == []:
                print("No shortcuts in \"Approved DataSets\".")
            elif shortcuts != []:
                possibleProjectData += shortcuts
                print("We found some shortcuts and added them to the Possible Project Data:")
                print(possibleProjectData)
                print('Total Items:')
                print(len(possibleProjectData))
                getProjectData(projects, projectDictNumber, currentProject, possibleProjectData)
            else:
                print("Something went wrong. Current function: getProjectData")
        else:
            pass

    #projectItemDictNum += 1
    #if projectItemDictNum > len(projectItems):

    print('''
    I am done looking through the \''''+str(currentProjectJson['title'])+
                                                        '''' project folder.''')
    projectDictNumber += 1
    whatNext(projects, projectDictNumber)

def whatNext(projects, projectDictNumber):
    print("Continue? (Y / N)")
    answer = input("> ")
    if 'y' in answer or 'Y' in answer:
        if projectDictNumber > len(projects):
            print("You have finished. No more available Projects")
            print('Goodbye')
            exit()
        elif projectDictNumber <= len(projects):
            print("Ok, let\'s start on project "+str(projectDictNumber+1)+
                " of "+str(len(projects))+".")
            main(projectDictNumber)
    elif 'n' in answer or 'N' in answer:
        print('Goodbye')
        exit()
    else:
        print("Please type an 'N' or 'Y'.")
        whatNext(projects, projectDictNumber)

    #elif projectItemDictNum <= len(projectItems):
    #    getProjectData(currentProject, projectItemDictNum)
    #else:
    #    print('Something is wrong. Current function: getProjectData')


def nextFunction():

    main(projectDictNumber, possibleProjectData)

if __name__ == '__main__':
    main(projectDictNumber, possibleProjectData)

sb.logout()



#ancestor = sb.get_ancestor_ids(parentid)
#print(ancestor)

#trying = '5536dbe1e4b0b22a15808467'
#tryThis = sb.get_item_file_info(trying)
#print("TryThis:")
#print(tryThis)
# List file info from the newly found items
#print("Starting count...")
#for i in ancestor:
#    ret = sb.get_item_file_info(i)
#    print('ret created')
#    print(ret)
#    for fileinfo in ret:
#        print("File " + fileinfo["name"] + ", " + str(fileinfo["size"]) + "bytes, download URL " + fileinfo["url"])
