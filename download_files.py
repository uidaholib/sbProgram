

import pysb
sb = pysb.SbSession()

def main():
    projectItems = sb.get_ancestor_ids("5006e94ee4b0abf7ce733f56")
    parse(projectDictNumber, projectItems, projects, currentProject, exceptionItems, exceptionFound,
                       lookedForShortcutsBefore, lookedForDataBefore)

def parse(projectDictNumber, projectItems, projects, currentProject, exceptionItems, exceptionFound,
                   lookedForShortcutsBefore, lookedForDataBefore):

    projectItems_Set = set()
    projectItems_Set.update(projectItems)
    for i in projectItems_Set:
        try:
            ancestors = sb.get_ancestor_ids(i)
        except Exception:
            exceptionItems.append(i)
            exceptionFound = True
            print("--------Hit upon a 404 exception: "+str(i)+" (1)")
        for item in ancestors:
            if item not in projectItems_Set:
                projectItems_Set.add(item)
                projectItems.append(item)
            elif item in projectItems_Set:
                pass
            else:
                print("Something went wrong. Current function: "
                      + "getProjectData (1)")
    print('Double checked Possible Project Data:')
    print(projectItems)
    print('Total Items:')
    print(len(projectItems))

    findShortcuts(projects, projectDictNumber, currentProject, exceptionItems, exceptionFound,
                  projectItems, projectItems, currentProjectJson,
                  lookedForShortcutsBefore, lookedForDataBefore)

def findShortcuts(projects, projectDictNumber, currentProject, exceptionItems, exceptionFound,
                  projectItems, projectItems, currentProjectJson,
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
                        projectItems += shortcuts
                        print("We found some shortcuts and added them to the " +
                              "Possible Project Data:")
                        print(shortcuts)
                        print('Total Items added:')
                        print(len(shortcuts))
                        print("New Possible Project Data:")
                        print(projectItems)
                        print("Current Item total:")
                        print(len(projectItems))
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
        pass #something should happen here. eyekeeper
    else:
        print("Something went wrong. Current function: findShortcuts (2)")
        exit()
    allShortcuts = []
    for i in projectItems:
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
        projectItems += allShortcuts
        print("We found some shortcuts and added them to the Possible Project "
              + "Data:")
        print(projectItems)
        print('Total Items:')
        print(len(projectItems))
    else:
        print("Something went wrong. Current function: findShortcuts (3)")
        exit()

    if foundShortcutsThisTime is True:
        print("-------- Found shortcuts this time!")
        getProjectData(projectDictNumber, projectItems, projects, currentProject, exceptionItems, exceptionFound,
                           lookedForShortcutsBefore, lookedForDataBefore)
        # getProjectData(projects, projectDictNumber, currentProject,
        #               projectItems, lookedForShortcutsBefore,
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


# then just get_item('id') for each thing. Then get_item_files_zip(sb_json, destination)


if __name__ == '__main__':
    main()
