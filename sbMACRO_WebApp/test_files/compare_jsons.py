import json
from pprint import pprint
import os
import shutil
from collections import Counter

def main():
    id_list = ["5006c2c9e4b0abf7ce733f42",  # NWCSC 2012
               "531899cce4b051b1b924ea01",  # NWCSC 2014
               "5007050de4b0abf7ce733fda",  # SWCSC 2012
               "531dd8c3e4b04cb293ee78ee"]  # SWCSC 2014
    print("{\\rtf1\\line")
    for sb_id in id_list:
        print("""\\line

                Starting New Fiscal Year: {0}\\line
                """.format(sb_id))
        # old_json = json.load(open('../jsonCache_old/{0}.json'.format(sb_id)))
        old_json = json.load(open(
            '/Users/taylorrogers/Documents/#Coding/oldsbJsons/newer_old_style/{0}.json'.format(sb_id)))
        new_json = json.load(open('../jsonCache/{0}.json'.format(sb_id)))

        # Total FY Data check
        old_total_fy_data = old_json["report"][0]["totalFYData"]
        if old_total_fy_data is not None:
             old_total_fy_data = old_total_fy_data * 1000  # to convert to megabytes
        new_total_fy_data = new_json["total_fy_data"]
        difference = old_total_fy_data - new_total_fy_data
        print(
"""
\\line
\\line        Old Total FY Data:              {0}
\\line        New Total FY Data:              {1}
\\line        ------------------------------------------------
\\line        Difference:                     {2}
\\line
              """.format(old_total_fy_data, new_total_fy_data, difference))

        # Number (and name?) of Projects check
        old_num_projects = len(old_json["report"])
        new_num_projects = len(new_json["projects"])
        difference = old_num_projects - new_num_projects
        print(
"""\\line\\line
\\line        Old Number of Projects:              {0}
\\line        New Number of Projects:              {1}
\\line        ------------------------------------------------
\\line        Difference:                          {2}

              """.format(old_num_projects, new_num_projects, difference))
        # Project size check
        old_projects = old_json["report"]
        new_projects = new_json["projects"]
        project_comparison_list = []
        for old_project in old_projects:
            old_id = old_project["ID"]
            new_project = get_matching_project(new_projects, old_id)
            comp_obj = sb_project(old_project, new_project)
            if comp_obj:
                project_comparison_list.append(comp_obj)
        print(
            """\\line\\line\\line
===============================================================================
""")
        for obj in project_comparison_list:
            size_diff = obj.old_size - obj.new_size
            old_i_count = len(obj.old_items)
            new_i_count = len(obj.new_items)
            item_count_diff = old_i_count - new_i_count

            old_f_count = len(obj.old_files)
            new_f_count = len(obj.new_files)
            file_count_diff = old_f_count - new_f_count
            if item_count_diff != 0 or file_count_diff != 0:

                print("""\\line\\line\\b {0} \\b0
\\line            ({1})
\\line        Old Project Size:\t\t\t{2}
\\line        New Project Size:\t\t\t{3}
\\line        ----------------------------------------------------------
\\line        Difference:\t\t\t\t{4}
\\line
\\line        Old Project Item Count\t\t\t{5}
\\line        New Project Item Count:\t\t\t{6}
\\line        ----------------------------------------------------------
\\line        Difference:\t\t\t\t{7}
\\line
\\line        Old Project File Count\t\t\t{8}
\\line        New Project File Count:\t\t\t{9}
\\line        ----------------------------------------------------------
\\line        Difference:\t\t\t\t{10}
\\line\\line        """.format(obj.name, obj.ID, obj.old_size, obj.new_size, 
                               size_diff, old_i_count, new_i_count, 
                               item_count_diff, old_f_count, new_f_count, 
                               file_count_diff))
                if item_count_diff != 0:
                    find_missing_items(obj.old_items, 
                                                    obj.new_items)
                if file_count_diff != 0:
                    find_missing_files(obj.old_files,
                                                    obj.new_files)
        print("===============================================================================")
        print("\\line\\lineCompleted Check")

    print("\\line}")


def find_missing_items(old_items, new_items):
    # First make a list of ids for old items
    old_items_id_list = []
    for old_item in old_items:
        old_items_id_list.append(old_item['id'])
    #find length
    old_list_len = len(old_items_id_list)
    print("\\line Here are the old items:\\line Length: {0}\\line"
          .format(old_list_len))
    if old_list_len < 200:
        print(old_items_id_list)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")
    # Create set from list
    old_items_id_set = set(old_items_id_list)
    #find length of set
    old_set_len = len(old_items_id_set)
    print("\\line Here is are the old items as a set:\\line Length: {0}\\line"
          .format(old_set_len))
    # Compare set and list length
    old_list_set_diff = old_list_len - old_set_len
    if old_list_set_diff != 0:
        print("\\line - Difference: {0}".format(old_list_set_diff))
        doubled_items = list(Counter(old_items_id_list) -
                             Counter(list(old_items_id_set)))
        print("\\line Here are the files in the new list that were doubled: \\line")
        print(doubled_items)
    if old_set_len < 200:
        print(old_items_id_set)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")

    # Now the same for list of ids for new items
    new_items_id_list = []
    for new_item in new_items:
        new_items_id_list.append(new_item['ID'])
    # find length
    new_list_len = len(new_items_id_list)
    print("\\line Here are the new items:\\line Length: {0}\\line"
          .format(new_list_len))
    if new_list_len < 200:
        print(new_items_id_list)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")
    # Create set from list
    new_items_id_set = set(new_items_id_list)
    # find length of set
    new_set_len = len(new_items_id_set)
    print("\\line Here is are the new items as a set:\\line Length: {0}\\line"
          .format(new_set_len))
    # Compare set and list length
    new_list_set_diff = new_list_len - new_set_len
    if new_list_set_diff != 0:
        print("\\line - Difference: {0}".format(new_list_set_diff))
        doubled_items = list(Counter(new_items_id_list) -
                             Counter(list(new_items_id_set)))
        print("\\line Here are the files in the new list that were doubled: \\line")
        print(doubled_items)
    if new_set_len < 200:
        print(new_items_id_set)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")

    print("\\line  Checking each old id for presence in new set:")
    print("\\line Old - New: \\line")
    print(list(old_items_id_set - new_items_id_set))
    print("\\line New - Old: \\line")
    print(list(new_items_id_set - old_items_id_set))
    print(" \\line")
    return



