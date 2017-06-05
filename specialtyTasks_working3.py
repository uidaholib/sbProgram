import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0

#==============================================================================
#for creating an Excel workbook:
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
#==============================================================================
ChosenFiscalYear = []
L1Project = []
L2DataInProject = []
L3NumSbItemsFound = []
L4DataPerFile = []
L5RunningDataTotal = []
L6NestedData = []
L7MissingData = []
L8MissingDataURL = []
L9Exceptions = []
L10Exceptions_IDs = []
#==============================================================================
def main():
    ChosenFiscalYear[:] = []
    L1Project[:] = []
    L2DataInProject[:] = []
    L3NumSbItemsFound[:] = []
    L4DataPerFile[:] = []
    L5RunningDataTotal[:] = []
    L6NestedData[:] = []
    L7MissingData[:] = []
    L8MissingDataURL[:] = []
    L9Exceptions[:] = []
    L10Exceptions_IDs[:] = []
    print('''
    What specialty tasks would you like to perform?
    1. Count data in a specific project
    2. Cound data in a specific fiscal year
    ''')
    answer = input('> ')
    if '1' in answer or 'project' in answer or 'Project' in answer:
        projectDataCount()
    elif '2' in answer or 'Special' in answer or 'special' in answer:
        yearDataCount()
    else:
        print('''
    Sorry, I didnt' understand that.''')
        main()

def projectDataCount(): #finish this later... pass
    print('''
    Is the project in the NWCSC folder or the SWCSC folder?
    ''')
    answer = input('> ')
    if 'nwcsc' in answer or 'NWCSC' in answer or 'n' in answer:
        searchNWCSC()
    elif 'swcsc' in answer or 'SWCSC' in answer or 's' in answer:
        searchSWCSC()
    else:
        print('''
    I didn't understand that input. Let's try that again...''')
        PubSearch()

def yearDataCount():
    print('''
    Which folder would you like to get the data from?
    NWCSC folder or the SWCSC folder?
    ''')
    answer = input('> ')
    if 'nwcsc' in answer or 'NWCSC' in answer or 'n' in answer:
        yearDataCountNWCSC()
    elif 'swcsc' in answer or 'SWCSC' in answer or 's' in answer:
        yearDataCountSWCSC()
    else:
        print('''
    I didn't understand that input. Let's try that again...''')
        yearDataCount()

def yearDataCountNWCSC():
    print(sb.is_logged_in())
    r = sb.get_child_ids('4f8c64d2e4b0546c0c397b46')
    pprint(r)
    print('''
    Here are the fiscal year folders to choose from:
    ''')
    num = 1
    for i in r:
        data = sb.get_item(i)
        print(str(num)+'. '+data['title'])
        num += 1
    print('''
    Now, which folder would you like to count data for?
    (Enter number)
    ''')
    answer = input('> ')
    try:
        val = int(float(answer))
        f = val-1
        folder = r[f]
        doubleCheckNWCSC(folder)

    except ValueError:
        print("That's not a number. Let's try this again.")
        yearDataCountNWCSC()


    #q = sb.get_item(r[0])
    #pprint(q)
    #for i in r:
    #    q = sb.get_child_ids(i)
    #    pprint(q)

def doubleCheckNWCSC(folder):
    r = sb.get_item(folder)
    #pprint(r) #Quantico
    print('''
    Ok, so we're counting the data in '''+r['title']+'''.

    Is that right?
    (Y / N)'''
    )
    answer = input('> ')
    if 'yes' in answer or 'Yes' in answer or 'y' in answer or 'Y' in answer:
         FYdataCount(r, folder)
    elif 'no' in answer or 'No' in answer or 'n' in answer or 'N' in answer:
        print('''
    Ok, let's try this again.''')
        yearDataCountNWCSC()
    else:
        print('''
    Sorry, I didn't understand that. Try typing 'Yes' or 'No' or the first letter of your answer.''')
        doubleCheckNWCSC(folder)

