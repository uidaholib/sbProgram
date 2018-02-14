"""Find all items in each fiscal year.

This module takes a list of fiscal years and finds the items within them
and sends those items to countData_proj.py to be counted.
"""

import sys
import os
import pysb  # pylint: disable=wrong-import-order

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "DataCounting/"))
import gl, parse  # pylint: disable=E0401,C0413,C0410,C0411


sb = pysb.SbSession()



def main(fiscal_year_id):
    fiscal_year = gl.sb_fiscal_year(fiscal_year_id)
    fiscal_year.Print()
    total_data_count = 0
    project_index_number = 0
    project_items[:] = []
    exception_found = False
    looked_for_shortcuts_before = False
    looked_for_data_before = False
    fy_projects = []
    first_fy_parse = True
    very_first_fy_parse = True
    project_items = getProjects()

# def main(fiscalYear):
#     resetGlobals()
#     gl.Current_Item = fiscalYear
#     global project_items
#     project_items[:] = []
#     print("parseFY.py main") # Quantico
#     select_project(fiscalYear)

def exceptionLoop(item):
    import exceptionRaised
    exceptionRaised.main(item)
    if exceptionRaised.worked is True:
        return
    elif exceptionRaised.worked is False:
        exceptionLoop(item)

def select_project(fiscalYear):
    global project_items
    project_items[:] = []
    global first_fy_parse
    global fy_projects
    global project_index_number
    global very_first_fy_parse
    if first_fy_parse is True:
        project_index_number = 0
        getProjects(fiscalYear)
        first_fy_parse = False
    # if project_index_number == -99999999999999:
    #     return
    print(fy_projects)  # Quantico
    print("Project dict number: "+str(project_index_number))  # Quantico
    try:
        currentProject = fy_projects[project_index_number]
    except IndexError:
        return
    print("currentProject: "+str(currentProject))  # Quantico
    getProjectData(project_items, fy_projects,
                   currentProject, exception_found,
                   )

def resetGlobals():
    global total_data_count
    total_data_count = 0
    global project_index_number
    project_index_number = 0
    global project_items
    project_items[:] = []
    global exception_found
    exception_found = False
    global looked_for_shortcuts_before
    looked_for_shortcuts_before = False
    global looked_for_data_before
    looked_for_data_before = False
    global fy_projects
    fy_projects[:] = []
    global first_fy_parse
    first_fy_parse = True
    global very_first_fy_parse
    very_first_fy_parse = True


def getProjects(fiscalYear):
    global project_items
    global project_index_number
    project_items[:] = []
    global fy_projects
    fy_projects[:] = []
    print(fiscalYear)
    try:
        currentFYprojects = sb.get_child_ids(fiscalYear)
    except Exception:
        exception_found = True
        exceptionLoop(fiscalYear)
        currentFYprojects = sb.get_child_ids(fiscalYear)
    print(currentFYprojects)  # Quantico
    for project in currentFYprojects:
        projectJson = sb.get_item(project)
        try:
            if "Project" in projectJson["browseCategories"] and project not in fy_projects:
                print("--Item is a project.")
                fy_projects.append(project)
            elif "Project" in projectJson["browseCategories"] and project in fy_projects:
                print("--Item already parsed.")
            else:
                print("browseCategories = "+str(projectJson["browseCategories"]))
        except KeyError:
            print("--"+str(project)+" not a project.")
            print("Quickly parsing "+str(project)+" to determine what it "
                  + "is...")
            print("======================================================")
            gl.on_the_fly_parsing.append(project)
            parse.parseOnTheFly()
            print("Back to finding projects...")
            main(fiscalYear)
    return fy_projects