def find_missing_files(old_files, new_files):
    # First make a list of ids for old files
    old_files_id_list = []
    for old_item in old_files:
        old_files_id_list.append(old_item['pathOnDisk'])
    #find length
    old_list_len = len(old_files_id_list)
    print("\\line Here are the old files: \\line Length: {0}\\line"
          .format(old_list_len))
    if old_list_len < 200:
        print(old_files_id_list)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")
    # Create set from list
    old_files_id_set = set(old_files_id_list)
    #find length of set
    old_set_len = len(old_files_id_set)
    print("\\line Here is are the old files as a set:\\line Length: {0}\\line"
          .format(old_set_len))
    # Compare set and list length
    old_list_set_diff = old_list_len - old_set_len
    if old_list_set_diff != 0:
        print("\\line - Difference: {0}".format(old_list_set_diff))
        doubled_files = list(Counter(old_files_id_list) - Counter(list(old_files_id_set)))
        print("\\line Here are the files in the new list that were doubled: \\line")
        print(doubled_files)
    if old_set_len < 200:
        print(old_files_id_set)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")


    # Now the same for list of ids for new files
    new_files_id_list = []
    for new_item in new_files:
        new_files_id_list.append(new_item['pathOnDisk'])
    # find length
    new_list_len = len(new_files_id_list)
    print("\\line Here are the new files:\\line Length: {0}\\line"
          .format(new_list_len))
    if new_list_len < 200:
        print(new_files_id_list)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")
    # Create set from list
    new_files_id_set = set(new_files_id_list)
    # find length of set
    new_set_len = len(new_files_id_set)
    print("\\line Here is are the new files as a set:\\line Length: {0}\\line"
          .format(new_set_len))
    # Compare set and list length
    new_list_set_diff = new_list_len - new_set_len
    if new_list_set_diff != 0:
        print("\\line - Difference: {0}".format(new_list_set_diff))
        doubled_files = list(Counter(new_files_id_list) - Counter(list(new_files_id_set)))
        print("\\line Here are the files in the new list that were doubled: \\line")
        print(doubled_files)

    if new_set_len < 200:
        print(new_files_id_set)
    else:
        print("\\line [LIST TOO LONG TO PRINT (over 200 items)]\\line")

    print("\\line  Checking each old id for presence in new set:")
    print("\\line Old - New: \\line")
    print(list(old_files_id_set - new_files_id_set))
    print("\\line New - Old: \\line")
    print(list(new_files_id_set - old_files_id_set))
    print(" \\line")
    return


        

class sb_project(object):
    def __init__(self, old_project, new_project):
        # to convert to megabytes, multiply old data by 1000
        old_size = old_project["DataInProject"]
        # print("-----------------------old_size! {0}".format(old_size))
        if "None" in str(old_size):
            # print("---Value is 'None'\n---Set to 0.")
            old_size = 0
        elif "None" not in str(old_size):
            # print("---Value is not 'None'\n---Multiplied by 1000.")
            old_size = old_size * 1000
        old_fy_data = old_project["totalFYData"]
        # print("-----------------------old_fy_data! {0}".format(old_fy_data))
        if "None" in str(old_fy_data):
            # print("---Value is 'None'\n---Set to 0.")
            old_fy_data = 0
        elif "None" not in str(old_fy_data):
            # print("---Value is not 'None'\n---Multiplied by 1000.")
            old_fy_data = old_fy_data * 1000
        self.ID = old_project["ID"]
        self.name = old_project["name"]
        self.old_size = old_size
        self.new_size = new_project["data_in_project"]
        self.old_fy_data = old_fy_data
        self.new_fy_data = new_project["total_fy_data"]
        self.old_files = old_project["ProjectFiles"]["Project_File_List"]
        self.new_files = new_project["project_files"]["Project_File_List"]
        self.old_items = old_project["ProjectItems"]["Project_Item_List"]
        self.new_items = new_project["project_items"]["Project_Item_List"]


def get_matching_project(project_list, sb_id):
    for project in project_list:
        if project["ID"] == sb_id:
            return project
    print("---------------No matching ID found!")
    return None



if __name__ == "__main__":
    main()
