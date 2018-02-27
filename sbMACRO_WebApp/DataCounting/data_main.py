"""This module is for creating the json database of ScienceBase items."""

import os
import json
import jsonpickle  # pylint: disable=E0401
import datetime
import pysb  # pylint: disable=wrong-import-order
import gl  # pylint: disable=C0413

SB = pysb.SbSession()

def get_fiscal_years(csc_id=None):
    """Create a sorted dict of fiscal years from NWCSC and return it.

    Arguments:
        csc_id -- the sciencebase id to be parsed (default None)

    Returns:
       fiscal_years_dict_ordered -- ordered dict of ScienceBase fiscal year ids

    Raises:
        ValueError: if no argument passed to csc_id

    """
    if csc_id is None:
        print("No id passed to get_fiscal_years")
        raise ValueError
    csc_json = SB.get_item(csc_id)
    csc_title = csc_json['title']
    if "Northwest" in csc_title:
        csc_title = csc_title.replace("Northwest ", "NW")
    elif "Southwest" in csc_title:
        csc_title = csc_title.replace("Southwest ", "SW")
    try:
        fiscal_years = SB.get_child_ids(csc_id)
    except Exception:  # pylint: disable=W0703  # pylint: disable=W0703
        print("----------Exception Raised in get_fiscal_years (1)")
        fiscal_years = gl.exception_loop(csc_id, ".get_child_ids")
        # fiscal_years = SB.get_child_ids(csc_id)
    fiscal_years_dict = {}
    for sb_id in fiscal_years:
        try:
            json_ = SB.get_item(sb_id)
        except Exception:  # pylint: disable=W0703  # pylint: disable=W0703
            print("----------Exception Raised in get_fiscal_years (2)")
            json_ = gl.exception_loop(sb_id, ".get_item")
            # json_ = SB.get_item(sb_id)
        title = json_['title'].replace(' Projects', '')
        fiscal_years_dict.update({title: sb_id})
    if __debug__:
        print("Original fiscal_years_dict")
        print(fiscal_years_dict)
    sorted_dict = sorted(fiscal_years_dict)
    fiscal_years_dict_ordered = {}
    fiscal_years_dict_ordered['csc'] = csc_title
    fiscal_years_dict_ordered['years'] = {}
    for i in sorted_dict:
        fiscal_years_dict_ordered['years'].update({i: fiscal_years_dict[i]})
    if __debug__:
        print("Newly Ordered fiscal_years_dict: fiscal_years_dict_ordered")
        print(fiscal_years_dict_ordered)
    return fiscal_years_dict_ordered


