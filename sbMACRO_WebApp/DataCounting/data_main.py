import sys
import os
from pprint import pprint
import json
import jsonpickle
import datetime
import pysb  # pylint: disable=wrong-import-order

# SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# print(APP_DIR)
# sys.path.insert(0, os.path.join(APP_DIR, "DataCounting2/"))
# print(sys.path[0])
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
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in get_fiscal_years (1)")
        fiscal_years = gl.exception_loop(csc_id, ".get_child_ids")
        # fiscal_years = SB.get_child_ids(csc_id)
    fiscal_years_dict = {}
    for sb_id in fiscal_years:
        try:
            json_ = SB.get_item(sb_id)
        except Exception:  # pylint: disable=W0703
            print("----------Exception Raised in get_fiscal_years (2)")
            json_ = gl.exception_loop(sb_id, ".get_item")
            # json_ = SB.get_item(sb_id)
        title = json_['title'].replace(' Projects', '')
        fiscal_years_dict.update({title: sb_id})
    print("Original fiscal_years_dict")
    print(fiscal_years_dict)
    sorted_dict = sorted(fiscal_years_dict)
    fiscal_years_dict_ordered = {}
    fiscal_years_dict_ordered['csc'] = csc_title
    fiscal_years_dict_ordered['years'] = {}
    for i in sorted_dict:
        fiscal_years_dict_ordered['years'].update({i: fiscal_years_dict[i]})
    print("Newly Ordered fiscal_years_dict: fiscal_years_dict_ordered")
    print(fiscal_years_dict_ordered)
    return fiscal_years_dict_ordered


def defined_hard_search():
    """Perform hard search on specific ids via user-input.

    The function first prompts the user for a ScienceBase id.
    Then, once done, the ids are placed into gl.items_to_be_parsed, and
    parse.main() is called to begin the hard search. This ends with new jsons
    being created and saved for whatever fiscal years were designated.
    """
    # To run this function from command line:
    # python -c 'from app import defined_hard_search; defined_hard_search()'

    gl.Excel_choice = "One_Excel_for_all_FYs"
    answer = None
    fy_obj_list = []
    while answer != 'done':
        print('Please enter an ID you would like parsed. '
              + 'When done, type \'done\'.')
        if not fy_obj_list:  # if fy_obj_list is empty (false)
            pass
        else:
            print("Currently in line:")
            print("------------------")
            for i in fy_obj_list:
                print(i)
            print("------------------")
        answer = input('sbID: ')
        if ((answer != 'done')
                and (answer != None)
                and (answer not in fy_obj_list)):
            fy_obj_list.append(answer)
    for i in fy_obj_list:
        gl.items_to_be_parsed.append(i)
    if gl.items_to_be_parsed != []:
        parse.main()  # pylint: disable=E1101
    else:
        return
    print("""

    ===========================================================================

                    Hard Search is now finished.""")


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
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (1)")
        nwcsc_fiscal_years = gl.exception_loop("4f8c64d2e4b0546c0c397b46", 
                                               ".get_child_ids")
        # nwcsc_fiscal_years = SB.get_child_ids("4f8c64d2e4b0546c0c397b46")
    try:
        swcsc_fiscal_years = SB.get_child_ids("4f8c6580e4b0546c0c397b4e")
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in full_hard_search (2)")
        swcsc_fiscal_years = gl.exception_loop("4f8c6580e4b0546c0c397b4e", 
                                               ".get_child_ids")
        # swcsc_fiscal_years = SB.get_child_ids("4f8c6580e4b0546c0c397b4e")
    fy_obj_list = []
    fy_obj_list[:] = []  # make double-sure it's empty
    create_fy_objs(fy_obj_list, nwcsc_fiscal_years, "NWCSC")
    create_fy_objs(fy_obj_list, swcsc_fiscal_years, "SWCSC")
    print("fy_obj_list:\n{0}".format(fy_obj_list))
    check_for_recency(fy_obj_list)
    if fy_obj_list:
        for fiscal_year in fy_obj_list:
            print("""
            Starting {0} ({1})
            CSC: {2}
            ===================================================================
            """.format(fiscal_year.name, fiscal_year.ID, fiscal_year.csc))
            try:
                project_ids = SB.get_child_ids(fiscal_year.ID)
            except Exception:
                project_ids = gl.exception_loop(fiscal_year.ID, 
                                                ".get_child_ids")
            project_obj_list = create_proj_objs(project_ids, fiscal_year)
            print(project_obj_list)
            for project in project_obj_list:
                print("""
                Starting Project: 
                {0} 
                ID: {1}
                CSC: {2}
                ---------------------------------------------------------------
                """.format(project.name, project.ID, project.csc))
                try:
                    project_child_ids = SB.get_child_ids(project.ID)
                except Exception:
                    project_child_ids = gl.exception_loop(project.ID, 
                                                          ".get_child_ids")
                    # project_child_ids = SB.get_child_ids(project.ID)
                approved_datasets = get_approved_datasets(project, 
                                                          project_child_ids)
                try:
                    proj_ancestors = SB.get_ancestor_ids(
                                                approved_datasets['id'])
                except Exception:
                    proj_ancestors = gl.exception_loop(approved_datasets['id'],
                                                       ".get_ancestor_ids")
                project_items = find_all_items(project, 
                                               fiscal_year, 
                                               proj_ancestors)
                for item in project_items:
                    print("Adding item...")
                    project.project_items["Project_Item_List"].append(item)
                    project.project_items["Project_Item_Count"] += 1
                    project.data_in_project += item.size
                #==============================================================
                fiscal_year.projects.append(project)
                fiscal_year.total_fy_data += project.data_in_project
                print("Saving Fiscal Year...")
                save_json(fiscal_year)
                fy_obj_list.remove(fiscal_year)


    if not fy_obj_list:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    elif fy_obj_list:
        full_hard_search()