def getProjectData(project_items, fy_projects,
                   currentProject, exception_found,
                   ):
    global looked_for_data_before
    projectItems = sb.get_child_ids(currentProject)
    try:
        currentProjectJson = sb.get_item(currentProject)
    except Exception:
        exception_found = True
        exceptionLoop(currentProject)
        currentProjectJson = sb.get_item(currentProject)

        # Old exception handling:
        # print("--------Hit upon a 404 exception: " +
        #       str(currentProject) + " (1)")
        # import exceptionRaised
        # exceptionRaised.main(currentProject)
        # if exceptionRaised.worked is True:
        #    currentProjectJson = sb.get_item(currentProject)
        # elif exceptionRaised.worked is False:
        #     getProjectData(project_items, fy_projects,
        #                    currentProject, exception_found,
        #                    )
        # else:
        #     print('Something went wrong. Function: getProjectData (1)')
    if looked_for_data_before is False:
        populateGPYLists(currentProject, currentProjectJson)
        print("""

        Currently searching '"""+str(currentProjectJson['title'])+"'.")
        # flash("""

        # Currently searching '"""+str(currentProjectJson['title'])+"'.")
        looked_for_data_before = True
        for i in projectItems:
            try:
                currentProjectItemJson = sb.get_item(i)
            except Exception:
                exception_found = True
                exceptionLoop(i)
                currentProjectItemJson = sb.get_item(i)
            print(currentProjectItemJson['title'])
            if currentProjectItemJson['title'] == "Approved DataSets":
                possibleProjectData_Set = set()
                possibleProjectData_Set.update(project_items)
                try:
                    ancestors = sb.get_ancestor_ids(i)
                except Exception:
                    exception_found = True
                    print("--------Hit upon a 404 exception: " + str(i) + " (22)")
                    exceptionLoop(i)
                    ancestors = sb.get_ancestor_ids(i)
                    # Old exception handling:
                    # import exceptionRaised
                    # exceptionRaised.main(i)
                    # if exceptionRaised.worked is True:
                    #     children = sb.get_child_ids(currentId)
                    # elif exceptionRaised.worked is False:
                    #     gl.exceptions.append(i)
                    #     print("-----------ERROR: Could not get project data.")
                    #     continue
                    # else:
                    #     print('Something went wrong. Function: getProjectData() (2)')
                for item in ancestors:
                    if item not in possibleProjectData_Set:
                        possibleProjectData_Set.add(item)
                        project_items.append(item)
                    else:
                        pass
                print('First look at Possible Project Data:')
                print(project_items)
                print('Total Items:')
                print(len(project_items))
            else:
                pass
    parse_data(project_items, fy_projects, projectItems,
          currentProject, exception_found,
          currentProjectJson)


def populateGPYLists(currentProject, currentProjectJson):
    gl.ID.append(currentProject)
    print(gl.ID)  # Quantico
    gl.URL.append(sb.get_item(currentProject)['link']['url'])
    print(gl.URL)
    gl.object_type.append("Project")
    print(gl.object_type)  # Quantico
    gl.name.append(currentProjectJson["title"])
    print(gl.name)  # Quantico
    findCurrentProjectFY(currentProject, currentProjectJson)
    print(gl.fiscal_year)  # Quantico
    gl.project.append("Self")
    print(gl.project)  # Quantico
    return

def printAllGLists():
    print(gl.ID)  # Quantico
    print(gl.URL)
    print(gl.object_type)  # Quantico
    print(gl.name)  # Quantico
    print(gl.fiscal_year)  # Quantico
    print(gl.project)  # Quantico
    print(gl.data_in_project)  # Quantico
    print(len(gl.data_per_file)) # Quantico
    print(gl.running_data_total)  # Quantico