def defined_hard_search():
    """Perform hard search on specific fiscal years via user-input.

    The function first prompts the user for a ScienceBase id.
    Then, once done, the ids are placed into gl.items_to_be_parsed, and
    parse.main() is called to begin the hard search. This ends with new jsons
    being created and saved for whatever fiscal years were designated.
    """
    # To run this function from command line:
    # python -c 'from data_main import defined_hard_search; defined_hard_search()'

    answer = None
    fy_id_list = []
    while answer != 'done':
        print('Please enter an Fiscal Year ID you would like parsed. '
              + 'When done, type \'done\'.')
        if not fy_id_list:  # if fy_obj_list is empty (false)
            pass
        else:
            print("Currently in line:")
            print("------------------")
            for i in fy_id_list:
                print("{0} -- {1}".format(i.ID, i.csc))
            print("------------------")
        answer = input('sbID: ').lower()
        if answer == "test":
            fy_id_list = generate_test()
            break
        obj = sb_fy_id(None, None)
        obj.ID = answer
        if ((answer != 'done')
                and (answer != None)
                and (not id_in_list(fy_id_list, obj))
                and (len(answer) == 24)):  # ID string length is 24
            print("Id not invalid...")
            csc = None
            while(csc != "NWCSC"
                    and csc != "SWCSC"
                    and csc != 'UNKNOWN'):
                if csc == "NWCSC":
                    print("csc = NWCSC")
                if csc == "SWCSC":
                    print("csc = SWCSC")
                if csc == "UNKNOWN":
                    print("csc = UNKNOWN")
                print("Please enter the CSC for the given ID, " 
                        + "or type 'unknown'.")
                csc = input('SB CSC: ').upper()
                print("Input: {0}".format(csc))
                if csc == 'UNKNOWN':
                    csc = get_csc_from_fy_id(answer)
                    if csc == False:
                        continue
            obj.csc = csc
            fy_id_list.append(obj)
    
    fy_obj_list = create_fy_objs(fy_id_list)
    
    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    check_for_recency(fy_obj_list)
    if fy_obj_list:
        for fiscal_year in fy_obj_list:
            if __debug__:
                print("""
            Starting {0} ({1})
            CSC: {2}
            ===================================================================
                """.format(fiscal_year.name, fiscal_year.ID, fiscal_year.csc))
            try:
                project_ids = SB.get_child_ids(fiscal_year.ID)
            except Exception:  # pylint: disable=W0703
                project_ids = gl.exception_loop(fiscal_year.ID, 
                                                ".get_child_ids")
            if __debug__:
                print("project_ids: \n{0}".format(project_ids))
            project_obj_list = create_proj_objs(project_ids, fiscal_year)
            print(project_obj_list)
            for project in project_obj_list:
                if __debug__:
                    print("""
                Starting Project: 
                {0} 
                ID: {1}
                CSC: {2}
                Fiscal Year: {3}
                ---------------------------------------------------------------
                    """.format(project.name, project.ID, project.csc, 
                               project.fiscal_year))
                try:
                    project_child_ids = SB.get_child_ids(project.ID)
                except Exception:  # pylint: disable=W0703
                    project_child_ids = gl.exception_loop(project.ID, 
                                                          ".get_child_ids")
                    # project_child_ids = SB.get_child_ids(project.ID)
                approved_datasets = get_approved_datasets(project_child_ids)
                try:
                    proj_ancestors = SB.get_ancestor_ids(
                                                approved_datasets['id'])
                except Exception:  # pylint: disable=W0703
                    proj_ancestors = gl.exception_loop(approved_datasets['id'],
                                                       ".get_ancestor_ids")
                project_items = find_all_items(project, 
                                               fiscal_year, 
                                               proj_ancestors,
                                               approved_datasets['id'])
                for item in project_items:
                    if __debug__:
                        print("Adding item...")
                    project.project_items["Project_Item_List"].append(item)
                    project.project_items["Project_Item_Count"] += 1
                    project.data_in_project += item.size/1000000  
                    #                                    ^ bytes to megabytes
                    project.project_files["Project_File_Count"] += \
                                                                item.num_files
                    project.project_files["Project_File_List"].extend(
                                                               item.file_list)
                #==============================================================
                if __debug__:
                    print("""
                ---------------------------------------------------------------
                |   Project size (in megabytes):                              |
                |   {0} mb                                                    |
                ---------------------------------------------------------------
                           """.format(project.data_in_project))
                    # item.size is in bytes, we want megabites,
                    # so divide by 1,000,000
                fiscal_year.projects.append(project)
                fiscal_year.total_fy_data += project.data_in_project
            if __debug__:
                print("""
==============================================================================
||   Fiscal Year size (in megabytes):\t\t\t\t\t||
||   {0} mb\t\t\t\t\t\t\t||
==============================================================================
                      """.format(fiscal_year.total_fy_data))
            if __debug__:
                print("Saving Fiscal Year...")
            save_json(fiscal_year)


def generate_test():
    """Generate test-case Fiscal Years for unit testing.
    
    The fiscal years chosen for testing are NWCSC 2012 and 2014 and SWCSC
    2012 and 2014.
    """
    fy_id_list = []
    obj = sb_fy_id("5006c2c9e4b0abf7ce733f42", "NWCSC")
    fy_id_list.append(obj)  # NWCSC 2012
    obj = sb_fy_id("531899cce4b051b1b924ea01", "NWCSC")
    fy_id_list.append(obj)  # NWCSC 2014
    obj = sb_fy_id("5007050de4b0abf7ce733fda", "SWCSC")
    fy_id_list.append(obj)  # SWCSC 2012
    obj = sb_fy_id("531dd8c3e4b04cb293ee78ee", "SWCSC")
    fy_id_list.append(obj)  # SWCSC 2014
    return fy_id_list