def FYdataCount(r, folder): #this may just create all the variables I will need, as well as create the dictionary of the projects for the fiscal year.
    ChosenFiscalYear.append(r['title'])
    DataHostedElsewhere_id = []
    #DataHostedElsewhere_url = [] #don't probably need this because I can get this from the id later
    CouldNotFindFiles_id = []
    #CouldNotFindFiles_url = [] #don't probably need this because I can get this from the id later
    PossiblePermissionsIssues_id = []
    projectDictNumber = 0
    projectChildDictNumber = 0
    projects = sb.get_child_ids(folder) #these are all the children of the chosen fiscal year
    filesExist = None
    totalProjects = None
    for i in projects:
        if totalProjects == None:
            totalProjects = 0
        else:
            totalProjects += 1
    print("""
    The total number of projects in """+r['title']+""" is """+str(totalProjects+1)
                                                                    +""".""")
    #pprint(projects) #Quantico
    totalFYData = 0 #the total data for the fiscal year starts at 0.
    projectFiles = []

    levelOne(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                                            projectChildDictNumber, filesExist)


def levelOne(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                projectChildDictNumber, filesExist): #this function should go through every project in the fiscal year, and get it's children
    #currentProject = sb.get_item(projects[projectDictNumber]) #This creates a variable for the current project folder in the FY folder
    totalProjectFiles = None
    L7MissingData2 = False  #this automatically sets the default to "no missing data"
    isException = False
    #try:
    currentProject = sb.get_item(projects[projectDictNumber]) #This creates a variable for the current project folder in the FY folder
    #isException = False
    projectChildDictNumber = 0
    print('''
    I am looking through the \''''+str(currentProject['title'])+
                                                        '''' project folder.''')
    L1Project.append(currentProject['title']) #This should add the project's title to a list for exporting to Excel later
    projectFiles = sb.get_child_ids(projects[projectDictNumber]) #this gets the children of the project folder
    totalProjectFiles = None
    for i in projectFiles:
        if totalProjectFiles == None:
            totalProjectFiles = 0
        else:
            totalProjectFiles += 1
    print("""
    The total number of items in this project is """+str(totalProjectFiles+1)
                                                                    +""".""")
    #pprint(projectFiles) #Quantico
    levelTwo(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)
    #except Exception:
    #    exception = projects[projectDictNumber]
    #    isException = True
    #    PossiblePermissionsIssues_id.append(exception)
    #    print('-------------------------------------WARNING(5): '+str(exception)+' raised an Exception or has a Permission issue.')
    #    print('-------------------------------------WARNING: Note that the above Exception or Permission issue is a project folder.')
    #    projectItemNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData,
    #        projectFiles, projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)





def levelTwo(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                        projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2):
        #this function should get the json for every child of the current project. If it can't, it should skip to projectItemNextStep
        #if it can, it should look to see if it is called "approved datasets". If so, it sends that to levelThree
    #currentProjectFileJson = sb.get_item(projectFiles[projectChildDictNumber]) #this is (the json for) every child in the project folder
    #try:
    currentProjectFileJson = sb.get_item(projectFiles[projectChildDictNumber]) #this is (the json for) every child in the project folder
    #isException = False

    print(currentProjectFileJson['title']) #This will print each item name in the project folder
    if currentProjectFileJson['title'] == "Approved DataSets":
        levelThree(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                    projectChildDictNumber, filesExist, totalProjectFiles,
                    currentProjectFileJson, isException, L7MissingData2)
    else:
        projectItemNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData,
            projectFiles, projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)
    #except Exception:
    #    currentProjectFileJson = None
    #    exception = projectFiles[projectChildDictNumber]
    #    isException = True
    #    PossiblePermissionsIssues_id.append(exception)
    #    print('-------------------------------------WARNING(6): '+str(exception)+' raised an Exception or has a Permission issue.')
    #    projectItemNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData,
    #        projectFiles, projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)

