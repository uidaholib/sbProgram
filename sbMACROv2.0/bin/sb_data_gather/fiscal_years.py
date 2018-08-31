"""Functions related to Science Base Fiscal Years."""
import os
import json
from datetime import datetime
import gl
import pysb
import main
import projects
import time

SB = pysb.SbSession()


def get_fiscal_years(csc_id=None):
    """Create a sorted dict of fiscal years from a CSC and return it.

    Use csc_id to create a dictionary with the names and Science Base IDs of
    each fiscal year that exists within the given CSC. Sort that dictionary,
    include the CSC name in the dictionary, and return it.

    Arguments:
        csc_id -- (string) the Science Base ID of a Climate Science Center
                  folder (default: None)

    Returns:
       fiscal_years_dict_ordered -- (dictionary) ordered dictionary containing
       the names and IDs of the fiscal years within the provided CSC, and the
       CSC name.

    Raises:
        ValueError: if no argument passed to csc_id OR if the CSC title is not
                    recognized.

    """
    if csc_id is None:
        print("No id passed to get_fiscal_years")
        raise ValueError("CSC ID is 'None' in get_fiscal_years()")
    csc_json = SB.get_item(csc_id)
    time.sleep(.050)  # Possibly for use to combat exceptions
    csc_title = csc_json['title']
    if "Northwest" in csc_title:
        csc_title = csc_title.replace("Northwest ", "NW")
    elif "Southwest" in csc_title:
        csc_title = csc_title.replace("Southwest ", "SW")
    else:
        raise ValueError("Error: \n"
                         + "Unrecognized Fiscal Year title in "
                         + "get_fiscal_years()")
    try:
        fiscal_years = SB.get_child_ids(csc_id)
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in get_fiscal_years (1)")
        fiscal_years = gl.exception_loop(csc_id, ".get_child_ids")
    fiscal_years_dict = {}
    for sb_id in fiscal_years:
        try:
            json_ = SB.get_item(sb_id)
            time.sleep(.050)  # Possibly for use to combat exceptions
        except Exception:  # pylint: disable=W0703
            print("----------Exception Raised in get_fiscal_years (2)")
            json_ = gl.exception_loop(sb_id, ".get_item")
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


class sb_fy_id(object):  # pylint: disable=C0103,R0903
    """Object for keeping track of the CSC for a given Fiscal Year."""

    def __init__(self, sb_id, csc):
        """Init function for sb_fy_id.

        Arguments:
            sb_id -- (string) the Science Base ID for a fiscal year.
            csc -- (string) A string of the format [char][char]CSC, eg. NWCSC
        Returns:
            An sb_fy_id object.
        """
        self.ID = sb_id  # pylint: disable=C0103
        self.csc = csc


def parse_fiscal_years(app, fy_obj_list):
    """Parse projects and items for list of fiscal years.

    Use fy_obj_list to get a fiscal year, find all the projects in that fiscal
    year and all the items and files in that project and add them together as
    objects in a multi-level fiscal year object.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fy_obj_list -- (list) A list of SbFiscalYear objects to be parsed.

    Returns:
        fy_obj_list -- (list) A list of SbFiscalYear objects to be parsed if
                       not done correctly already, OR None if done correctly.
        None -- (boolean) Returned if it appears the fiscal years were parsed
                correctly.
    
    Raises:
        Exception -- if fy_obj_list iteration does not return properly.

    """
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
                time.sleep(.050)  # Possibly for use to combat exceptions
            except Exception:  # pylint: disable=W0703
                project_ids = gl.exception_loop(fiscal_year.ID,
                                                ".get_child_ids")
            if __debug__:
                print("project_ids: \n{0}".format(project_ids))
            project_obj_list = projects.create_proj_objs(project_ids,
                                                         fiscal_year)
            print(project_obj_list)
            for project in project_obj_list:
                projects.parse_project(project)
                fiscal_year.projects.append(project)
                fiscal_year.total_fy_data += project.data_in_project
            if __debug__:
                print("""
==============================================================================
||   {0} size (in megabytes):\t\t\t\t\t||
||   {1} mb\t\t\t\t\t\t\t||
==============================================================================
                      """.format(fiscal_year.name, fiscal_year.total_fy_data))
            main.save_to_db(app, fiscal_year)
            if __debug__:
                print("Saved Fiscal Year.")
                print("fy_obj_list before NULLing {0}:\n{1}"
                      .format(fiscal_year, fy_obj_list))
            index_of_fy = fy_obj_list.index(fiscal_year)
            fy_obj_list[index_of_fy] = None
            fiscal_year = None
            if __debug__:
                print("fy_obj_list after NULLing {0}:\n{1}"
                      .format(fiscal_year, fy_obj_list))
            continue
        for obj in fy_obj_list:
            if obj is not None:
                return fy_obj_list
        return None
    raise Exception("Should not reach here: fiscal_years.parse_fiscal_years()")
    # return fy_obj_list


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


