"""Functions related to Science Base Projects."""
import time
import sciencebasepy
from app.updater import gl
from app.updater import main


SB = sciencebasepy.SbSession()


def parse_project(project):
    """Parse files and items for provided project.

    Use the provided project, find all the items and files in that project
    and add them together as objects in a multi-level project object that will
    be incorporated into the current fiscal year object.

    Arguments:
        project -- (SbProject) an object containing to which will be added
                   all items and files found within the Approved DataSets
                   folder of the project.

    Raises:
        Exception -- If Approved Datasets folder was not found but was
                     expected.

    """
    if __debug__:
        print("""
                Starting Project:
                {0}
                ID: {1}
                CSC: {2}
                Fiscal Year: {3}
                ---------------------------------------------------------------
        """.format(project.name.encode('utf-8'), project.ID.encode('utf-8'), project.csc.encode('utf-8'), project.fiscal_year.encode('utf-8')))
    try:
        project_child_ids = SB.get_child_ids(project.ID)
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        project_child_ids = gl.exception_loop(project.ID,
                                              ".get_child_ids")
    approved_datasets = get_approved_datasets(project_child_ids)
    if approved_datasets is None and project.ID == "559afce2e4b0b94a64016ffe":
        return
    elif approved_datasets is None:
        raise Exception("Approved Datasets not found in {0}"
                        .format(project.ID))
    try:
        proj_ancestors = SB.get_ancestor_ids(
            approved_datasets['id'])
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        proj_ancestors = gl.exception_loop(approved_datasets['id'],
                                           ".get_ancestor_ids")
    project_items = find_all_items(proj_ancestors,
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
    return


def get_approved_datasets(project_child_ids):  # pylint: disable=R1710
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
            time.sleep(.050)  # Possibly for use to combat exceptions
        except Exception:  # pylint: disable=W0703
            item_json = gl.exception_loop(item, ".get_item")
            if item_json is None:
                raise TypeError
        if item_json['title'] == "Approved DataSets":
            approved_datasets = item_json
            return approved_datasets
        else:
            continue
    return None


class item_id(object):  # pylint: disable=C0103,R0903
    """
    Class to track if an ID has been checked for shortcuts and descendents.

    The boolean values of shortcut_checked and ancestor_checked are changed to
    True once the Science Base ID has been checked using SB.get_shortcut_ids()
    and SB.get_ancestor_ids() respectively.
    """

    def __init__(self, sb_id):
        """Create an item_id object.

        Arguments:
            sb_id -- (string) the ID of a Science Base item.

        Returns:
            A item_id object.

        """
        self.ID = sb_id  # pylint: disable=C0103
        self.shortcut_checked = False
        self.ancestor_checked = False

    def Print(self):  # pylint: disable=C0103
        """Print the contents of an item_id object to the standard output."""
        print("""
        Item temp object:
        {0}
        -----------------
        Checked for shortcuts:\t\t{1}
        Checked for descendents:\t{2}
            """.format(self.ID, self.shortcut_checked, self.ancestor_checked))


def find_shortcuts(project_items_ids, approved_datasets):
    """
    Return all possible items within the project's 'Approved DataSets' folder.

    This is the caller of a recursively looping function set designed to find
    all shortcuted items and non-shortcut items within the approved datasets
    folder of the current project and return a list of the Science Base IDs
    for those items.

    First, the function creates an item_id object out of each ID in the
    incoming project_items_ids list and marks those at ancestor_checked (as
    they were checked inherently do to being recieved from
    SB.get_ancestor_ids()). Those objects are appended to item_temp_obj_list.

    Then, approved_datasets is checked for shortcuts. If found, item_id
    objects are created from the IDs and they are added to the
    item_temp_obj_list.

    shortcut_loop() is then called to finish gathering the Science Base items
    that have not yet been found. The list returned from that function
    contains all item IDs in the project's Approved DataSet folder. That list
    is returned.

    Arguments:
        project_items_ids -- (list) a list of the IDs (strings) recieved from
                             SB.get_ancestor_ids() called on approved_datasets.
        approved_datasets -- (string) the Science Base ID for the Approved
                             DataSets folder of the current project.

    Returns:
        item_ids -- (list) A list of strings that represent every Science Base
                    item found within the Approved DataSet folder of the
                    current project.

    """
    item_temp_obj_list = []
    for sb_id in project_items_ids:
        obj = item_id(sb_id)
        obj.ancestor_checked = True
        item_temp_obj_list.append(obj)
    try:
        approved_datasets_shortcuts = SB.get_shortcut_ids(approved_datasets)
        time.sleep(.050)  # Possibly for use to combat exceptions
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
        print("""
        Found these item_ids in find_shortcuts:
        {0}""".format(item_ids))
    return item_ids


def shortcut_loop(obj_list):  # pylint: disable=R1710
    """Recursively find all shortcuted items and descendents.

    For every object passed in within obj_list:
    First, see if it has been checked for shortcuts. If not, check it, mark it
    as checked, and create objects out of any IDs found. Check of those IDs
    are already in obj_list, if not, add append them.

    Second, see if it has been checked for descendents. If not, check it, mark
    it as checked, and create objects out of any IDs found. Mark those new
    objects as ancestor_checked = True. Check of those IDs are already in
    obj_list, if not, add append them.

    If shortcut_loop() returns true, then loop through obj_list, appending
    each obj.ID to a list and return that list which now contains all items in
    the project.

    If shortcut_loop() returns false, then call shortcut_loop() (itself).

    Arguments:
        obj_list -- (list) a list of item_id objects.

    Returns:
        item_id_list -- (list) a list of the IDs (as strings) for every item
                        found in the project.

    """
    if __debug__:
        print("In shortcut_loop...\n\n")
    for obj in obj_list:
        obj.Print()
        if obj.shortcut_checked is False:
            check_shortcuts(obj, obj_list)
        if obj.ancestor_checked is False:
            check_descendents(obj, obj_list)
    if shortcut_loop_control(obj_list):
        item_id_list = []
        for obj in obj_list:
            if obj.ID not in item_id_list:
                item_id_list.append(obj.ID)
        if __debug__:
            print("""
            Found these item ids in shortcut_loop:
            {0}""".format(item_id_list))
        return item_id_list
    else:
        if __debug__:
            print("Found shortcuts in shortcut_loop. Looping...")
        shortcut_loop(obj_list)


def check_descendents(obj, obj_list):
    """Check obj for descendents, create objects from any new IDs.

    Check obj for any descendents, mark it as checked, and create objects out
    of any IDs found. Check of those IDs are already in obj_list, if not
    append them.

    Arguments:
        obj -- (item_id) the item to be checked for descendents.
        obj_list (list) the list of all item_id objects found in the current
                 project.

    """
    if __debug__:
        print("{0} not checked for descendents".format(obj.ID))
    try:
        descendents = SB.get_ancestor_ids(obj.ID)
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        descendents = gl.exception_loop(obj.ID, ".get_ancestor_ids")
    if descendents:
        for sb_id in descendents:
            new_obj = item_id(sb_id)
            # Mark any descendents as ancestor_checked, as
            # SB.get_ancestor_ids() inherently gets all descendents
            # from every item it finds:
            new_obj.ancestor_checked = True
            if not main.id_in_list(obj_list, new_obj):
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


def check_shortcuts(obj, obj_list):
    """Check obj for shortcuts, create objects from any new IDs.

    Check obj for any shortcuts, mark it as checked, and create objects out of
    any IDs found. Check of those IDs are already in obj_list, if not, append
    them.

    Arguments:
        obj -- (item_id) the item to be checked for shortcuts.
        obj_list (list) the list of all item_id objects found in the current
                 project.

    """
    if __debug__:
        print("{0} not checked for shortcuts".format(obj.ID))
    try:
        shortcuts = SB.get_shortcut_ids(obj.ID)
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        shortcuts = gl.exception_loop(obj.ID, ".get_shortcut_ids")
    if shortcuts:
        for sb_id in shortcuts:
            new_obj = item_id(sb_id)
            if not main.id_in_list(obj_list, new_obj):
                obj_list.append(new_obj)
    obj.shortcut_checked = True
    if __debug__:
        print("{0} has now been checked for shortcuts".format(obj.ID))
        if shortcuts:
            print("----- Shortcuts found")
        else:
            print("----- Shortcuts NOT found")


def shortcut_loop_control(obj_list):
    """Return whether or not every object in the list has been checked.

    Return True if all objects in list have been checked for shortcuts and
    descendents. Otherwise, return False as soon as one is found that hasn't
    been checked for either.

    Arguments:
        obj_list -- (list) a list of item_id objects.

    Returns:
        True -- (boolean) Returned if no object was found with False as a
                value for .shortcut_checked or .ancestor_checked.
        False -- (boolean) Returned if any object was found with False as a
                 value for .shortcut_checked or .ancestor_checked.

    """
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


def find_all_items(proj_ancestors, approved_datasets):
    """Return a list of SbItem objects representing all items in a project.

    Firstly, the proj_ancestors list (containing the IDs of all descendents of
    the 'Approved DataSets' item) is converted to a set in order to not allow
    duplicate items to be counted in the project. Then, find_shortcuts() is
    called on the set and approved_datasets to initiate the recursive loop to
    find all possible items within the project's 'Approved DataSets' folder.
    The list of IDs returned from that function is iterated through, creating
    an item object (using the SbItem class) and adding it to the
    project_items list, which is then returned.

    Arguments:
        proj_ancestors -- (list) a list of Science Base ID strings
                          representing all descendents of the Approved
                          DataSets folder for the current project.
        approved_datasets -- (string) the ScienceBase ID for the Approved
                             Datasets folder.
    Returns:
        project_items -- (list) a list of SbItem objects representing all
                         items found within the Approved DataSets folder of
                         the current project.

    """
    # We don't want any repeats of items, so we use a set()...
    proj_ancestors_set = set(proj_ancestors)
    project_items = []
    all_items = find_shortcuts(proj_ancestors_set, approved_datasets)
    for item in all_items:
        item_obj = gl.SbItem(item)
        if not main.id_in_list(project_items, item_obj):
            project_items.append(item_obj)
    if __debug__:
        print("""
        Found these items in find_all_items:
        {0}""".format(project_items))
    return project_items


def create_proj_objs(project_ids, fiscal_year):
    """Return a list populated with project objects created using project_ids.

    For each of the SB IDs in project_ids, project objects are created using
    the SbProject class and the current fiscal year object. If "Project" is
    in the "browseCategories" of the project json, it is appended to the
    proj_obj_list. If not a project, it is skipped. The ID of each project
    object that is added to the proj_obj_list is tracked to make sure projects
    are not created in duplicate. proj_obj_list is finally returned

    Arguments:
        project_ids -- (list) A list of strings that are each an SB ID
                        representing a project found within the current fiscal
                        year.
        fiscal_year -- (SbFiscalYear) the current fiscal year object.

    Returns:
       proj_obj_list -- (list) a list of project objects made using the
                        SbProject class.

    """
    fy_projects = []
    proj_obj_list = []
    for project in project_ids:
        if __debug__:
            print("Creating project object for {0}".format(project))
        obj = gl.SbProject(project, fiscal_year)
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