def levelThree(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                        projectChildDictNumber, filesExist, totalProjectFiles,
                        currentProjectFileJson, isException, L7MissingData2):
        #this function takes the "approved datasets" item found in levelTwo, get's it's children.
        #if children exist, it sets the number of files to zero (for dict use),
        #set's the amount of times checkChildrenIteration has been activated as 0
        #and calls that functon, passing it all the children of "Approved Datasets" if they exist.

        #If "Approved Datasets" is empty, the amount of data in the project = 0
        #the number of sb items found = 0, the data per file is none, there is
        #no nested data, the running total is the same as before, their is no
        #missing data, or missing data url's, nor any exceptions. So projectItemNextStep is called

    possibleData = sb.get_child_ids(currentProjectFileJson['id']) #I create a var that is all children of "Approved DataSets"
    ApprDataSetsDictPosition = 0

    if possibleData == []:
        filesExist = False
    else:
        filesExist = True
    #print('Files Exist: '+str(filesExist)) #Quantico
    if filesExist == True:
        #pprint(possibleData) #Quantico. This prints out all of the file ids for the files in "Approved DataSets"
        numFiles = 0 #the number of files in Approved DataSets is zero
        timesFunctionHasActivated = 0 #the number of times checkChildrenIteration has been activated is 0
        #isException = False
        checkChildrenIteration(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
            projectChildDictNumber, filesExist, totalProjectFiles, currentProjectFileJson,
            possibleData, numFiles, timesFunctionHasActivated, isException, L7MissingData2)
    elif filesExist == False:
        print('-----No data in this project\'s \'Approved DataSets\' folder.')
        L2DataInProject.append(0)
        L3NumSbItemsFound.append(0)
        L4DataPerFile.append(None)
        L6NestedData.append(None)
        L5RunningDataTotal.append(totalFYData/1000000000)
        #L7MissingData.append(None)
        #L8MissingDataURL.append(None)
        #L9Exceptions.append(None)
        projectItemNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData,
            projectFiles, projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)