def get_all_cscs():
    """Get fiscal year IDs and return their SbFiscalYear objects as a list.

    Using the legal CSCs, get their fiscal years, tracking their corresponding
    CSCs, and return the SbFiscalYear objects for them as a list that was
    created in create_fy_objs().

    Returns:
        Result of create_fy_objs() -- (list) a list of SbFiscalYear objects

    """
    try:
        alaska_fiscal_years = SB.get_child_ids("4f831626e4b0e84f6086809b")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        alaska_fiscal_years = gl.exception_loop("4f831626e4b0e84f6086809b",
                                                ".get_child_ids")
    try:
        nccwsc_fiscal_years = SB.get_child_ids("5050cb0ee4b0be20bb30eac0")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        nccwsc_fiscal_years = gl.exception_loop("5050cb0ee4b0be20bb30eac0",
                                                ".get_child_ids")
    try:
        nccsc_fiscal_years = SB.get_child_ids("4f83509de4b0e84f60868124")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        nccsc_fiscal_years = gl.exception_loop("4f83509de4b0e84f60868124",
                                               ".get_child_ids")
    try:
        necsc_fiscal_years = SB.get_child_ids("4f8c648de4b0546c0c397b43")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        necsc_fiscal_years = gl.exception_loop("4f8c648de4b0546c0c397b43",
                                               ".get_child_ids")
    try:
        nwcsc_fiscal_years = SB.get_child_ids("4f8c64d2e4b0546c0c397b46")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (1)")
        nwcsc_fiscal_years = gl.exception_loop("4f8c64d2e4b0546c0c397b46",
                                               ".get_child_ids")
    try:
        pacific_fiscal_years = SB.get_child_ids("4f8c650ae4b0546c0c397b48")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (1)")
        pacific_fiscal_years = gl.exception_loop("4f8c650ae4b0546c0c397b48",
                                               ".get_child_ids")
    try:
        sccsc_fiscal_years = SB.get_child_ids("4f8c652fe4b0546c0c397b4a")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        sccsc_fiscal_years = gl.exception_loop("4f8c652fe4b0546c0c397b4a",
                                               ".get_child_ids")
    try:
        secsc_fiscal_years = SB.get_child_ids("4f8c6557e4b0546c0c397b4c")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        secsc_fiscal_years = gl.exception_loop("4f8c6557e4b0546c0c397b4c",
                                               ".get_child_ids")
    try:
        swcsc_fiscal_years = SB.get_child_ids("4f8c6580e4b0546c0c397b4e")
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        swcsc_fiscal_years = gl.exception_loop("4f8c6580e4b0546c0c397b4e",
                                               ".get_child_ids")
    sb_fy_id_list = []
    for sb_id in alaska_fiscal_years:
        obj = sb_fy_id(sb_id, "ALASKACSC")
        sb_fy_id_list.append(obj)
    for sb_id in nccwsc_fiscal_years:
        obj = sb_fy_id(sb_id, "NCCWSC")
        sb_fy_id_list.append(obj)
    for sb_id in nccsc_fiscal_years:
        obj = sb_fy_id(sb_id, "NCCSC")
        sb_fy_id_list.append(obj)
    for sb_id in necsc_fiscal_years:
        obj = sb_fy_id(sb_id, "NECSC")
        sb_fy_id_list.append(obj)
    for sb_id in nwcsc_fiscal_years:
        obj = sb_fy_id(sb_id, "NWCSC")
        sb_fy_id_list.append(obj)
    for sb_id in pacific_fiscal_years:
        if sb_id == "598dac27e4b09fa1cb13ef6a":
            continue
        obj = sb_fy_id(sb_id, "PacificCSC")
        sb_fy_id_list.append(obj)
    for sb_id in sccsc_fiscal_years:
        obj = sb_fy_id(sb_id, "SCCSC")
        sb_fy_id_list.append(obj)
    for sb_id in secsc_fiscal_years:
        if sb_id == "59c56277e4b017cf313d592c":
            continue
        obj = sb_fy_id(sb_id, "SECSC")
        sb_fy_id_list.append(obj)
    for sb_id in swcsc_fiscal_years:
        obj = sb_fy_id(sb_id, "SWCSC")
        sb_fy_id_list.append(obj)

    return create_fy_objs(sb_fy_id_list)