class sb_fy_id(object):
    """Object for keeping track of the CSC for a given Fiscal Year."""

    def __init__(self, sb_id, csc):
        """Init function for sb_fy_id.

        Arguments:
            sb_id -- (string) the Science Base ID for a fiscal year.
            csc -- (string) A string of the format [char][char]CSC, eg. NWCSC
        Returns:
            An sb_fy_id object.
        """
        self.ID = sb_id
        self.csc = csc


def debug_parse_projects():
    """For debugging/testing, find all items and calculate project size.

    The function can be given a fiscal year ID and CSC, or use a 'dummy' 
    default (SWCSC FY 2011) if not important. It will then parse the project
    and its items as it normally would and print the results.
    """
    # To run this from the terminal, use the following:
    # python -c 'from data_main import debug_parse_projects; debug_parse_projects()'

    project_ID = '1'
    while len(project_ID) is not 24:
        print("Please provide a Science Base Project ID.")
        project_ID = input("Project ID: ")
    print("Provide a fiscal year ID and CSC, or use Dummy Fiscal Year?")
    preference = input("> ").lower()
    if "dum" in preference:
        # Dummy Fiscal Year:
        fiscal_year = gl.sb_fiscal_year("50070504e4b0abf7ce733fd7", "SWCSC")
    else:
        fy_id = input("Fiscal Year ID: ")
        fy_csc = input("CSC: ")
        fiscal_year = gl.sb_fiscal_year(fy_id, fy_csc)
    
    project = gl.sb_project(project_ID, fiscal_year)
    if __debug__:
        print("""
    Starting Project: 
    {0} 
    ID: {1}
    CSC: {2}
    Fiscal Year: {3}
    ---------------------------------------------------------------
        """.format(project.name, project.ID, project.csc,
                    project.fiscal_year))
    try:
        project_child_ids = SB.get_child_ids(project.ID)
    except Exception:  # pylint: disable=W0703
        project_child_ids = gl.exception_loop(project.ID,
                                                ".get_child_ids")
        # project_child_ids = SB.get_child_ids(project.ID)
    approved_datasets = get_approved_datasets(project_child_ids)
    try:
        proj_ancestors = SB.get_ancestor_ids(
            approved_datasets['id'])
    except Exception:  # pylint: disable=W0703
        proj_ancestors = gl.exception_loop(approved_datasets['id'],
                                            ".get_ancestor_ids")
    project_items = find_all_items(project,
                                    fiscal_year,
                                    proj_ancestors,
                                    approved_datasets['id'])
    for item in project_items:
        if __debug__:
            print("Adding item...")
        project.project_items["Project_Item_List"].append(item)
        project.project_items["Project_Item_Count"] += 1
        project.data_in_project += item.size/1000000
    #==============================================================
    if __debug__:
        print("""
    ---------------------------------------------------------------
    |   Project size (in megabytes):                              |
    |   {0} mb                                                    |
    ---------------------------------------------------------------
                """.format(project.data_in_project))
    print("\n\nAnother? (Y / N)")
    answer = input("> ").lower()
    if 'y' in answer:
        debug_parse_projects()
    elif 'n' in answer:
        exit(0)
    else:
        print("Neither answer selected. Program ended.")