def findCurrentProjectFY(currentProject, currentProjectJson):
    currentId = currentProject[:]
    json = currentProjectJson
    parentId = currentProjectJson["parentId"]
    try:
        children = sb.get_child_ids(currentId)
    except Exception:
        exception_found = True
        print("--------Hit upon a 404 exception: "+str(currentId)+" (1)")
        exceptionLoop(currentId)
        children = sb.get_child_ids(currentId)

        # import exceptionRaised
        # exceptionRaised.main(i)
        # if exceptionRaised.worked is True:
        #     children = sb.get_child_ids(currentId)
        # elif exceptionRaised.worked is False:
        #     FY = "Exception Raised: Could not find Fiscal Year"
        #     print("Exception Raised: Could not find Fiscal Year.")
        #     gl.fiscal_year.append(FY)
        #     return
        # else:
        #     print('Something went wrong. Function: findCurrentProjectFY() (2.2)')
    try:
        child = children[0]
    except (KeyError, IndexError) as error:
        print("No children of the current item.")
        currentId = parentId[:]  # this makes a slice that is the whole list.
        json = sb.get_item(currentId)
        parentId = json['parentId']
        children = sb.get_child_ids(currentId)
        child = children[0]
    try:
        childJson = sb.get_item(child)
    except Exception:
        exception_found = True
        print("--------Hit upon a 404 exception: " + str(child) + " (1)")
        exceptionLoop(child)
        childJson = sb.get_item(child)
    if 'FY' in json['title']:
        print("Item is a Fiscal Year")  # Quantico
        gl.fiscalYears.append(json['title'])
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
            try:
                json = sb.get_item(currentId)
            except Exception:
                exception_found = True
                print("--------Hit upon a 404 exception: " + str(currentId) + " (2)")
                exceptionLoop(currentId)
                json = sb.get_item(currentId)


            
            parentId = json['parentId']
            try:
                children = sb.get_child_ids(currentId)
            except Exception:
                exception_found = True
                print("--------Hit upon a 404 exception: "+str(currentId)+" (1)")
                exceptionLoop(currentId)
                children = sb.get_child_ids(currentId)
                # import exceptionRaised
                # exceptionRaised.main(currentId)
                # if exceptionRaised.worked is True:
                #     children = sb.get_child_ids(currentId)
                # elif exceptionRaised.worked is False:
                #     continue
                # else:
                #     print('Something went wrong. Function: findCurrentProjectFY (1)')
            child = children[0]
            try:
                childJson = sb.get_item(child)
            except Exception:
                exception_found = True
                print("--------Hit upon a 404 exception: " + str(child) + " (1)")
                exceptionLoop(child)
                childJson = sb.get_item(child)
                # import exceptionRaised
                # exceptionRaised.main(child)
                # if exceptionRaised.worked is True:
                #     hildJson = sb.get_item(child)
                # elif exceptionRaised.worked is False:
                #     continue
                # else:
                #     print('Something went wrong. Function: parse_data (1)')

            print("Not a Fiscal Year.")
            continue
        if 'Project' in childJson['browseCategories']:
            control = False
    FY = json['title'].replace(" Projects", "")
    print("appending \'"+str(json['title'])+'\' as '+str(FY))  # Quantico
    gl.fiscal_year.append(FY)
    return

    #do a "while" loop here. Something like, while the children of the current thing are NOT projects...
    #and when they are, take the ['title'] and append that to gl.fiscal_year and return

def parse_data(project_items, fy_projects, projectItems,
          currentProject, exception_found,
          currentProjectJson):
    possibleProjectData_Set = set()
    for i in project_items:
        possibleProjectData_Set.update(project_items)
        try:
            ancestors = sb.get_ancestor_ids(i)
        except Exception:
            exception_found = True
            print("--------Hit upon a 404 exception: "+str(i)+" (1)")
            exceptionLoop(i)
            ancestors = sb.get_ancestor_ids(i)
            # import exceptionRaised
            # exceptionRaised.main(i)
            # if exceptionRaised.worked is True:
            #     ancestors = sb.get_ancestor_ids(i)
            # elif exceptionRaised.worked is False:
            #     continue  # eyekeeper make sure this continues on to the next i in project_items.
            # else:
            #     print('Something went wrong. Function: parse_data (1)')
        for item in ancestors:
            if item not in possibleProjectData_Set:
                possibleProjectData_Set.add(item)
                project_items.append(item)
            elif item in possibleProjectData_Set:
                pass
            else:
                print("Something went wrong. Current function: "
                      + "getProjectData (1)")
    print('Double checked Possible Project Data:')
    print(project_items)
    print('Total Items:')
    print(len(project_items))

    findShortcuts(fy_projects, currentProject, exception_found,
                  project_items, projectItems, currentProjectJson,
                  )