def get_csc_from_fy_id(sb_id, more_data=False):  # pylint: disable=R1710
    """Find and return the corresponding CSC using Fiscal Year ID.

    Arguments:
        sb_id -- (string) the sciencebase id for a Fiscal Year
        more_data -- (boolean, optional) If provided as True, the function
                     finds and returns the CSC's Science Base ID, URL, and
                     unalterned name. Otherwise, the function behaves normally.

    Returns:
        name -- (string) the name of the CSC of the form __CSC (eg. "NWCSC")
        False -- (boolean) If a legal CSC is not found or there was no parent
                  to sb_id, the boolean False is returned.

    Raises:
        ValueError -- if parent_id is None, False, or otherwise illegal.

    """
    try:
        fy_json = SB.get_item(sb_id)
        time.sleep(.050)  # Possibly for use to combat exceptions
    except Exception:  # pylint: disable=W0703
        fy_json = gl.exception_loop(sb_id, ".get_item")
    parent_id = fy_json['parentId']
    if parent_id:
        try:
            parent_json = SB.get_item(parent_id)
            time.sleep(.050)  # Possibly for use to combat exceptions
        except Exception:  # pylint: disable=W0703
            parent_json = gl.exception_loop(parent_id, ".get_item")
        name = parent_json['title']
        if more_data:
            sb_url = parent_json['link']['url']
            return (parent_id, name, sb_url)
        if 'Alaska' in name:
            name = name.replace('Alaska ', 'ALASKA')
        elif 'North Central' in name:
            name = name.replace('North Central ', 'NC')
        elif 'Northeast' in name:
            name = name.replace('Northeast ', 'NE')
        elif 'Northwest' in name:
            name = name.replace('Northwest ', 'NW')
            return name
        elif 'Pacific Islands' in name:
            name = name.replace('Pacific Islands ', 'Pacific')
            return name
        elif 'South Central' in name:
            name = name.replace('South Central ', 'SC')
            return name
        elif 'Southeast' in name:
            name = name.replace('Southeast ', 'SE')
            return name
        elif 'Southwest' in name:
            name = name.replace('Southwest ', 'SW')
            return name

        else:
            return False
    else:
        raise ValueError("No parent id fiscal_years.get_csc_from_fy_id()")


