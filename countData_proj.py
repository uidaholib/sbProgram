







def main(actualData):
    numFiles = 0 # starting number of files in Approved Datasets is 0
    countData(actualData)

def countData(actualData):
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
                bData += actualDataJson['files'][dictNum]['size'] #this adds the size of the file to bData. It cycles through each file in the dataset folder.
                thisData = actualDataJson['files'][dictNum]['size']
                foundData = True
                forDataPerFile_1.append(thisData)
                dictNum += 1 #this increases the dictionary place so that we move to the next file
                try:
                    for z in actualDataJson['facets']['files']:
                        bData += actualDataJson['facets']['files'][facetDictNum]['size']
                        thisData = actualDataJson['facets']['files'][facetDictNum]['size']
                        foundData = True
                        forDataPerFile_1.append(thisData)
                        facetDictNum += 1
                except KeyError:
                    if foundData is True:
                        pass
                    elif foundData is not True:
                        print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                        forDataPerFile_1.append('[Missing]')
                        g.MissingData.append(actualDataJson['id'])
                        continue #if we get a KeyError, it's ok. Keep calm and carry on.



                print('File size: '+str(thisData/1000)+' kilobytes.') #at the end, this prints how many bytes total there are after each file in "approved DataSets"
        except KeyError: #if there is no "files" portion in the json, it causes a KeyError. If we get a KeyError...
            try:
                for z in actualDataJson['facets']['files']:
                    bData += actualDataJson['facets']['files'][facetDictNum]['size']
                    thisData = actualDataJson['facets']['files'][facetDictNum]['size']
                    forDataPerFile_1.append(thisData)
                    facetDictNum += 1
            except KeyError:
                if foundData is True:
                    pass
                elif foundData is not True:
                    print("----No files in "+str(actualDataJson['id'])) #we print this if we get a KeyError
                    forDataPerFile_1.append('[Missing]')
                    g.MissingData.append(actualDataJson['id'])
                    continue #if we get a KeyError, it's ok. Keep calm and carry on.
        forDataPerFile_2.append(forDataPerFile_1) #This should add a string representing the sizes of each item in the project to a list for exporting to Excel later


    DataPerFile.append(forDataPerFile_2)
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
        totalFYData += bData
        print('----So far, our total data for the fiscal year is '+str(totalFYData/1000000000)+' gigabytes.')
        g.RunningDataTotal.append(totalFYData/1000000000) #This should add the running total of all data for the fiscal year to a list for exporting to Excel later
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
    ''')
    issueDiagnostics(r, DataHostedElsewhere_id, PossiblePermissionsIssues_id, CouldNotFindFiles_id, totalFYData)
