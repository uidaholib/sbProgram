import gl
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify
import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()



def main(currentProject, actualData):
    numFiles = 0 # starting number of files in Approved Datasets is 0
    countData(currentProject, actualData, numFiles)


def countData(currentProject, actualData, numFiles):
        #this function counts the data in "actualData" that was populated in checkChildrenIteration
        #first it set's the amount of data to 0, then it creates the emty array forDataPerFile_2
        #Then it goes through each item in actualData and tries to get the item data
            #IF it can get the item data:
                #the number of files is increased by 1.
                #the dictionary number is set to 0 and forDataPerFile_1 is created and emptied
                #it tries to count the data
                    #IF it can find files, it increases the amount of data by
                        #the size of the file it is on
                        #each file is archived as "thisData" and appended to forDataPerFile_1
                        #the file size is printed for each file in each Item
                    #IF there are no 'files' in the item, the ID is appended
                        #to CouldNotFindFiles_id

    print('Alright, let\'s count all this data') #Quantico
    bData = 0 #For "approved datasets" the bytes = 0 at first
    
    forDataPerFile_2 = []

    # print("forDataPerFile_2: {0}".format(forDataPerFile_2))  # Quantico
    filesExist = False
    
    # create a list to track items
    projItemList = []
    # create a variable to track item count
    projItemCount = 0
    # create a list to track files
    projFileList = []
    # create a variable to track file count
    projFileCount = 0
    print("gl.ProjFiles: (1)")
    print(gl.ProjFiles)
    for data in actualData:
        
        foundData = False
        try:
            actualDataJson = sb.get_item(data)
        except Exception:
            import parseFY
            parseFY.exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(data)+" (1)")
            parseFY.exceptionLoop(data)
            actualDataJson = sb.get_item(data)
            # old exception handling:
            # import exceptionRaised
            # exceptionRaised.main(data)
            # if exceptionRaised.worked is True:
            #     actualDataJson = sb.get_item(data)
            # elif exceptionRaised.worked is False:
            #     continue
            # else:
            #     print('Something went wrong. Function: countData (1)')
            
        # each "data" is an item in the "Approved Datasets" folder, so for each one, add one to our count.
        projItemCount += 1 # each "data" is an item in the "Approved Datasets" folder, so for each one, add one to our count.
        # We create an item object/dictionary
        Item = {}
        #For each item, we take the name and url and add it to a list of items filed under the project id key.
        Item['url'] = actualDataJson['link']['url']
        Item['id'] = actualDataJson['id']
        Item['name'] = actualDataJson['title']
        Item['hasChildren'] = actualDataJson['hasChildren']
        if 'browseTypes' in actualDataJson:
            Item['browseTypes'] = actualDataJson['browseTypes']
        else:
            Item['browseTypes'] = "None provided by ScienceBase"
        if 'systemTypes' in actualDataJson:
            Item['systemType'] = actualDataJson['systemTypes']
        else:
            Item['systemType'] = "None provided by ScienceBase"
        if 'dates' in actualDataJson:
            Item['dates'] = actualDataJson['dates']
        else:
            Item['dates'] = "None provided by ScienceBase"




        #then we add the item to the projItemList
        projItemList.append(Item)
        #pprint(actualDataJson) #Quantico
        numFiles += 1 #for each file, increase the number of Files by 1.
        facetDictNum = 0
        dictNum = 0 #The dictionary place for each attached file is also 0
        forDataPerFile_1 = []
        # print("forDataPerFile_1: {0}".format(forDataPerFile_1))  # Quantico
        if forDataPerFile_1 != []:
            forDataPerFile_1[:] = []

        try:
            for z in actualDataJson['files']: #I try looking at each item in 'approved datasets' and seeing if it has any files attached, if not, I say there aren't any
                # for each file, increase projFileCount by one
                projFileCount += 1
                print("projFileCount: 1")
                print(projFileCount)

                # for each file, add it to the files list
                projFileList.append(z)
                print("projFileList: 1")
                print(projFileList[-1])
                filesExist = True
                bData += actualDataJson['files'][dictNum]['size'] #this adds the size of the file to bData. It cycles through each file in the dataset folder.
                thisData = actualDataJson['files'][dictNum]['size']/1000
                foundData = True
                forDataPerFile_1.append(thisData)
                dictNum += 1 #this increases the dictionary place so that we move to the next file
                facetFileDictNum = 0
                try:
                    for z in actualDataJson['facets']:
                        for i in z['files']:
                            # for each extension, increase projFileCount by one
                            projFileCount += 1
                            print("projFileCount: 2")
                            print(projFileCount)
                            # for each extension, add it's file to the files list
                            projFileList.append(i)
                            print("projFileList: 2")
                            print(projFileList[-1])
                            # print("Extension size: "+str(i['size']/1000)+ " kilobytes")  # Quantico
                            filesExist = True
                            bData += i['size']
                            thisData = i['size']/1000
                            foundData = True
                            forDataPerFile_1.append(thisData)
                except KeyError:
                    if foundData is True:
                        filesExist = True
                    elif foundData is not True:
                        try:
                            if 'Folder' in actualDataJson['systemTypes']:
                                print("----Item is a folder. No attached files.")
                            else:
                                print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                                forDataPerFile_1.append('[Missing]')
                                if data not in gl.MissingData:
                                    gl.MissingData.append(actualDataJson['id'])
                                else:
                                    print("---------Something went wrong. Current"+
                                          " Function: countData (1)")
                                    print(str(data)+" already in gl.MissingData.")
                        except KeyError:
                            print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                            forDataPerFile_1.append(['Missing'])
                            if data not in gl.MissingData:
                                gl.MissingData.append(actualDataJson['id'])
                            else:
                                print("---------Something went wrong. Current"+
                                      " Function: countData (2)")
                                print(str(data)+" already in gl.MissingData.")
                         #if we get a KeyError, it's ok. Keep calm and carry on.



                # print('File size: '+str(thisData/1000)+' kilobytes.')  # Quantico
                # ^ at the end, this prints how many bytes total there are after each file in "approved DataSets"
        except KeyError: #if there is no "files" portion in the json, it causes a KeyError. If we get a KeyError...
            try:
                for z in actualDataJson['facets']:
                    for i in z['files']:
                        # print("Extension size: "+str(i['size']/1000)+ "kilobytes")  # Quantico
                        # for each extension, increase projFileCount by one
                        projFileCount += 1
                        print("projFileCount: 3")
                        print(projFileCount)
                        # for each extension, add it's file to the files list
                        projFileList.append(i)
                        print("projFileList: 3")
                        print(projFileList[-1])
                        filesExist = True
                        bData += i['size']
                        thisData = i['size']/1000
                        foundData = True
                        forDataPerFile_1.append(thisData)
            except KeyError:
                if foundData is True:
                    filesExist = True
                elif foundData is not True:
                    try:
                        if 'Folder' in actualDataJson['systemTypes']:
                            print("----Item is a folder. No attached files.")
                        else:
                            print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                            forDataPerFile_1.append('[Missing]')
                            if data not in gl.MissingData:
                                gl.MissingData.append(actualDataJson['id'])
                            else:
                                print("---------Something went wrong. Current"+
                                      " Function: countData (2)")
                                print(str(data)+" already in gl.MissingData.")
                    except KeyError:
                        print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                        forDataPerFile_1.append('[Missing]')
                        if data not in gl.MissingData:
                            gl.MissingData.append(actualDataJson['id'])
                        else:
                            print("---------Something went wrong. Current"+
                                  " Function: countData (2)")
                            print(str(data)+" already in gl.MissingData.")
        forDataPerFile_2.append(forDataPerFile_1) #This should add a string representing the sizes of each item in the project to a list for exporting to Excel later


    gl.DataPerFile.append(forDataPerFile_2)
    print("Here is the data per file added to gl.DataPerFile for this project:\n{0}".format(forDataPerFile_2))
    print("\n\nHere is gl.DataPerFile:\n{0}".format(gl.DataPerFile))
    if filesExist == True:
        kData = bData/1000 #this tells us how many kilobytes we have from bytes
        mData = kData/1000 #this tells us how many megabytes we have from kilobytes
        gData = mData/1000 #this tells us how many gigabytes we have from megabytes
        gl.DataInProject.append(gData) #This should add the amount of data in the project to a list for exporting to Excel later
        #global totalDataCount += int(bData) #COME BACK TO THIS LATER
        print('----I found '+str(numFiles)+' item(s) in this '+
        'project\'s '+'\'Approved Dataset\' folder, bringing the total data in this project to '+
        str(kData)+' kilobytes, or '+str(mData)+' megabytes, or '+
        str(gData)+' gigabytes.')
        # flash('----I found '+str(numFiles)+' item(s) in this '+
        # 'project\'s '+'\'Approved Dataset\' folder, bringing the total data in this project to '+
        # str(kData)+' kilobytes, or '+str(mData)+' megabytes, or '+
        # str(gData)+' gigabytes.')
        gl.totalDataCount += gData
        gl.totalFYData += gData
        print('----So far, our total data for the fiscal year is '+str(gl.totalFYData)+' gigabytes.')
        # flash('----So far, our total data for the fiscal year is '+str(gl.totalFYData)+' gigabytes.')
        gl.RunningDataTotal.append(gl.totalDataCount) #This should add the running total of all data for the fiscal year to a list for exporting to Excel later

    else:
        gl.DataInProject.append("None")
        gl.RunningDataTotal.append(gl.totalDataCount)
        print('No Files exist in actualData. Current function: countData (3)')

    #create the project id key to find project item data in gl.ProjItems. The key leads to an object containing the item count and a list of all items in the project.
    gl.ProjItems[currentProject] = {}
    gl.ProjItems[currentProject]['Project_Item_List'] = projItemList
    gl.ProjItems[currentProject]['Project_Item_Count'] = projItemCount
    #create the project id key to find project file data in gl.ProjFiles. The key leads to an object containing a file count and a list of all files in the project.
    gl.ProjFiles[currentProject] = {}
    gl.ProjFiles[currentProject]['Project_File_List'] = projFileList
    gl.ProjFiles[currentProject]['Project_File_Count'] = projFileCount

    return