def create_fy_objs(fy_obj_list, id_list, csc):
    for i in id_list:
        obj = gl.sb_fiscal_year(i, csc)
        obj.date = get_date()
        fy_obj_list.append(obj)
        print("{0} {1}: {2} fy object created and added to fy_obj_list."
              .format(obj.csc, obj.name, obj.ID))


def create_proj_objs(project_ids, fiscal_year):
    fy_projects = []
    proj_obj_list = []
    for project in project_ids:
        obj = gl.sb_project(project, fiscal_year)
        project_json = obj.sb_json
        try:
            if "Project" in project_json["browseCategories"] \
                    and project not in fy_projects:
                print("--Item is a project.")
                fy_projects.append(project)
                obj = gl.sb_project(project_json, fiscal_year)
                proj_obj_list.append(obj)
            elif "Project" in project_json["browseCategories"] \
                    and project in fy_projects:
                print("--Item already parsed.")
        except KeyError:
            print("--{0} not a project. This should be looked into..."
                  .format(project))
            print("Discarding {0}...".format(project))
            project_ids.remove(project)
            print("Back to finding projects...")
            continue
    # for project in proj_obj_list:
    #     project.Print()
    return proj_obj_list


def get_approved_datasets(project, project_child_ids):
    for item in project_child_ids:
        try:
            item_json = SB.get_item(item)
        except Exception:
            item_json = gl.exception_loop(item, ".get_item")
        if item_json['title'] == "Approved DataSets":
            approved_datasets = item_json
            break
        else:
            continue
    return approved_datasets


def find_all_items(project, fiscal_year, proj_ancestors):
    project_items = []
    project_items_ids = []
    for ID in proj_ancestors:
        if ID not in project_items_ids:
            project_items_ids.append(ID)
    all_items = find_shortcuts(project_items_ids)
    for item in all_items:
        item_obj = gl.sb_item(item)
        if not id_in_list(item_obj, project_items):
            project_items.append(item_obj)
    return project_items
    # project_items = find_shortcuts(project_items, )


class item_id(object):
    def __init__(self, sb_id):
        self.ID = sb_id
        self.shortcut_checked = False
        self.ancestor_checked = False

def find_shortcuts(project_items_ids):
    item_obj_list = []
    for sb_id in project_items_ids:
        obj = item_id(sb_id)
        obj.ancestor_checked = True
        item_obj_list.append(obj)
    item_ids = shortcut_loop(item_obj_list)
    return item_ids


def shortcut_loop(obj_list):
    for obj in obj_list:
        if not obj.shortcut_checked:
            try:
                shortcuts = SB.get_shortcut_ids(obj.ID)
            except Exception:
                shortcuts = gl.exception_loop(obj.ID, ".get_shortcut_ids")
            if shortcuts:
                for sb_id in shortcuts:
                    obj = item_id(sb_id)
                    obj_list.append(obj)
        if not obj.ancestor_checked:
            try:
                descendents = SB.get_shortcut_ids(obj.ID)
            except Exception:
                descendents = gl.exception_loop(obj.ID, ".get_shortcut_ids")
            if descendents:
                for sb_id in descendents:
                    obj = item_id(sb_id)
                    obj_list.append(obj)
    if shortcut_loop_control(obj_list):
        item_id_list = []
        for obj in obj_list:
            if obj.ID not in item_id_list:
                item_id_list.append(obj.ID)
        return item_id_list
    else:
        shortcut_loop(obj_list)


def shortcut_loop_control(obj_list):
    for obj in obj_list:
        if not obj.shortcut_checked:
            return False
        if not obj.ancestor_checked:
            return False
    return True


def id_in_list(obj_list, sb_object):
    obj_id = sb_object.ID
    for sb_object in obj_list:
        if obj_id == sb_object.ID:
            return True
    return False


def get_date():
    from datetime import datetime
    dateinfo = {}
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    return date


def check_for_recency(fy_obj_list):
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
                            continue
                        else:
                            # uncomment 'continue' if you want to do all FYs
                            # regardless of when they were last done:
                            # continue
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
    full_report_json = JsonTransformer()
    full_report_json = JsonTransformer.transform(full_report_json, fiscal_year)
    with open('./jsonCache/{0}.json'.format(fiscal_year.ID), 'w') as outfile:
        outfile.write(full_report_json)
    print("finished full_report_json:")
    pprint(full_report_json)  # Quantico

    return


if __name__ == "__main__":
    full_hard_search()
