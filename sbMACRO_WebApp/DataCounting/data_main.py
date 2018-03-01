"""Main module from which all Science Base data gathering branches."""
import os
from datetime import datetime
import gl
import pysb
import jsonpickle  # pylint: disable=E0401
import fiscal_years
import projects


SB = pysb.SbSession()


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

    fy_obj_list = fiscal_years.get_all_cscs()

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fiscal_years.check_for_recency(fy_obj_list)
    fy_obj_list = fiscal_years.parse_fiscal_years(fy_obj_list)
    if not fy_obj_list:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    print("WHY AM I HERE???")
    assert False, "Should never get here!!!!"
    raise Exception("Something went wrong in full_hard_search()")


def defined_hard_search():
    """Perform hard search on specific fiscal years via user-input.

    This hard search function collects fiscal years from a user that are
    parsed to find projects, which are parsed to find items. All of the above
    are turned into nested objects which are printed as json files to the
    jsonCache directory.

    """
    # To run this function from command line:
# python -c 'from data_main import defined_hard_search; defined_hard_search()'

    fy_id_list = fiscal_years.get_user_input_fys()
    fy_obj_list = fiscal_years.create_fy_objs(fy_id_list)

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fiscal_years.check_for_recency(fy_obj_list)
    fiscal_years.parse_fiscal_years(fy_obj_list)
    return


def debug_projects():
    """For debugging/testing, find all items and calculate project size.

    The function can be given a fiscal year ID and CSC, or use a 'dummy'
    default (SWCSC FY 2011) if not important. It will then parse the project
    and its items as it normally would and print the results.
    """
    # To run this from the terminal, use the following:
# python -c 'from data_main import debug_projects; debug_projects()'

    project_id = '1'
    while len(project_id) != 24:
        print("Please provide a Science Base Project ID.")
        project_id = input("Project ID: ")
    print("Provide a fiscal year ID and CSC, or use Dummy Fiscal Year?")
    preference = input("> ").lower()
    if "dum" in preference:
        # Dummy Fiscal Year:
        fiscal_year = gl.SbFiscalYear("50070504e4b0abf7ce733fd7", "SWCSC")
    else:
        fy_id = input("Fiscal Year ID: ")
        fy_csc = input("CSC: ")
        fiscal_year = gl.SbFiscalYear(fy_id, fy_csc)

    project = gl.SbProject(project_id, fiscal_year)
    projects.parse_project(project)
    print("\n\nAnother? (Y / N)")
    answer = input("> ").lower()
    if 'y' in answer:
        debug_projects()
    elif 'n' in answer:
        exit(0)
    else:
        print("Neither answer selected. Program ended.")


def id_in_list(obj_list, sb_object):
    """Check if an Science Base object exists in a list.

    Arguments:
        obj_list -- (list) a list of objects with an 'ID' attribute.
        sb_object -- (item_id, SbFiscalYear, SbProject, or SbItem)
                     Any item with an '.ID' field.

    Returns:
        True -- (boolean) returned if an item is encountered in obj_list with
                an .ID attribute that matches the .ID attribute of sb_object.
        False -- (boolean) returned if no such item is encountered after
                 iterating through obj_list.

    """
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
    """Return the current date as a string."""
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    return date


class JsonTransformer(object):  # pylint: disable=R0903
    """Class to create save-able, multi-level jsons."""

    def transform(self, my_object):  # pylint: disable=R0201
        """Create save-able, multi-level jsons using jsonpickle.

        Arguments:
            my_object -- (object) The object to be turned into a json.

        Returns:
            json-encoded object.

        """
        return jsonpickle.encode(my_object, unpicklable=False)


def save_json(fiscal_year):
    """Save fiscal year object as json using jsonpickle.

    Arguments:
        fiscal_year -- (SbFiscalYear) fiscal year object to be saved.

    """
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
    print("finished saving full_report_json")

    return


if __name__ == "__main__":
    full_hard_search()
