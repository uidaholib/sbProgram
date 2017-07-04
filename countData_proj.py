import g
import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()



def main(actualData):
    numFiles = 0 # starting number of files in Approved Datasets is 0
    countData(actualData, numFiles)


def countData(actualData, numFiles):
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
    filesExist = False
    for data in actualData:
        foundData = False
        actualDataJson = sb.get_item(data)
        #pprint(actualDataJson) #Quantico
        numFiles += 1 #for each file, increase the number of Files by 1.
        facetDictNum = 0
        dictNum = 0 #The dictionary place for each attached file is also 0
        forDataPerFile_1 = []
        if forDataPerFile_1 != []:
            forDataPerFile_1[:] = []

        try:
            for z in actualDataJson['files']: #I try looking at each item in 'approved datasets' and seeing if it has any files attached, if not, I say there aren't any
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
                            print("Extention size: "+str(i['size']/1000)+ " kilobytes")
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
                                if data not in g.MissingData:
                                    g.MissingData.append(actualDataJson['id'])
                                else:
                                    print("---------Something went wrong. Current"+
                                          " Function: countData (1)")
                                    print(str(data)+" already in g.MissingData.")
                        except KeyError:
                            print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                            forDataPerFile_1.append('[Missing]')
                            if data not in g.MissingData:
                                g.MissingData.append(actualDataJson['id'])
                            else:
                                print("---------Something went wrong. Current"+
                                      " Function: countData (2)")
                                print(str(data)+" already in g.MissingData.")
                         #if we get a KeyError, it's ok. Keep calm and carry on.



                print('File size: '+str(thisData/1000)+' kilobytes.') #at the end, this prints how many bytes total there are after each file in "approved DataSets"
        except KeyError: #if there is no "files" portion in the json, it causes a KeyError. If we get a KeyError...
            try:
                for z in actualDataJson['facets']:
                    for i in z['files']:
                        print("Extention size: "+str(i['size']/1000)+ "kilobytes")
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
                            if data not in g.MissingData:
                                g.MissingData.append(actualDataJson['id'])
                            else:
                                print("---------Something went wrong. Current"+
                                      " Function: countData (2)")
                                print(str(data)+" already in g.MissingData.")
                    except KeyError:
                        print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                        forDataPerFile_1.append('[Missing]')
                        if data not in g.MissingData:
                            g.MissingData.append(actualDataJson['id'])
                        else:
                            print("---------Something went wrong. Current"+
                                  " Function: countData (2)")
                            print(str(data)+" already in g.MissingData.")
        forDataPerFile_2.append(forDataPerFile_1) #This should add a string representing the sizes of each item in the project to a list for exporting to Excel later


    g.DataPerFile.append(str(forDataPerFile_2))
    if filesExist == True:
        kData = bData/1000 #this tells us how many kilobytes we have from bytes
        mData = kData/1000 #this tells us how many megabytes we have from kilobytes
        gData = mData/1000 #this tells us how many gigabytes we have from megabytes
        g.DataInProject.append(gData) #This should add the amount of data in the project to a list for exporting to Excel later
        #global totalDataCount += int(bData) #COME BACK TO THIS LATER
        print('----I found '+str(numFiles)+' item(s) in this '+
        'project\'s '+'\'Approved Dataset\' folder, bringing the total data in this project to '+
        str(kData)+' kilobytes, or '+str(mData)+' megabytes, or '+
        str(gData)+' gigabytes.')
        g.totalDataCount += gData
        g.totalFYData += gData
        print('----So far, our total data for the fiscal year is '+str(g.totalFYData)+' gigabytes.')
        g.RunningDataTotal.append(g.totalDataCount) #This should add the running total of all data for the fiscal year to a list for exporting to Excel later

    else:
        print('No Files exist in actualData. Current function: countData (3)')

    return


def doneCountingFY():
    totalkData = g.totalFYData/1000 #this tells us how many kilobytes we have from bytes
    totalmData = totalkData/1000 #this tells us how many megabytes we have from kilobytes
    totalgData = totalmData/1000 #this tells us how many gigabytes we have from megabytes

    r = g.FiscalYear[-1]  # r is the last reported fiscal year. Most recent list item.
    print('''
    In total, I found '''+str(g.totalFYData)+''' bytes of data in '''+str(r)+
    '''.

    This comes out to '''+str(totalkData)+''' kilobytes, or '''+str(totalmData)+
    ''' megabytes, or '''+str(totalgData)+''' gigabytes.
    ''')
    return


if __name__ == '__main__':
    actualData = ["561bf56fe4b0cdb063e5837f"]
    main(actualData)