def checkChildrenIteration(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
        projectChildDictNumber, filesExist, totalProjectFiles, currentProjectFileJson, possibleData,
        numFiles, timesFunctionHasActivated, isException, L7MissingData2):
        #this function is activated and each time it is it increases it's activation time by 1.
        #It creates a bunch of new empty array variables, and archives the original "possibleData"
        #passed to it as "oldPossibleData"
        #it looks through each item in "possibleData" and tries to read them.
        #IF it can: it then looks to see if it has children.
            #IF it does have children: it addes it to an array "DataWithChildren"
                #then it get's the children of that item, creating a variable for them
                #called 'children2', and it adds each child to an array called "newPossibleData"
                #Then it tries to see if any of those children have weblinks and have data elsewhere
                    #if 'cida.usgs.gov' is one of the weblinks it adds that ID
                        #to 'DataHostedElsewhere_id' and appends L7MissingData2 with True
                        #and L8MissingDataURL with the url of the current child
                    #if 'cida.usgs.gov' is not one of the weblinks, nothing happens
                #if there are no weblinks, nothing happens
                #finally, atLeastOneParentItem is changed to True because some items had had children.
            #IF it doesn't have children it checks the weblinks of the item just like above.
                #and it adds that item to "actualData"

        #IF it can't read the item: it adds the current ID to PossiblePermissionsIssues_id

        #then it looks through "DataWithChildren" and tries to get each entry's info
        #IF it can: it tells you that it has children
        #IF it can't read the item: it adds the current ID to PossiblePermissionsIssues_id

        #IF atLeastOneParentItem is True (an item had had children),
            #it goes through each item in DataWithChildren
            #and tries to remove that entry from possibleData.
            #IF it can (meaning, "if it's there to remove"):
                #Then it sents oldPossibleData equal to possibleData
            #IF the ID isn't in there to remove, it continues on.
            #it then sets 'possibleData' equal to 'oldPossibleData' + 'newPossibleData'
            #IF it is the first time the function was activated, L6NestedData is set to 'Yes'
            #IF it is the first time AND L7MissingData2 is False, L7MissingData
                #is appended with None.
            #IF it is the first time AND L7MissingData2 is True, L7MissingData
                #is appended with "Yes"
            #Then the function calls itself to iterate again.
        #IF atLeastOneParentItem is False (no items had children), and it's the
            #first iteration of the function, it set's L6NestedData to None.
            #IF L7MissingData2 is NOT True, L7MissingData is appended with None
            #IF L7MissingData2 is True, L7MissingData is appended with 'Yes'
            #countData() is called.



    #print('Current Function: checkChildrenIteration') #Quantico
    timesFunctionHasActivated +=1
    DataWithChildren = []
    newPossibleData = []
    oldPossibleData = possibleData
    actualData = []
    atLeastOneParentItem = False
    #print('Possible Data before any editing:') #Quantico
    #pprint(possibleData) #Quantico
    for i in possibleData:
        #possibleDataJson = sb.get_item(i)
        try:
            possibleDataJson = sb.get_item(i)
            #isException = False
            if possibleDataJson['hasChildren'] == True:
                DataWithChildren.append(possibleDataJson['id'])
                children2 = sb.get_child_ids(possibleDataJson['id'])

                for i in children2:
                    newPossibleData.append(i)
                #newPossibleData.append(sb.get_child_ids(possibleDataJson['id'])) #This creates a list within a list
                try:
                    if 'cida.usgs.gov' in possibleDataJson['webLinks']:
                        DataHostedElsewhere_id.append(possibleDataJson['id'])
                        print('-----This possibly has data hosted elsewhere: ') #Quantico
                        pprint(DataHostedElsewhere_id) #Quantico
                        L7MissingData2 = True #MissingDataQuestion
                        L8MissingDataURL.append(i['link']['url'])#MissingDataQuestion

                        #pprint(possibleDataJson['webLinks']) #Quantico
                    else:
                        print('This file does have webLinks, but \"cida.usgs.gov\" not in the web links.')
                        #pprint(possibleDataJson['webLinks']) #Quantico. Use this if you want to double check any items with weblinks

                except KeyError:
                    print('This file doesn\'t have \'webLinks\'.') #Quantico


                atLeastOneParentItem = True

            elif possibleDataJson['hasChildren'] == False:

                try:
                    if 'cida.usgs.gov' in possibleDataJson['webLinks']:
                        DataHostedElsewhere_id.append(possibleDataJson['id'])
                        print('-----This possibly has data hosted elsewhere: ') #Quantico
                        pprint(DataHostedElsewhere_id) #Quantico
                        L7MissingData2 = True #MissingDataQuestion
                        L8MissingDataURL.append(possibleDataJson['link']['url']) #MissingDataQuestion

                        #pprint(possibleDataJson['webLinks']) #Quantico
                    else:
                        print('\"cida.usgs.gov\" not in the web links.')


                        #pprint(possibleDataJson['webLinks']) #Quantico. Use this if you want to double check any items with weblinks
                except KeyError:
                    print('This file doesn\'t have \'webLinks\'.') #Quantico


                actualData.append(possibleDataJson['id'])
            else:
                print('Something went wrong. Current function: checkChildrenIteration')

        except Exception:
            exception = i
            isException = True
            PossiblePermissionsIssues_id.append(exception)
            print('-------------------------------------WARNING(7): '+str(exception)+' raised an Exception or has a Permission issue.')


    for i in DataWithChildren:
        #parent = sb.get_item(i)
        try:
            parent = sb.get_item(i)
            #isException = False
            try:
                print('-----'+str(parent['title'])+' has children.') #Quantico
            except ValueError:
                pass
        except Exception:
            exception = i
            isException = True
            PossiblePermissionsIssues_id.append(exception)
            print('-------------------------------------WARNING(8): '+str(exception)+' raised an Exception or has a Permission issue.')


    if atLeastOneParentItem == True:

        #print('Data with Children: ') #Quantico
        #pprint(DataWithChildren) #Quantico
        #print('New Possible Data: ') #Quantico
        #pprint(newPossibleData) #Quantico

        #print('Old Possible Data (before this iteration of this function)') #Quantico
        #pprint(oldPossibleData) #Quantico
        for parents in DataWithChildren:
            try:
                possibleData.remove(parents)
                oldPossibleData = possibleData
                #print('Old Possible Data once Data With Children is removed:') #Quantico
                #pprint(oldPossibleData) #Quantico
            except ValueError:
                continue
        #possibleData = set(possibleData)
        #possibleData = list(possibleData)
        possibleData = oldPossibleData + newPossibleData
        #possibleData = []
        #for i in oldPossibleData:
        #    possibleData.append(i)
        #for i in newPossibleData:
        #    possibleData.append(i)
        #this should merge lists of unique values (take away duplicates if there are any)

        #print('End result \'Possible Data\' (with Data with Children removed, and New Possible Data added):') #Quantico
        #pprint(possibleData) #Quantico
        print('Let\'s start again!') #Quantico
        if timesFunctionHasActivated == 1:
            L6NestedData.append("Yes")
        #if timesFunctionHasActivated == 1 and L7MissingData2 == False:
        #    L7MissingData.append(None)
        #elif timesFunctionHasActivated == 1 and L7MissingData2 == True:
        #    L7MissingData.append("Yes")


        checkChildrenIteration(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                projectChildDictNumber, filesExist, totalProjectFiles, currentProjectFileJson, possibleData,
                numFiles, timesFunctionHasActivated, isException, L7MissingData2)
    elif atLeastOneParentItem == False:
        #print('Actual Data: ') #Quantico
        #pprint(actualData) #Quantico
        if timesFunctionHasActivated != 1:
             pass
        else:
            L6NestedData.append(None)
        #if timesFunctionHasActivated == 1 and L7MissingData2 != True:
        #    L7MissingData.append(None)
        #elif timesFunctionHasActivated == 1 and L7MissingData2 == True:
        #    L7MissingData.append("Yes")

        countData(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
            projectChildDictNumber, filesExist, totalProjectFiles, currentProjectFileJson,
            actualData, numFiles, json, isException, L7MissingData2)