def doneCountingFY():
    totalkData = gl.totalFYData*1000000 #this tells us how many kilobytes we have from bytes
    totalmData = totalkData/1000 #this tells us how many megabytes we have from kilobytes
    totalgData = totalmData/1000 #this tells us how many gigabytes we have from megabytes
    number = len(gl.FiscalYear)
    for i in range(0, number):
        gl.totalFYDataList.append(gl.totalFYData)


    print("totalFYDataList:")
    for i in gl.totalFYDataList:
        print(i, end="")
    print("\nList length: {0}".format(len(gl.totalFYDataList)))
    r = gl.FiscalYear[-1]  # r is the last reported fiscal year. Most recent list item.
    print('''
    In total, I found '''+str(gl.totalFYData)+''' gigabytes of data in '''+str(r)+
    '''.

    This comes out to '''+str(totalkData)+''' kilobytes, or '''+str(totalmData)+
    ''' megabytes, or '''+str(totalgData)+''' gigabytes.
    ''')
    # flash('''
    # In total, I found '''+str(gl.totalFYData)+''' gigabytes of data in '''+str(r)+
    # '''.

    # This comes out to '''+str(totalkData)+''' kilobytes, or '''+str(totalmData)+
    # ''' megabytes, or '''+str(totalgData)+''' gigabytes.
    # ''')
    return


if __name__ == '__main__':
    actualData = ["561bf56fe4b0cdb063e5837f"]
    main(actualData)
