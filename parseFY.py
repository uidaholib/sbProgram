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
exceptionFound = False
lookedForShortcutsBefore = False
lookedForDataBefore = False
FYprojects = []


firstFYParse = True
FYdictNum = 0

def main():
    possibleProjectData[:] = []
    print("parseFY.py main") # Quantico
    global firstFYParse
    global FYprojects
    global projectDictNumber
    if firstFYParse is True:
        projectDictNumber = 0
        getProjects()
        firstFYParse = False
    print(FYprojects)  # Quantico
    # projectDictNumber = 11  # Quantico
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
                   lookedForShortcutsBefore, lookedForDataBefore)

def getProjects():
    possibleProjectData[:] = []
    global FYprojects
    FYprojects[:] = []
    global FYdictNum
    try:
        i = g.fiscalYears[FYdictNum]
    except IndexError:
        print("No more fiscal years.")
        FYprojects[:] = []
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
                   lookedForShortcutsBefore, lookedForDataBefore):
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
          lookedForShortcutsBefore, lookedForDataBefore, currentProjectJson)


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


def findCurrentProjectFY(currentProject, currentProjectJson):
    currentId = currentProject[:]
    json = currentProjectJson
    parentId = currentProjectJson["parentId"]
    children = sb.get_child_ids(currentId)
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
            children = sb.get_child_ids(currentId)
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
          lookedForShortcutsBefore, lookedForDataBefore, currentProjectJson):
    possibleProjectData_Set = set()
    for i in possibleProjectData:
        possibleProjectData_Set.update(possibleProjectData)
        try:
            ancestors = sb.get_ancestor_ids(i)
        except Exception:
            if i not in g.Exceptions:
                g.Exceptions.append(i)
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

    findShortcuts(FYprojects, currentProject, exceptionFound,
                  possibleProjectData, projectItems, currentProjectJson,
                  lookedForShortcutsBefore, lookedForDataBefore)


def findShortcuts(FYprojects, currentProject, exceptionFound,
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
                if i not in g.Exceptions:
                    g.Exceptions.append(i)
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
            if i not in g.Exceptions:
                g.Exceptions.append(i)
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
        getProjectData(possibleProjectData, FYprojects, currentProject, exceptionFound,
                           lookedForShortcutsBefore, lookedForDataBefore)
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
    print("There appear to have been exceptions raised for the following items:")
    print(g.Exceptions)
    print('''

    I am done looking through the \''''+str(currentProjectJson['title']) +
          '''' project folder.''')
    # eyekeeper come back to this and add an option to try the exception raising items again.
    global projectDictNumber
    projectDictNumber += 1
    whatNext(FYprojects, exceptionFound)


def whatNext(FYprojects, exceptionFound):
    print("Continue? (Y / N)")
    answer = input("> ").lower()
    global firstFYParse
    global FYdictNum
    global projectDictNumber
    if 'y' in answer:
        if projectDictNumber >= len(FYprojects):
            print("You have finished one Fiscal Year. No more available Projects.")
            import countData_proj
            countData_proj.doneCountingFY()
            firstFYParse = True
            FYdictNum += 1
            lookedForShortcutsBefore = False
            lookedForDataBefore = False
            totalFYData = 0
            main()
        elif projectDictNumber < len(FYprojects):
            print("Ok, let\'s start on project "+str(projectDictNumber+1) +
                  " of "+str(len(FYprojects))+".")
            lookedForShortcutsBefore = False
            lookedForDataBefore = False

            main()
    elif 'n' in answer or 'N' in answer:
        print('Goodbye')
        exit()
    else:
        print("Please type an 'N' or 'Y'.")
        whatNext(FYprojects, exceptionFound)


if __name__ == '__main__':
    g.itemsToBeParsed.append("5006c2c9e4b0abf7ce733f42")
    # g.itemsToBeParsed.append("5006e94ee4b0abf7ce733f56")
    # g.itemsToBeParsed.append("55130c4fe4b02e76d75c0755")
    # g.itemsToBeParsed.append("55e07a67e4b0f42e3d040f3c")
    # g.itemsToBeParsed.append("58111fafe4b0f497e79892f7")
    # g.itemsToBeParsed.append("57daef3fe4b090824ffc3226")
    main()