def full_hard_search():
    """Perform hard search on any ids older than 1 day.

    The function calls get_fiscal_years on all desired CSCs to get ordered
    dictionaries of each CSC's fiscal years. All fiscal year IDs are added to
    the fy_obj_list list. Then, it  parses the appropriate fiscal year's
    json file (if it exists) to see if any of those fiscal years have been
    hard search that day. If so, it removes them from the list. The list is
    used to populate gl.items_to_be_parsed before calling parse.main(). This
    ends with new jsons being created and saved for whatever fiscal years were
    designated.
    """
    # To run this function from command line:
    # python -c 'from data_main import full_hard_search; full_hard_search()'

    try:
        nwcsc_fiscal_years = SB.get_child_ids("4f8c64d2e4b0546c0c397b46")
    except Exception:  # pylint: disable=W0703  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (1)")
        nwcsc_fiscal_years = gl.exception_loop("4f8c64d2e4b0546c0c397b46", 
                                               ".get_child_ids")
        # nwcsc_fiscal_years = SB.get_child_ids("4f8c64d2e4b0546c0c397b46")
    try:
        swcsc_fiscal_years = SB.get_child_ids("4f8c6580e4b0546c0c397b4e")
    except Exception:  # pylint: disable=W0703  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        swcsc_fiscal_years = gl.exception_loop("4f8c6580e4b0546c0c397b4e", 
                                               ".get_child_ids")
        # swcsc_fiscal_years = SB.get_child_ids("4f8c6580e4b0546c0c397b4e")
    sb_fy_id_list = []
    for ID in nwcsc_fiscal_years:
        obj = sb_fy_id(ID, "NWCSC")
        sb_fy_id_list.append(obj)
    for ID in swcsc_fiscal_years:
        obj = sb_fy_id(ID, "SWCSC")
        sb_fy_id_list.append(obj)

    fy_obj_list = create_fy_objs(sb_fy_id_list)
    
    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    check_for_recency(fy_obj_list)
    if fy_obj_list:
        for fiscal_year in fy_obj_list:
            if not fiscal_year:
                assert False, "FOUND NULL FISCAL YEAR."
            if __debug__:
                print("""
            Starting {0} ({1})
            CSC: {2}
            ===================================================================
                """.format(fiscal_year.name, fiscal_year.ID, fiscal_year.csc))
            try:
                project_ids = SB.get_child_ids(fiscal_year.ID)
            except Exception:  # pylint: disable=W0703
                project_ids = gl.exception_loop(fiscal_year.ID, 
                                                ".get_child_ids")
            if __debug__:
                print("project_ids: \n{0}".format(project_ids))
            project_obj_list = create_proj_objs(project_ids, fiscal_year)
            print(project_obj_list)
            for project in project_obj_list:
                if __debug__:
                    print("""
                Starting Project: 
                {0} 
                ID: {1}
                CSC: {2}
                Fiscal Year: {3}
                ---------------------------------------------------------------
                    """.format(project.name, project.ID, project.csc, 
                               project.fiscal_year))
                try:
                    project_child_ids = SB.get_child_ids(project.ID)
                except Exception:  # pylint: disable=W0703
                    project_child_ids = gl.exception_loop(project.ID, 
                                                          ".get_child_ids")
                    # project_child_ids = SB.get_child_ids(project.ID)
                approved_datasets = get_approved_datasets(project_child_ids)
                try:
                    proj_ancestors = SB.get_ancestor_ids(
                                                approved_datasets['id'])
                except Exception:  # pylint: disable=W0703
                    proj_ancestors = gl.exception_loop(approved_datasets['id'],
                                                       ".get_ancestor_ids")
                project_items = find_all_items(project, 
                                               fiscal_year, 
                                               proj_ancestors,
                                               approved_datasets['id'])
                for item in project_items:
                    if __debug__:
                        print("Adding item...")
                    project.project_items["Project_Item_List"].append(item)
                    project.project_items["Project_Item_Count"] += 1
                    project.data_in_project += item.size/1000000  
                #==============================================================
                if __debug__:
                    print("""
                ---------------------------------------------------------------
                |   Project size (in megabytes):                              |
                |   {0} mb                                                    |
                ---------------------------------------------------------------
                           """.format(project.data_in_project))
                    # item.size is in bytes, we want megabites,
                    # so divide by 1,000,000
                fiscal_year.projects.append(project)
                fiscal_year.total_fy_data += project.data_in_project
            if __debug__:
                print("""
==============================================================================
||   {0} size (in megabytes):\t\t\t\t\t||
||   {1} mb\t\t\t\t\t\t\t||
==============================================================================
                      """.format(fiscal_year.name, fiscal_year.total_fy_data))
            if __debug__:
                print("Saving Fiscal Year...")
            save_json(fiscal_year)
            if __debug__:
                print("fy_obj_list before NULLing {0}:\n{1}"
                      .format(fiscal_year, fy_obj_list))
            fiscal_year = None
            if __debug__:
                print("fy_obj_list after NULLing {0}:\n{1}"
                      .format(fiscal_year, fy_obj_list))
            continue
    if not fy_obj_list:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    print("WHY AM I HERE???")
    assert False, "Should never get here!!!!"