def levelFour(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
        projectChildDictNumber, filesExist, totalProjectFiles, currentProjectFileJson,
        possibleData, numFiles, json, dataPosWithChildren, dataPosWithoutChildren, isException, L7MissingData2):
    #here, I need to have the positions in dataPosWithChildren each run through a thing to find their children, and if those children have children.
    #THEN I can take that data, and send it to countData
    #change actualData to take away and add the file ids that are what we need.
    print('current function: levelFour') #Quantico

    print('Here\'s the data we have now: ') #Quantico
    pprint(possibleData) #Quantico
    print('Data positions without children: ') #Quantico
    pprint(dataPosWithoutChildren) #Quantico
    print('Data positions with children: ') #Quantico
    pprint(dataPosWithChildren) #Quantico
    #First, find the children of the ids with children
    for ids in dataPosWithChildren:
        childrenOfData = sb.get_child_ids(ids)

    #Second, remove the data in actualData that are folders (i.e. have children)


def countData(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
        projectChildDictNumber, filesExist, totalProjectFiles, currentProjectFileJson,
        actualData, numFiles, json, isException, L7MissingData2):
        #this function counts the data in "actualData" that was populated in checkChildrenIteration
        #first it set's the amount of data to 0, then it creates the emty array forL4_2
        #Then it goes through each item in actualData and tries to get the item data
            #IF it can get the item data:
                #the number of files is increased by 1.
                #the dictionary number is set to 0 and forL4_1 is created and emptied
                #it tries to count the data
                    #IF it can find files, it increases the amount of data by
                        #the size of the file it is on
                        #each file is archived as "thisData" and appended to forL4_1
                        #the file size is printed for each file in each Item
                    #IF there are no 'files' in the item, the ID is appended
                        #to CouldNotFindFiles_id

    print('Alright, let\'s count all this data') #Quantico
    bData = 0 #For "approved datasets" the bytes = 0 at first
    forL4_2 = []
    for data in actualData:
        #try:
        actualDataJson = sb.get_item(data)
        #isException = False
        #pprint(actualDataJson) #Quantico
        numFiles += 1 #for each file, increase the number of Files by 1.

        dictNum = 0 #The dictionary place for each attached file is also 0
        forL4_1 = []
        if forL4_1 != []:
            forL4_1[:] = []

        try:
            for z in actualDataJson['files']: #I try looking at each item in 'approved datasets' and seeing if it has any files attached, if not, I say there aren't any
                bData += actualDataJson['files'][dictNum]['size'] #this adds the size of the file to bData. It cycles through each file in the dataset folder.
                thisData = actualDataJson['files'][dictNum]['size']
                forL4_1.append(thisData)
                dictNum += 1 #this increases the dictionary place so that we move to the next file



                print('File size: '+str(thisData/1000)+' kilobytes.') #at the end, this prints how many bytes total there are after each file in "approved DataSets"
        except KeyError: #if there is no "files" portion in the json, it causes a KeyError. If we get a KeyError...
            CouldNotFindFiles_id.append(actualDataJson['id'])
            print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
            forL4_1.append('[Missing]')
            L7MissingData2 = True
            L8MissingDataURL.append(actualDataJson['link']['url'])
            continue #if we get a KeyError, it's ok. Keep calm and carry on.
        forL4_2.append(forL4_1) #This should add a string representing the sizes of each item in the project to a list for exporting to Excel later

        #except Exception:
        #    exception = data
        #    isException = True
        #    PossiblePermissionsIssues_id.append(exception)
        #    print('-------------------------------------WARNING(9): '+str(exception)+' raised an Exception or has a Permission issue.')
        #    continue


    L4DataPerFile.append(forL4_2)
    if filesExist == True:
        kData = bData/1000 #this tells us how many kilobytes we have from bytes
        mData = kData/1000 #this tells us how many megabytes we have from kilobytes
        gData = mData/1000 #this tells us how many gigabytes we have from megabytes
        L2DataInProject.append(gData) #This should add the amount of data in the project to a list for exporting to Excel later
        L3NumSbItemsFound.append(numFiles) #This should add the number of items in the project to a list for exporting to Excel later
        #global totalDataCount += int(bData) #COME BACK TO THIS LATER
        print('----I found '+str(numFiles)+' item(s) in this '+
        'project\'s '+'\'Approved Dataset\' folder, bringing the total data in this project to '+
        str(kData)+' kilobytes, or '+str(mData)+' megabytes, or '+
        str(gData)+' gigabytes.')
        totalFYData += bData
        print('----So far, our total data for the fiscal year is '+str(totalFYData/1000000000)+' gigabytes.')
        L5RunningDataTotal.append(totalFYData/1000000000) #This should add the running total of all data for the fiscal year to a list for exporting to Excel later
    else:
        print('Something went wrong. Current function: countData')


    projectItemNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                            projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)


def projectItemNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                        projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2):

    projectChildDictNumber += 1
#    L7MissingData.append(None)
#    L8MissingDataURL.append(None)
#    L9Exceptions.append(None)
    if totalProjectFiles == None:
        projectFolderNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData,
            projectFiles, projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)
    elif projectChildDictNumber <= totalProjectFiles:
        #print('-----More files in the project folder') #Quantico
        levelTwo(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                        projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)
    elif projectChildDictNumber > totalProjectFiles:
        #print('-----No more files in the project folder') #Quantico
        projectFolderNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData,
            projectFiles, projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2)

    else:
        print('''
    Something went wrong. Current function: ProjectItemNextStep''')

def projectFolderNextStep(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                        projectChildDictNumber, filesExist, totalProjectFiles, isException, L7MissingData2):
    projectDictNumber += 1
    if L7MissingData2 == False:
        L7MissingData.append(None)
    elif L7MissingData2 == True:
        L7MissingData.append("Yes")
    if isException == True:
        L9Exceptions.append("Yes")
    elif isException == False:
        L9Exceptions.append(None)
    if projectDictNumber <= totalProjects:
        levelOne(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalProjects, projectDictNumber, projects, totalFYData, projectFiles,
                    projectChildDictNumber, filesExist)
    elif projectDictNumber > totalProjects:
        doneCountingFY(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalFYData)




def doneCountingFY(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalFYData):
    totalkData = totalFYData/1000 #this tells us how many kilobytes we have from bytes
    totalmData = totalkData/1000 #this tells us how many megabytes we have from kilobytes
    totalgData = totalmData/1000 #this tells us how many gigabytes we have from megabytes
    print('''
    In total, I found '''+str(totalFYData)+''' bytes of data in '''+r['title']+
    '''.

    This comes out to '''+str(totalkData)+''' kilobytes, or '''+str(totalmData)+
    ''' megabytes, or '''+str(totalgData)+''' gigabytes.
    ''')x
    issueDiagnostics(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalFYData)