def findShortcuts(fy_projects, currentProject, exception_found,
                  project_items, projectItems, currentProjectJson,
                  ):
    global looked_for_shortcuts_before
    global looked_for_data_before
    print("Looking for shortcuts in any items...")
    foundShortcutsThisTime = False
    if looked_for_shortcuts_before is False:
        looked_for_shortcuts_before = True
        for i in projectItems:
            try:
                currentProjectItemJson = sb.get_item(i)
            except Exception:
                exception_found = True
                print("--------Hit upon a 404 exception: " + str(i) + " (1)")
                exceptionLoop(i)
                currentProjectItemJson = sb.get_item(i)
            if currentProjectItemJson['title'] == "Approved DataSets":
                try:
                    shortcuts = sb.get_shortcut_ids(i)
                except Exception:
                    exception_found = True
                    print("--------Hit upon a 404 exception: " + str(i) + " (1)")
                    exceptionLoop(i)
                    shortcuts = sb.get_shortcut_ids(i)
                print("Shortcuts in Approved DataSets:")  # Quantico
                print(shortcuts)
                if shortcuts == []:
                    looked_for_shortcuts_before = True
                    print("No shortcuts in \"Approved DataSets\".")
                elif shortcuts != []:
                    looked_for_shortcuts_before = True
                    foundShortcutsThisTime = True
                    for i in shortcuts:
                        if i not in project_items:
                            project_items.append(i)
                    print("We found some shortcuts and added them to the " +
                            "Possible Project Data:")
                    print(shortcuts)
                    print('Total Items added:')
                    print(len(shortcuts))
                    print("New Possible Project Data:")
                    print(project_items)
                    print("Current Item total:")
                    print(len(project_items))
                else:
                    print("Something went wrong. Current function: "
                            + "findShortcuts (1)")
                    exit()
            else:
                pass
                # elif exceptionRaised.worked is False:
                #     continue
                # else:
                #     print('Something went wrong. Function: findShortcuts (1.1)')

    elif looked_for_shortcuts_before is True:
        pass #something should happen here. eyekeeper
    else:
        print("Something went wrong. Current function: findShortcuts (2)")
        exit()
    allShortcuts = []
    allShortcuts[:] = []
    for i in project_items:
        try:
            preShortcuts = sb.get_shortcut_ids(i)
        except Exception:
            exception_found = True
            print("--------Hit upon a 404 exception: " + str(i) + " (1)")
            exceptionLoop(i)
            preShortcuts = sb.get_shortcut_ids(i)
            # import exceptionRaised
            # exceptionRaised.main(i)
            # if exceptionRaised.worked is True:
            #     preShortcuts = sb.get_shortcut_ids(i)
            #     for item in preShortcuts:
            #         if item not in allShortcuts:
            #             allShortcuts.append(item)
            # elif exceptionRaised.worked is False:
            #     continue
            # else:
            #     print('Something went wrong. Function: findShortcuts (2.2)')
            # print("preShortcuts: ")  # Quantico
            # print(preShortcuts)  # Quantico
        for item in preShortcuts:
            if item not in allShortcuts:
                allShortcuts.append(item)
        
    print("All shortcuts:")  # Quantico
    print(allShortcuts)  # Quantico
    if allShortcuts == []:
        print("No shortcuts in \"Possible Project Data\".")
    elif allShortcuts != []:
        #foundShortcutsThisTime = True
        for i in allShortcuts:
            if i not in project_items:
                foundShortcutsThisTime = True
                project_items.append(i)
        print("We found some shortcuts and added them to the Possible Project "
              + "Data:")
        print(project_items)
        print('Total Items:')
        print(len(project_items))
    else:
        print("Something went wrong. Current function: findShortcuts (3)")
        exit()

    if foundShortcutsThisTime is True:
        print("-------- Found shortcuts this time!")
        getProjectData(project_items, fy_projects, currentProject, exception_found,
                           )
    elif foundShortcutsThisTime is False:
        print("-------- Didn't find any Shortcuts this time!") # Quantico

        import countData_proj
        countData_proj.main(currentProject, project_items)
        print("gl.project_files: (2)")
        print(gl.project_files)
        #Now we collect all Project file info in ProjectFileDict:
        # gl.ProjFileDict[currentProject] = {}
        # currProj = gl.ProjFileDict[currentProject]
        # currProj['Num_Of_Files'] = gl.NumOfFiles
        # currProj['Project_Files'] = gl.project_files
        print("""=================================================================
                Here is projFiles as it currently stands: """)
        print(gl.project_files)

        print("""=================================================================
                Here is projItems as it currently stands: """)
        print(gl.project_items)

        if exception_found is False:
            print('''
            I am done looking through the \''''+str(currentProjectJson['title']) +
                  '''' project folder.''')
            global project_index_number
            # flash("Total Data in Project: ")
            # flash(gl.data_in_project[project_index_number])
            # flash("Running Total of Data thus far: ")
            # flash(gl.running_data_total[project_index_number])
            project_index_number += 1
            whatNext(fy_projects, exception_found)

        elif exception_found is True:
            diagnostics(fy_projects, exception_found, currentProjectJson)
    else:
        print('Something went wrong. Current function: findShortcuts (4)')







