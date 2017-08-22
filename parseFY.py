import g
import requests
import json
import pysb
import sys
import time

from pprint import pprint

sb = pysb.SbSession()

totalDataCount = 0
projectDictNumber = 0
possibleProjectData = []
exceptionFound = False
#lookedForShortcutsBefore = False       #Taking away all lookedForShortcutsBefore.
lookedForDataBefore = False                 #Not sure of the purpose if we add only the shortcuts
FYprojects = []                             # that aren't already in possibleProjectData already.
                                            # So there's no difference between how we would treat
doubleCheck = None                          #data if we'd looked before or not.
firstFYParse = True
veryFirstFYParse = True
FYdictNum = 0

def main():
    global possibleProjectData
    possibleProjectData[:] = []
    print("parseFY.py main") # Quantico
    global firstFYParse
    global FYprojects
    global projectDictNumber
    global doubleCheck
    global veryFirstFYParse
    if firstFYParse is True:
        projectDictNumber = 0
        getProjects()
        if veryFirstFYParse is True:
            print('''
            Firstly, as I go through each project in this Fiscal Year, would you '''+
            '''like me to double check with you after each project that you want to'''+
            ''' continue?
            (Y / N)
                  ''')
            answer = input("> ").lower()
            if 'y' in answer:
                doubleCheck = True
            elif 'n' in answer:
                doubleCheck = False
            else:
                print("Please type 'y' or 'n'.")
                main()
            veryFirstFYParse = False
        firstFYParse = False
    if projectDictNumber is 1000:
        return




    print(FYprojects)  # Quantico
    # maybe here just do: for i in FY projects, i = currentProject, getProjectData
    # Maybe have it work for each FY and have at the end, would you like to print just this FY to a spreadsheet
    # then delete everything if it does, and continue with everything if not.
    print("dict number: "+str(projectDictNumber))  # Quantico
    try:
        currentProject = FYprojects[projectDictNumber]
    except IndexError:
        return
    print("currentProject: "+str(currentProject))  # Quantico
    getProjectData(possibleProjectData, FYprojects,
                   currentProject, exceptionFound,
                   )

def getProjects():
    global possibleProjectData
    global projectDictNumber
    possibleProjectData[:] = []
    global FYprojects
    FYprojects[:] = []
    global FYdictNum
    try:
        i = g.fiscalYears[FYdictNum]
        print(i)  # Quantico
    except IndexError:
        print("No more fiscal years.")
        FYprojects[:] = []
        projectDictNumber = 1000
        return
    print("Found g.fiscalYears item.")  # Quantico
    print(i)
    currentFYprojects = sb.get_child_ids(i)
    print(currentFYprojects)  # Quantico
    for project in currentFYprojects:
        projectJson = sb.get_item(project)
        try:
            if "Project" in projectJson["browseCategories"] and project not in FYprojects:
                print("--Item is a project.")
                FYprojects.append(project)
            elif "Project" in projectJson["browseCategories"] and project in FYprojects:
                print("--Item already parsed.")
            else:
                print("browseCategories = "+str(projectJson["browseCategories"]))
        except KeyError:
            print("--"+str(project)+" not a project.")
            print("Quickly parsing "+str(i)+" to determine what it is...")
            print("======================================================")
            g.onTheFlyParsing.append(i)
            import parse
            parse. parseOnTheFly()
            print("Back to finding projects...")
            main()
    return FYprojects



def getProjectData(possibleProjectData, FYprojects,
                   currentProject, exceptionFound,
                   ):
    global lookedForDataBefore
    projectItems = sb.get_child_ids(currentProject)
    currentProjectJson = sb.get_item(currentProject)
    if lookedForDataBefore is False:
        populateGPYLists(currentProject, currentProjectJson)
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


    parse(possibleProjectData, FYprojects, projectItems,
          currentProject, exceptionFound,
          currentProjectJson)


