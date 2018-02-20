# pylint: disable=C0103
"""Variables for access by all modules in the ScienceBase MACRO program.

This module contains empty lists to be populated with all ScienceBase items,
projects, and Fiscal Years to be accessed from all other modules via
"gl.items","gl.projects", "gl.FiscalYears" and gl.items_to_be_parsed. It also
contains the total data count, and the variables needed to print data counting
info to excel.
"""
import pysb  # pylint: disable=wrong-import-order

SB = pysb.SbSession()

class sb_fiscal_year(object):
    """Science Base Fiscal Year object."""

    def __init__(self, sb_id, csc):
        """Initialize of sb_fiscal_year object."""
        try:
            fy_json = SB.get_item(sb_id)
        except Exception:
            if __debug__:
                print("Exception Raised when creating Fiscal Year object for"
                      + " {0}".format(sb_id))
            fy_json = exception_loop(sb_id, ".get_item")
        self.ID = sb_id
        self.URL = fy_json['link']['url']
        self.object_type = "Fiscal Year"
        self.name = fy_json['title'].replace(' Projects', '')
        self.csc = csc
        self.date = None
        self.total_fy_data = 0
        self.exceptions = []
        self.missing = []
        self.projects = []
        self.sb_json = fy_json

    def Print(self, long=False):
        """Print contents of sb_fiscal_year object.
        
        Pass true to this function to print out all project info."""
        print("""
        Object Type: {0}
        ID: {1}
        Name: {2}
        CSC: {3}
        URL: {4}
        Date: {5}
        Total FY Data: {6}
        
        Exceptions: {7}
        Missing: {8}"""
        .format(self.object_type, self.ID, self.name, self.csc, self.URL,
                   self.date, self.total_fy_data, self.exceptions, 
                   self.missing))
        
        if long:
            print("""
        Projects: 
        {0}
        ----------------------------------------------------------------------
                  """.format(self.projects))
        else:
            print("""
        Projects: 
        ***Pass boolean 'True' to Print() to show Projects***
        ----------------------------------------------------------------------
                  """.format(self.projects))


class sb_project(object):
    """Science Base Project object."""

    def __init__(self, proj_id, fy):
        """Initialize of sb_project object."""
        try:
            proj_json = SB.get_item(proj_id)
        except Exception:
            if __debug__:
                print("Exception Raised when creating Project object for"
                      + " {0}".format(proj_id))
            proj_json = exception_loop(proj_id, ".get_item")
        project_items_specs = {"Project_Item_Count": 0,
                               "Project_Item_List": []}
        project_files_specs = {"Project_File_Count": 0,
                               "Project_File_List": []}
        self.ID = proj_json['id']
        self.URL = proj_json['link']['url']
        self.object_type = "Project"
        self.name = proj_json['title']
        self.fiscal_year = fy.name
        self.csc = fy.csc
        self.data_in_project = 0
        self.data_per_file = None
        self.total_fy_data = None
        self.project_items = project_items_specs
        self.project_files = project_files_specs
        self.sb_json = proj_json

    def Print(self, long=False):
        """Print contents of sb_project object."""
        print("""
        Object Type: {0}
        ID: {1}
        Name: {2}
        Fiscal Year: {3}
        CSC: {4}
        URL: {5}
        Data In Project: {6}
        Data per File: {7}
        Total FY Data:
        {8}
        """.format(self.object_type, self.ID,  self.name, self.fiscal_year,
                   self.csc, self.URL, self.data_in_project,
                   self.data_per_file, self.total_fy_data))

        if long:
            print("""
        Project Items:
        {0}

        Project Files:
        {1}
        ----------------------------------------------------------------------
                  """.format(self.project_items, self.project_files))
        else:
            print("""
        Project Items:
        ***Pass boolean 'True' to Print() to show Project Items***

        Project Files:
        ***Pass boolean 'True' to Print() to show Project Items***
        ----------------------------------------------------------------------
                  """)

class sb_item(object):
    """Science Base Item object."""

    def __init__(self, sb_id):
        """Initialize of sb_item object."""
        try:
            item_json = SB.get_item(sb_id)
        except Exception:
            if __debug__:
                print("Exception Raised when creating Item object for"
                      + " {0}".format(sb_id))
            item_json = exception_loop(sb_id, ".get_item")
        self.ID = sb_id
        self.URL = item_json['link']['url']
        self.object_type = "Item"
        self.name = item_json['title']
        self.size = self.check_for_files(item_json)
        self.sb_json = item_json

    def Print(self):
        """Print contents of sb_item object."""
        print("""
        Object Type: {0}
        URL: {1}
        ID: {2}
        Name: {3}
        """.format(self.object_type, self.URL, self.ID, self.name))
    
    def check_for_files(self, item_json):
        size = 0
        try:
            files = item_json["files"]
            for sb_file in files:
                size += sb_file["size"]
        except KeyError:
            pass  # No files
        try:
            extentions = item_json["facets"]
            for extention in extentions:
                try:
                    files = extention["files"]
                    for sb_file in files:
                        size += sb_file["size"]
                except KeyError:
                    pass  # No files
        except KeyError:
            pass  # No extentions
        return size



def exception_loop(item_id, sb_action):
    import exception_raised
    result = exception_raised.main(item_id, sb_action)
    if result:
        return result
    elif not result:
        exception_loop(item_id, sb_action)

# items_to_be_parsed = []
# items = []
# projects = []
# fiscalYears = []
# on_the_fly_parsing = []

# totalDataCount = 0
# total_fy_data = 0

# current_item = None

# ID = []  # Added
# URL = []
# object_type = []  # Added
# name = []  # Added
# fiscal_year = []  # Added
# project = []  # Added
# data_in_project = []   # Added
# data_per_file = []   # Added
# total_fy_data_list = []
# running_data_total = []  # Added

# project_files = {}
# project_items = {}

# # Other sheets
# missing_data = []
# exceptions = []

# Excel_choice = None