def issueDiagnostics(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalFYData):
    if DataHostedElsewhere_id == [] and CouldNotFindFiles_id == []:
        print('''
    There appear to be no abnormalities when tallying data.
        ''')
        #pprint(DataHostedElsewhere_id) #Quantico
        #pprint(CouldNotFindFiles_id) #Quantico
        permissionsAndExceptionsDiagnostics(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id)

    elif CouldNotFindFiles_id == [] and not DataHostedElsewhere_id == []:
        print('''
    NOTE: There appear to be items that could contain data hosted somewhere
          other than ScienceBase. Here are the items of concern:
        ''')
        for i in DataHostedElsewhere_id:
            #json = sb.get_item(i)
            try:
                json = sb.get_item(i)
                isException = False
            except Exception:
                exception = i
                isException = True
                PossiblePermissionsIssues_id.append(exception)
                print('-------------------------------------WARNING(1): '+str(exception)+' raised an Exception or has a Permission issue.')

            try:
                itemTitle = json['title']
                itemID = json['id']
                itemURL = json['link']['url']
                print('''

            Item Title: '''+str(itemTitle)+'''
            Item ID: '''+str(itemID)+'''
            Item URL: '''+str(itemURL)+'''

            ''')
            except KeyError:
                print('There was an error getting item details. Here is the item ID:')
                print(str(i))


        #pprint(DataHostedElsewhere_id) #Quantico
        #pprint(CouldNotFindFiles_id) #Quantico
        permissionsAndExceptionsDiagnostics(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id)

    elif DataHostedElsewhere_id == [] and not CouldNotFindFiles_id == []:
        print('''
    NOTE: There appear to be items within the 'Approved DataSets' folder that
          did not contain any data. You may want to manually check them. Here are
          the items of concern:
        ''')
        for i in CouldNotFindFiles_id:
            #json = sb.get_item(i)
            try:
                json = sb.get_item(i)
                isException = False
                try:
                    itemTitle = json['title']
                    itemID = json['id']
                    itemURL = json['link']['url']
                    print('''

                Item Title: '''+str(itemTitle)+'''
                Item ID: '''+str(itemID)+'''
                Item URL: '''+str(itemURL)+'''

                ''')
                except KeyError:
                    print('There was an error getting item details. Here is the item ID:')
                    print(str(i))
            except Exception:
                exception = i
                isException = True
                PossiblePermissionsIssues_id.append(exception)
                print('-------------------------------------WARNING(2): '+str(exception)+' raised an Exception or has a Permission issue.')


        permissionsAndExceptionsDiagnostics(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id)
        #pprint(DataHostedElsewhere_id) #Quantico
        #pprint(CouldNotFindFiles_id) #Quantico
    elif not DataHostedElsewhere_id == [] and not CouldNotFindFiles_id == []:
        print('''
    NOTE: There appear to be items that could contain data hosted somewhere
          other than ScienceBase. Here are the items of concern:
        ''')
        for i in DataHostedElsewhere_id:
            #json = sb.get_item(i)
            try:
                json = sb.get_item(i)
                isException = False
            except Exception:
                exception = i
                isException = True
                PossiblePermissionsIssues_id.append(exception)
                print('-------------------------------------WARNING(3): '+str(exception)+' raised an Exception or has a Permission issue.')

            try:
                itemTitle = json['title']
                itemID = json['id']
                itemURL = json['link']['url']
                print('''

            Item Title: '''+str(itemTitle)+'''
            Item ID: '''+str(itemID)+'''
            Item URL: '''+str(itemURL)+'''

            ''')
            except KeyError:
                print('There was an error getting item details. Here is the item ID:')
                print(str(i))

        print('''
    NOTE: There appear to be items within the 'Approved DataSets' folder that
          did not contain any data. You may want to manually check them. Here are
          the items of concern:
        ''')
        for i in CouldNotFindFiles_id:
            #json = sb.get_item(i)
            try:
                json = sb.get_item(i)
                isException = False
            except Exception:
                exception = i
                isException = True
                PossiblePermissionsIssues_id.append(exception)
                print('-------------------------------------WARNING(4): '+str(exception)+' raised an Exception or has a Permission issue.')

            try:
                itemTitle = json['title']
                itemID = json['id']
                itemURL = json['link']['url']
                print('''

            Item Title: '''+str(itemTitle)+'''
            Item ID: '''+str(itemID)+'''
            Item URL: '''+str(itemURL)+'''

            ''')
            except KeyError:
                print('There was an error getting item details. Here is the item ID:')
                print(str(i))
        permissionsAndExceptionsDiagnostics(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id)

        #pprint(DataHostedElsewhere_id) #Quantico
        #pprint(CouldNotFindFiles_id) #Quantico
    else:
        print("Something went wrong. Current function: doneCountingFY")