def get_csc_from_fy_id(sb_id):
    """Find and return the corresponding CSC using Fiscal Year ID.

    Arguments:
        sb_id -- (string) the sciencebase id for a Fiscal Year

    Returns:
        name -- (string) the name of the CSC of the form __CSC (eg. "NWCSC")
        False -- (boolean) If a legal CSC is not found or there was no parent 
                  to sb_id, the boolean False is returned.

    """
    try:
        fy_json = SB.get_item(sb_id)
    except Exception:  # pylint: disable=W0703
        fy_json = gl.exception_loop(sb_id, ".get_item")
    parent_id = fy_json['parentId']
    if parent_id:
        try:
            parent_json = SB.get_item(parent_id)
        except Exception:  # pylint: disable=W0703
            parent_json = gl.exception_loop(parent_id, ".get_item")
        name = parent_json['title']
        if 'Southwest' in name:
            name = name.replace('Southwest ', 'SW')
            return name
        elif 'Northwest' in name:
            name = name.replace('Northwest ', 'NW')
            return name
        else:
            return False
    else:
        assert False, "No parent id"




def create_fy_objs(id_list):
    """Return a list populated with fiscal year objects created using id_list.

    For each of the SB IDs in id_list, fiscal year objects are created using 
    the sb_fiscal_year class. Each of those objects is appended to the 
    fy_obj_list, which is finally returned.

    Arguments:
        id_list -- (list) A list of sb_fy_id objects to be made into 
                    sb_fiscal_year objects.

    Returns:
       fy_obj_list -- (list) a list of fiscal year objects made using the 
                      sb_fiscal_year class

    """
    fy_obj_list = []
    for i in id_list:
        obj = gl.sb_fiscal_year(i.ID, i.csc)
        obj.date = get_date()
        fy_obj_list.append(obj)
        if __debug__:
            print("{0} {1}: {2} fy object created and added to fy_obj_list."
                  .format(obj.csc, obj.name, obj.ID))
    return fy_obj_list


def create_proj_objs(project_ids, fiscal_year):
    """Return a list populated with project objects created using project_ids.

    For each of the SB IDs in project_ids, project objects are created using 
    the sb_project class and the current fiscal year object. If "Project" is 
    in the "browseCategories" of the project json, it is appended to the 
    proj_obj_list. If not a project, it is skipped. The ID of each project 
    object that is added to the proj_obj_list is tracked to make sure projects 
    are not created in duplicate. proj_obj_list is finally returned.

    Arguments:
        project_ids -- (list) A list of strings that are each an SB ID 
                        representing a project found within the current fiscal 
                        year.
        fiscal_year -- (sb_fiscal_year) the current fiscal year object

    Returns:
       proj_obj_list -- (list) a list of project objects made using the 
                        sb_project class

    """
    fy_projects = []
    proj_obj_list = []
    for project in project_ids:
        if __debug__:
            print("Creating project object for {0}".format(project))
        obj = gl.sb_project(project, fiscal_year)
        project_json = obj.sb_json
        try:
            if "Project" in project_json["browseCategories"] \
                    and project not in fy_projects:
                if __debug__:
                    print("--Item is a project.")
                fy_projects.append(project)
                proj_obj_list.append(obj)
            elif "Project" in project_json["browseCategories"] \
                    and project in fy_projects:
                if __debug__:
                    print("--Item already parsed.")
        except KeyError:
            assert False, ("--{0} not a project. This should be looked into..."
                          .format(project))
            print("Back to finding projects...")
            continue
    # for project in proj_obj_list:
    #     project.Print()
    return proj_obj_list