def create_fy_objs(id_list):
    """Return a list populated with fiscal year objects created using id_list.

    For each of the SB IDs in id_list, fiscal year objects are created using
    the SbFiscalYear class. Each of those objects is appended to the
    fy_obj_list, which is finally returned.

    Arguments:
        id_list -- (list) A list of sb_fy_id objects to be made into
                    SbFiscalYear objects.

    Returns:
       fy_obj_list -- (list) a list of fiscal year objects made using the
                      SbFiscalYear class.

    """
    fy_obj_list = []
    for i in id_list:
        obj = gl.SbFiscalYear(i.ID, i.csc)
        obj.date = main.get_date()
        fy_obj_list.append(obj)
        if __debug__:
            print("{0} {1}: {2} fy object created and added to fy_obj_list."
                  .format(obj.csc, obj.name, obj.ID))
    return fy_obj_list


def check_for_recency(app, fy_obj_list):
    """Check current date against each fiscal year json date.

    Iterates through each object in fy_obj_list, checks the current date
    against the date of the json corresponding to that object's Science Base
    ID, and if the current date is more recent it is kept. If not, the object
    is removed from the list.

    NOTE: This function is no longer used in the current algorithm as of Aug.
    10, 2018. It was found to be not useful, but in case it would be in the
    future, it has been left, rather than deleted.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fy_obj_list -- (list) a list of SbFiscalYear objects

    """
    if __debug__:
        print("Checking recency...")
    ids_to_be_deleted = []
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           os.pardir))
    fiscal_year_json_folder = os.path.join(app_dir, "jsonCache/")
    for the_file in os.listdir(fiscal_year_json_folder):
        file_path = os.path.join(fiscal_year_json_folder, the_file)
        try:
            if os.path.isfile(file_path) and file_path.endswith(".json"):
                with open(file_path) as json_data:
                    data = json.load(json_data)
                try:  # If date doesn't exist replace the file.
                    data_date = data['date']
                except KeyError:
                    print("Couldn't find date. This could be an"
                          + " error.")
                    assert False, "Check this error"
                now = datetime.now()
                current_date = now.strftime("%Y%m%d")

                if current_date <= data_date:
                    if __debug__:
                        print("---- {0} is recent:".format(the_file))
                    # uncomment 'continue' below if you want to do all
                    # FYs regardless of when they were last done:
                    continue
                    if __debug__:
                        print("     {0} will be skipped"
                              .format(data['ID']))
                    fy_id = the_file.replace(".json", "")
                    print("fy_id from today: {0}".format(fy_id))
                    ids_to_be_deleted.append(fy_id)
            else:
                print("Not a json file")
        except Exception as err:  # pylint: disable=W0703
            raise Exception("Exception raised when getting filepath to jsons:"
                            + "\n" + err)
    for fy_id in ids_to_be_deleted:
        while fy_id in fy_obj_list:
            fy_obj_list.remove(fy_id)
    return


def get_user_input_fys():
    """Gather Science Base fiscal year IDs and CSCs via user input.

    The function first prompts the user for a Science Base fiscal year ID, and
    then for the CSC of that fiscal year. If 'test' is entered, a test suite
    of fiscal years and CSCs is generated and used. Otherwise, once checked
    for appropriate length and that the ID is not already in the queue, the
    user is asked for the CSC, which is also checked against legal CSC values.
    If 'UNKNOWN' is given, the CSC is found using get_csc_from_fy_id()

    Returns:
        fy_id_list -- (list) A list of sb_fy_id objects containing the IDs and
                      CSCs for the fiscal years given by the user.

    """
    answer = None
    fy_id_list = []
    while answer != 'done':
        print('Please enter an Fiscal Year ID you would like parsed. '
              + 'When finished, type \'done\'.')
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
        elif answer == "598dac27e4b09fa1cb13ef6a" \
              or answer == "59c56277e4b017cf313d592c":
            print("That is not a fiscal year...")
            continue
        obj = sb_fy_id(None, None)
        obj.ID = answer
        if ((answer != 'done')
                and (answer != None)
                and (not main.id_in_list(fy_id_list, obj))
                and (len(answer) == 24)):  # ID string length is 24
            print("ID appears valid...")
            csc = get_csc_from_fy_id(answer)
            obj.csc = csc
            fy_id_list.append(obj)
    return fy_id_list