def permissionsAndExceptionsDiagnostics(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id):
    #We sometimes get the following exception: Exception("Resource not found, or user does not have access"
    if PossiblePermissionsIssues_id == []:
        print('''


    There were no Exceptions raised or Permission issues while accessing files.

    ''')
        for i in L9Exceptions:
            L10Exceptions_IDs.append(i)

    else:
        print('''


    The following item's raised Exeptions or had Permission issues when accessing them:

    ''')
        for i in PossiblePermissionsIssues_id:
            print("- "+str(i))
        for i in L9Exceptions:
            L10Exceptions_IDs.append(i)
        print(L10Exceptions_IDs)
        position = 0
        for i in L10Exceptions_IDs:
            if i == "Yes":
                i = PossiblePermissionsIssues_id[position]
                position += 1
            else:
                continue
    printToExcel(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id)


def printToExcel(DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id):
    print(ChosenFiscalYear)
    print(L1Project)
    print(L2DataInProject)
    print(L3NumSbItemsFound)
    print(L4DataPerFile)
    print(L5RunningDataTotal)
    print(L6NestedData)
    print('Missing:')
    print(L7MissingData)
    print(L8MissingDataURL)
    print("Exceptions:")
    print(L9Exceptions)
    print(L10Exceptions_IDs)

    print(len(ChosenFiscalYear))
    print(len(L1Project))
    print(len(L2DataInProject))
    print(len(L3NumSbItemsFound))
    print(len(L4DataPerFile))
    print(len(L5RunningDataTotal))
    print(len(L6NestedData))
    print('Missing:')
    print(len(L7MissingData))
    print(len(L8MissingDataURL))
    print("Exceptions:")
    print(len(L9Exceptions))
    print(len(L10Exceptions_IDs))

    print('Missing')
    print(CouldNotFindFiles_id)

    print('Hosted elsewhere?')
    print(DataHostedElsewhere_id)

    print("Possible Permission Issues:")
    print(PossiblePermissionsIssues_id)

    print('''
    Would you like to print the results to an Excel file?
    (Y / N)
            ''')
    answer = input('> ')
    if 'y' in answer or 'Y' in answer or "yes" in answer or "Yes" in answer:
        import ExcelPrint
        ExcelPrint.mainExcel(ChosenFiscalYear, L1Project, L2DataInProject, L3NumSbItemsFound,
                L5RunningDataTotal, L6NestedData, L7MissingData,
                L8MissingDataURL, L9Exceptions, L10Exceptions_IDs, CouldNotFindFiles_id,
                DataHostedElsewhere_id, PossiblePermissionsIssues_id)

    elif 'no' in answer or 'No' in answer or 'n' in answer or 'N' in answer:
        nowWhat()
    else:
        print('''
    I'm sorry, I didn't get that.''')


def nowWhat():
    print('''
    Now What would you like to do?
    1. Go back to login
    2. Count data in another fiscal year
    (Type number)''')
    answer = input('> ')

    if '1' in answer:
        import start
        start.questionLogin()
    elif '2' in answer:
        main()

if __name__ == '__main__':
    main()
    #yearDataCountNWCSC()


sb.logout()