def get_approved_datasets(project_child_ids):
    """Return for the 'Approved Datasets" folder within a project.

    Take every child item in project_child_ids and get its json. If that 
    json's title is "Approved DataSets, return that json. If we don't find 
    approved datasets, assert and exit with -1. 

    Arguments:
        project_child_ids -- (list) A list of strings that are each an SB ID 
                        representing a child of the current project.

    Returns:
       approved_datasets -- (json) a Science Base json for the Approved 
                            DataSets folder within the current project.

    """
    for item in project_child_ids:
        try:
            item_json = SB.get_item(item)
        except Exception:  # pylint: disable=W0703
            item_json = gl.exception_loop(item, ".get_item")
        if item_json['title'] == "Approved DataSets":
            approved_datasets = item_json
            return approved_datasets
        else:
            continue
    assert approved_datasets, "Approved Datasets was not found"
    exit(-1)


def find_all_items(project, fiscal_year, proj_ancestors, approved_datasets):
    """Return a list of sb_item objects representing all items in a project.

    For every Science Base ID found in the proj_ancestors list, 
    """
    project_items = []
    project_items_ids = []
    for sb_id in proj_ancestors:
        if sb_id not in project_items_ids:
            project_items_ids.append(sb_id)
    all_items = find_shortcuts(project_items_ids, approved_datasets)
    for item in all_items:
        item_obj = gl.sb_item(item)
        if not id_in_list(project_items, item_obj):
            project_items.append(item_obj)
    if __debug__:
        print(
        """Found these items in find_all_items:
        {0}""".format(project_items))
    return project_items
    # project_items = find_shortcuts(project_items, )


class item_id(object):
    def __init__(self, sb_id):
        self.ID = sb_id
        self.shortcut_checked = False
        self.ancestor_checked = False
    
    def Print(self):
        print("""
        Item temp object:
        {0}
        -----------------
        Checked for shortcuts:\t\t{1}
        Checked for descendents:\t{2}
            """.format(self.ID, self.shortcut_checked, self.ancestor_checked))

def find_shortcuts(project_items_ids, approved_datasets):
    item_temp_obj_list = []
    for sb_id in project_items_ids:
        obj = item_id(sb_id)
        obj.ancestor_checked = True
        item_temp_obj_list.append(obj)
    try:
        approved_datasets_shortcuts = SB.get_shortcut_ids(approved_datasets)
    except Exception:  # pylint: disable=W0703
        approved_datasets_shortcuts = gl.exception_loop(approved_datasets, 
                                                        ".get_shortcut_ids")
    if approved_datasets_shortcuts:
        if __debug__:
            print("FOUND shortcuts in Approved Datasets:")
            print(approved_datasets_shortcuts)
        for sb_id in approved_datasets_shortcuts:
            obj = item_id(sb_id)
            item_temp_obj_list.append(obj)
    item_ids = shortcut_loop(item_temp_obj_list)
    if __debug__:
        print(
        """Found these item_ids in find_shortcuts:
        {0}""".format(item_ids))
    return item_ids


def shortcut_loop(obj_list):
    if __debug__:
        print("In shortcut_loop...\n\n")
    for obj in obj_list:
        obj.Print()
        if obj.shortcut_checked is False:
            if __debug__:
                print("{0} not checked for shortcuts".format(obj.ID))
            try:
                shortcuts = SB.get_shortcut_ids(obj.ID)
            except Exception:  # pylint: disable=W0703
                shortcuts = gl.exception_loop(obj.ID, ".get_shortcut_ids")
            if shortcuts:
                for sb_id in shortcuts:
                    new_obj = item_id(sb_id)
                    if not id_in_list(obj_list, new_obj):
                        obj_list.append(new_obj)
            obj.shortcut_checked = True
            if __debug__:
                print("{0} has now been checked for shortcuts".format(obj.ID))
                if shortcuts:
                    print("----- Shortcuts found")
                else:
                    print("----- Shortcuts NOT found")
        if obj.ancestor_checked is False:
            if __debug__:
                print("{0} not checked for descendents".format(obj.ID))
            try:
                descendents = SB.get_ancestor_ids(obj.ID)
            except Exception:  # pylint: disable=W0703
                descendents = gl.exception_loop(obj.ID, ".get_ancestor_ids")
            if descendents:
                for sb_id in descendents:
                    new_obj = item_id(sb_id)
                    if not id_in_list(obj_list, new_obj):
                        obj_list.append(new_obj)
                        if __debug__:
                            print("---{0} added to obj_list".format(sb_id))
            obj.ancestor_checked = True
            if __debug__:
                print("{0} has now been checked for descendents"
                      .format(obj.ID))
                if descendents:
                    print("----- Descendents found:")
                    print(descendents)
                else:
                    print("----- Descendents NOT found")
    if shortcut_loop_control(obj_list):
        item_id_list = []
        for obj in obj_list:
            if obj.ID not in item_id_list:
                item_id_list.append(obj.ID)
        if __debug__:
            print(
            """Found these item ids in shortcut_loop:
            {0}""".format(item_id_list))
        return item_id_list
    else:
        if __debug__:
            print("Found shortcuts in shortcut_loop. Looping...")
        shortcut_loop(obj_list)


