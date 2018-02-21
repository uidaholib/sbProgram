import json
from pprint import pprint
import os
import shutil

def main():
    id_list = ["5006c2c9e4b0abf7ce733f42",  # NWCSC 2012
               "531899cce4b051b1b924ea01",  # NWCSC 2014
               "5007050de4b0abf7ce733fda",  # SWCSC 2012
               "531dd8c3e4b04cb293ee78ee"]  # SWCSC 2014
    for sb_id in id_list:
        print("""
==============================================================================
==============================================================================
==============================================================================
                Starting New Fiscal Year: {0}
                """.format(sb_id))
        old_json = json.load(open('../jsonCache_old/{0}.json'.format(sb_id)))
        new_json = json.load(open('../jsonCache/{0}.json'.format(sb_id)))

        # Total FY Data check
        old_total_fy_data = old_json["report"][0]["totalFYData"]
        if old_total_fy_data is not None:
             old_total_fy_data = old_total_fy_data * 1000  # to convert to megabytes
        new_total_fy_data = new_json["total_fy_data"]
        difference = old_total_fy_data - new_total_fy_data
        print(
"""

        Old Total FY Data:              {0}
        New Total FY Data:              {1}
        ------------------------------------------------
        Difference:                     {2}

              """.format(old_total_fy_data, new_total_fy_data, difference))

        # Number (and name?) of Projects check
        old_num_projects = len(old_json["report"])
        new_num_projects = len(new_json["projects"])
        difference = old_num_projects - new_num_projects
        print(
"""\n\n
        Old Number of Projects:              {0}
        New Number of Projects:              {1}
        ------------------------------------------------
        Difference:                          {2}

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
            """\n\n\n
===============================================================================
""")
        for obj in project_comparison_list:
            diff = obj.old_size - obj.new_size
            print("""{0}
            ({1})
        Old Project Size:\t\t\t{2}
        New Project Size:\t\t\t{3}
        ----------------------------------------------------------
        Difference:\t\t\t\t{4}
        """.format(obj.name, obj.ID, obj.old_size, obj.new_size, diff))
        print("===============================================================================")
        print("\n\nCompleted Check")




        

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


def get_matching_project(project_list, sb_id):
    for project in project_list:
        if project["ID"] == sb_id:
            return project
    print("---------------No matching ID found!")
    return None



if __name__ == "__main__":
    main()