def populateGPYLists(currentProject, currentProjectJson):
    g.ID.append(currentProject)
    print(g.ID)  # Quantico
    g.ObjectType.append("Project")
    print(g.ObjectType)  # Quantico
    g.Name.append(currentProjectJson["title"])
    print(g.Name)  # Quantico
    findCurrentProjectFY(currentProject, currentProjectJson)
    print(g.FiscalYear)  # Quantico
    g.Project.append("Self")
    print(g.Project)  # Quantico
    return

def printAllGLists():
    print(g.ID)  # Quantico
    print(g.ObjectType)  # Quantico
    print(g.Name)  # Quantico
    print(g.FiscalYear)  # Quantico
    print(g.Project)  # Quantico
    print(g.DataInProject)  # Quantico
    print(len(g.DataPerFile)) # Quantico
    print(g.RunningDataTotal)  # Quantico

def findCurrentProjectFY(currentProject, currentProjectJson):
    currentId = currentProject[:]
    json = currentProjectJson
    parentId = currentProjectJson["parentId"]
    try:
        children = sb.get_child_ids(currentId)
    except Exception:
        exceptionFound = True
        print("--------Hit upon a 404 exception: "+str(i)+" (1)")
        import exceptionRaised
        exceptionRaised.main(i)
        if exceptionRaised.worked is True:
            children = sb.get_child_ids(currentId)
        elif exceptionRaised.worked is False:
            FY = "Exception Raised: Could not find Fiscal Year"
            print("Exception Raised: Could not find Fiscal Year.")
            g.FiscalYear.append(FY)
            return
        else:
            print('Something went wrong. Function: findCurrentProjectFY() (2.2)')
    try:
        child = children[0]
    except KeyError:
        print("No children of the current item.")
        currentId = parentId[:]  # this makes a slice that is the whole list.
        json = sb.get_item(currentId)
        parentId = json['parentId']
        children = sb.get_child_ids(currentId)
        child = children[0]
    childJson = sb.get_item(child)
    if 'FY' in json['title']:
        print("Item is a Fiscal Year")  # Quantico
        g.fiscalYears.append(json['title'])
        return
    control = True
    while control is True:
        try:
            while 'Project' not in childJson['browseCategories']:
                currentId = parentId[:]  # this makes a slice that is the whole list.
                json = sb.get_item(currentId)
                parentId = json['parentId']
                children = sb.get_child_ids(currentId)
                child = children[0]
                childJson = sb.get_item(child)
                print("Not a Fiscal Year.")  # Quantico
        except KeyError:
            currentId = parentId[:]  # this makes a slice that is the whole list.
            json = sb.get_item(currentId)
            parentId = json['parentId']
            try:
                children = sb.get_child_ids(currentId)
            except Exception:
                import parseFY
                parseFY.exceptionFound = True
                print("--------Hit upon a 404 exception: "+str(i)+" (1)")
                import exceptionRaised
                exceptionRaised.main(data)
                if exceptionRaised.worked is True:
                    children = sb.get_child_ids(currentId)
                elif exceptionRaised.worked is False:
                    continue
                else:
                    print('Something went wrong. Function: findCurrentProjectFY (1)')
            child = children[0]
            childJson = sb.get_item(child)
            print("Not a Fiscal Year.")
            continue
        if 'Project' in childJson['browseCategories']:
            control = False
    FY = json['title'].replace(" Projects", "")
    print("appending \'"+str(json['title'])+'\' as '+str(FY))  # Quantico
    g.FiscalYear.append(FY)
    return

    #do a "while" loop here. Something like, while the children of the current thing are NOT projects...
    #and when they are, take the ['title'] and append that to g.FiscalYear and return

def parse(possibleProjectData, FYprojects, projectItems,
          currentProject, exceptionFound,
          currentProjectJson):
    possibleProjectData_Set = set()
    for i in possibleProjectData:
        possibleProjectData_Set.update(possibleProjectData)
        try:
            ancestors = sb.get_ancestor_ids(i)
        except Exception:
            exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(i)+" (1)")
            import exceptionRaised
            exceptionRaised.main(i)
            if exceptionRaised.worked is True:
                ancestors = sb.get_ancestor_ids(i)
            elif exceptionRaised.worked is False:
                continue  # eyekeeper make sure this continues on to the next i in possibleProjectData.
            else:
                print('Something went wrong. Function: parse (1)')
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

    findShortcuts(FYprojects, currentProject, exceptionFound,
                  possibleProjectData, projectItems, currentProjectJson,
                  )