def shortcut_loop_control(obj_list):
    for obj in obj_list:
        if not obj.shortcut_checked:
            if __debug__:
                print("{0} not shorcut_checked in loop_control".format(obj.ID))
            return False
        if not obj.ancestor_checked:
            if __debug__:
                print("{0} not ancestor_checked in loop_control"
                      .format(obj.ID))
            return False
    if __debug__:
        print("Did not find any items not checked in loop_control.")
        print("Ending loop...")
    return True


def id_in_list(obj_list, sb_object):
    if __debug__:
        print("Checking if sb_object in list...")
    for sb_objects in obj_list:
        if sb_object.ID == sb_objects.ID:
            if __debug__:
                print("Object in list.")
            return True
    if __debug__:
        print("Object not in list")
    return False


def get_date():
    from datetime import datetime
    dateinfo = {}
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    return date


def check_for_recency(fy_obj_list):
    if __debug__:
        print("Checking recency...")
    ids_to_be_deleted = []
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                           os.pardir))
    fiscal_year_json_folder = os.path.join(app_dir, "jsonCache/")
    for the_file in os.listdir(fiscal_year_json_folder):
        file_path = os.path.join(fiscal_year_json_folder, the_file)
        try:
            if os.path.isfile(file_path):
                if file_path.endswith(".json"):
                    with open(file_path) as json_data:
                        data = json.load(json_data)
                        try:  # If date doesn't exist replace it.
                            data_date = data['date']
                        except KeyError:
                            print("Couldn't find date. This could be an"
                                  + " error.")
                            continue
                        now = datetime.datetime.now()
                        current_date = now.strftime("%Y%m%d")

                        if current_date > data_date:
                            if __debug__:
                                print("---- {0} is not recent"
                                      .format(data['ID']))
                                print("     {0} will be done"
                                      .format(data['ID']))
                            continue
                        else:
                            if __debug__:
                                print("---- {0} is recent:".format(data['ID']))
                            # uncomment 'continue' below if you want to do all 
                            # FYs regardless of when they were last done:
                            continue
                            if __debug__:
                                print("     {0} will be skipped"
                                      .format(data['ID']))
                            fy_id = the_file.replace(".json", "")
                            print("fy_id from today: {0}".format(fy_id))
                            # Quantico
                            ids_to_be_deleted.append(fy_id)
            else:
                print("Not a json file")
        except Exception as err:  # pylint: disable=W0703
            print("Exception: " + err)
    for fy_id in ids_to_be_deleted:
        while fy_id in fy_obj_list:
            fy_obj_list.remove(fy_id)
    return


class JsonTransformer(object):
    def transform(self, myObject):
        return jsonpickle.encode(myObject, unpicklable=False)


def save_json(fiscal_year):
    if __debug__:
        print("Saving {0} ({1}) as a json..."
              .format(fiscal_year.name, fiscal_year.ID))
    full_report_json = JsonTransformer()
    full_report_json = JsonTransformer.transform(full_report_json, fiscal_year)
    app_dir = os.path.abspath(os.path.join(
                              os.path.dirname(__file__), os.pardir))
    if __debug__:
        print("Directory in which app resides: {0}".format(app_dir))
    with open('{0}/jsonCache/{1}.json'.format(app_dir, fiscal_year.ID), 
              'w') as outfile:
        outfile.write(full_report_json)
    print("finished full_report_json:")

    return


if __name__ == "__main__":
    full_hard_search()