def diagnostics(fy_projects, exception_found, currentProjectJson):
    print("There appear to have been exceptions raised during the parsing "+
          "process. Here is the list of IDs for items that raised exceptions "+
          "that were not solved:")
    print(gl.exceptions)
    print('''

    I am done looking through the \''''+str(currentProjectJson['title']) +
          '''' project folder.''')
    global project_index_number
    # flash("Total Data in Project: ")
    # flash(gl.data_in_project[project_index_number])
    # flash("Running Total of Data thus far: ")
    # flash(gl.running_data_total[project_index_number])
    # eyekeeper come back to this and add an option to try the exception raising items again.

    project_index_number += 1
    whatNext(fy_projects, exception_found)


def whatNext(fy_projects, exception_found):
    printAllGLists()
    global first_fy_parse
    global project_index_number
    global looked_for_shortcuts_before
    global looked_for_data_before
    if project_index_number >= len(fy_projects):
        print("You have finished one Fiscal Year. No more available Projects.")
        # flash("You have finished one Fiscal Year. No more available Projects.")
        # flash("""
        # ---------------------------------------------------------------------------------------
        # """)
        import countData_proj
        countData_proj.doneCountingFY()
        # excel()
        first_fy_parse = True
        looked_for_shortcuts_before = False
        looked_for_data_before = False
        gl.totalFYData = 0
        return
    elif project_index_number < len(fy_projects):
        print("Ok, let\'s start on project "+str(project_index_number+1) +
              " of "+str(len(fy_projects))+".")
        # flash("Ok, let\'s start on project "+str(project_index_number+1) +
        #       " of "+str(len(fy_projects))+".")
        # flash("""
        # ---------------------------------------------------------------------------------------
        # """)
        looked_for_shortcuts_before = False
        looked_for_data_before = False
        select_project(gl.Current_Item)




if __name__ == '__main__':
    # gl.itemsToBeParsed.append("5006c2c9e4b0abf7ce733f42")
    # gl.itemsToBeParsed.append("5006e94ee4b0abf7ce733f56")
    # gl.itemsToBeParsed.append("55130c4fe4b02e76d75c0755")
    # gl.itemsToBeParsed.append("55e07a67e4b0f42e3d040f3c")
    # gl.itemsToBeParsed.append("58111fafe4b0f497e79892f7")
    # gl.itemsToBeParsed.append("57daef3fe4b090824ffc3226")
    # main(fiscalYear)
    print("Set __name__ = '__main__' to something...")