def findShortcuts(FYprojects, currentProject, exceptionFound,
                  possibleProjectData, projectItems, currentProjectJson,
                  ):
    #global lookedForShortcutsBefore
    global lookedForDataBefore
    print("Looking for shortcuts in any items...")
    foundShortcutsThisTime = False
    print("Original foundShortcutsThisTime = False")  # Quantico
    print(foundShortcutsThisTime)  # Quantico
#if lookedForShortcutsBefore is False:
#    lookedForShortcutsBefore = True
    for i in projectItems:
        try:
            currentProjectItemJson = sb.get_item(i)
            if currentProjectItemJson['title'] == "Approved DataSets":
                shortcuts = sb.get_shortcut_ids(i)
                print("Shortcuts in Approved DataSets:")  # Quantico
                print(shortcuts)
                if shortcuts == []:
                    #lookedForShortcutsBefore = True
                    print("No shortcuts in \"Approved DataSets\".")
                elif shortcuts != []:
                    #lookedForShortcutsBefore = True
                    foundShortcutsThisTime = True
                    print("Place 1: foundShortcutsThisTime = True")  # Quantico
                    print(foundShortcutsThisTime)  # Quantico
                    for i in shortcuts:
                        if i not in possibleProjectData:
                            possibleProjectData.append(i)
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
            exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(i)+" (1)")
            import exceptionRaised
            exceptionRaised.main(i)
            if exceptionRaised.worked is True:
                currentProjectItemJson = sb.get_item(i)
                if currentProjectItemJson['title'] == "Approved DataSets":
                    shortcuts = sb.get_shortcut_ids(i)
                    print("Shortcuts in Approved DataSets:")  # Quantico
                    print(shortcuts)
                    if shortcuts == []:
                        #lookedForShortcutsBefore = True
                        print("No shortcuts in \"Approved DataSets\".")
                    elif shortcuts != []:
                        #lookedForShortcutsBefore = True
                        foundShortcutsThisTime = True
                        print("Place 2: foundShortcutsThisTime = True")  # Quantico
                        print(foundShortcutsThisTime)  # Quantico
                        for i in shortcuts:
                            if i not in possibleProjectData:
                                possibleProjectData.append(i)
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
            elif exceptionRaised.worked is False:
                continue
            else:
                print('Something went wrong. Function: findShortcuts (1.1)')

#elif lookedForShortcutsBefore is True:
#    pass #something should happen here. eyekeeper
#    else:
#        print("Something went wrong. Current function: findShortcuts (2)")
#        exit()
    allShortcuts = []
    allShortcuts[:] = []
    for i in possibleProjectData:
        try:
            preShortcuts = sb.get_shortcut_ids(i)
            print("preShortcuts: ")
            print(preShortcuts)  # Quantico
            for item in preShortcuts:
                if item not in allShortcuts:
                    allShortcuts.append(item)
        except Exception:
            exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(i)+" (1)")
            import exceptionRaised
            exceptionRaised.main(i)
            if exceptionRaised.worked is True:
                preShortcuts = sb.get_shortcut_ids(i)
                for item in preShortcuts:
                    if item not in allShortcuts:
                        allShortcuts.append(item)
            elif exceptionRaised.worked is False:
                continue
            else:
                print('Something went wrong. Function: findShortcuts (2.2)')
    print("All shortcuts:")  # Quantico
    print(allShortcuts)  # Quantico
    if allShortcuts == []:
        print("No shortcuts in \"Possible Project Data\".")
    elif allShortcuts != []:
        foundShortcutsThisTime = True
        print("Place 3: foundShortcutsThisTime = True")  # Quantico
        print(foundShortcutsThisTime)  # Quantico
        for i in allShortcuts:
            if i not in possibleProjectData:
                foundShortcutsThisTime = True
                print("Place 4: foundShortcutsThisTime = True")  # Quantico
                print(foundShortcutsThisTime)  # Quantico
                possibleProjectData.append(i)
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
        getProjectData(possibleProjectData, FYprojects, currentProject, exceptionFound,
                           )
    elif foundShortcutsThisTime is False:
        print("-------- Didn't find any Shortcuts this time!") # Quantico

        import countData_proj
        countData_proj.main(possibleProjectData)

        if exceptionFound is False:
            print('''
            I am done looking through the \''''+str(currentProjectJson['title']) +
                  '''' project folder.''')
            global projectDictNumber
            projectDictNumber += 1
            whatNext(FYprojects, exceptionFound)
        elif exceptionFound is True:
            diagnostics(FYprojects, exceptionFound, currentProjectJson)
    else:
        print('Something went wrong. Current function: findShortcuts (4)')







