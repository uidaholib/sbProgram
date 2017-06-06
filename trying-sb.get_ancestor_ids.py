import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0
projectDictNumber = 0

def main(projectDictNumber):
    FY2012 = '5006c2c9e4b0abf7ce733f42'

    projects = sb.get_child_ids(FY2012)
    print(len(projects))
    print(projects)
    currentProject = projects[projectDictNumber]
    print(currentProject)

    #projectItemDictNum = 0
    getProjectData(projectDictNumber, currentProject)

def getProjectData(projectDictNumber, currentProject):
    projectItems = sb.get_child_ids(currentProject)
    currentProjectJson = sb.get_item(currentProject)
    for i in projectItems:
        currentProjectItemJson = sb.get_item(i)
        print(currentProjectItemJson['title'])
        if currentProjectItemJson['title'] == "Approved DataSets":
            possibleProjectData = sb.get_ancestor_ids(i)
            print('Possible Project Data:')
            print(possibleProjectData)
        else:
            pass
    #projectItemDictNum += 1
    #if projectItemDictNum > len(projectItems):

    print('''
    I am done looking through the \''''+str(currentProjectJson['title'])+
                                                        '''' project folder.''')
    projectDictNumber += 1
    #main():
    #elif projectItemDictNum <= len(projectItems):
    #    getProjectData(currentProject, projectItemDictNum)
    #else:
    #    print('Something is wrong. Current function: getProjectData')


def nextFunction():

     main(projectDictNumber)

if __name__ == '__main__':
    main(projectDictNumber)

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