def diagnostics(FYprojects, exceptionFound, currentProjectJson):
    print("There appear to have been exceptions raised during the parsing "+
          "process. Here is the list of IDs for items that raised exceptions "+
          "that were not solved:")
    print(g.Exceptions)
    print('''

    I am done looking through the \''''+str(currentProjectJson['title']) +
          '''' project folder.''')
    # eyekeeper come back to this and add an option to try the exception raising items again.
    global projectDictNumber
    projectDictNumber += 1
    whatNext(FYprojects, exceptionFound)


def whatNext(FYprojects, exceptionFound):
    global doubleCheck
    printAllGLists()
    if doubleCheck is True:
        print("Continue? (Y / N)")
        answer = input("> ").lower()
    elif doubleCheck is False:
        answer = 'y'
    else:
        print('Something is wrong. Current function: whatNext()')
        exit()
    global firstFYParse
    global FYdictNum
    global projectDictNumber
    #global lookedForShortcutsBefore
    global lookedForDataBefore
    if 'y' in answer:
        if projectDictNumber >= len(FYprojects):
            print("You have finished one Fiscal Year. No more available Projects.")
            import countData_proj
            countData_proj.doneCountingFY()
            excel()
            firstFYParse = True
            FYdictNum += 1
            #lookedForShortcutsBefore = False
            lookedForDataBefore = False
            g.totalFYData = 0
            main()
        elif projectDictNumber < len(FYprojects):
            print("Ok, let\'s start on project "+str(projectDictNumber+1) +
                  " of "+str(len(FYprojects))+".")
            #lookedForShortcutsBefore = False
            lookedForDataBefore = False

            main()
    elif 'n' in answer or 'N' in answer:
        print('Goodbye')
        exit()
    else:
        print("Please type an 'N' or 'Y'.")
        whatNext(FYprojects, exceptionFound)

def excel():
    print("""
    Would you like to create an Excel Spreadsheet with all parsed data """+
    """currently in memory before continuing on? If you choose no, all """+
    """information gathered will continue to be compiled and will be """+
    """available to be included in a final spreadsheet at the end of """+
    """the process or to be used to create a speadsheet after each """+
    """subsequent Fiscal Year, Project, or Item that was originally """+
    """selected to be parsed is parsed.

    (Y / N)""")
    answer = input("> ").lower()
    if "y" in answer:
        import ExcelPrint
        import editGPY
        ExcelPrint.main()
        editGPY.clearMemory()
    elif 'n' in answer:
        print("No spreadsheet created.")


if __name__ == '__main__':
    g.itemsToBeParsed.append("5006c2c9e4b0abf7ce733f42")
    # g.itemsToBeParsed.append("5006e94ee4b0abf7ce733f56")
    # g.itemsToBeParsed.append("55130c4fe4b02e76d75c0755")
    # g.itemsToBeParsed.append("55e07a67e4b0f42e3d040f3c")
    # g.itemsToBeParsed.append("58111fafe4b0f497e79892f7")
    # g.itemsToBeParsed.append("57daef3fe4b090824ffc3226")
    main()
