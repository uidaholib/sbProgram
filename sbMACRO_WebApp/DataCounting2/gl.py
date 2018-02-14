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

    def __init__(self, sb_id):
        """Initialize of sb_fiscal_year object."""
        fy_json = SB.get_item(sb_id)
        self.ID = sb_id
        self.URL = fy_json['link']['url']
        self.ObjectType = "Fiscal Year"
        self.name = fy_json['title'].replace(' Projects', '')
        self.projects = []
        self.date = None
        self.identity = None
        self.exceptions = []
        self.missing = []

    def Print(self):
        """Print contents of sb_fiscal_year object."""
        print("""
        Object Type: {0}
        URL: {1}
        ID: {2}
        Name: {3}
        Date: {4}
        Identity: 
        {5}
        
        Exceptions: {6}
        Missing: {7}
        
        Projects:
        {8}
        """.format(self.ObjectType, self.URL, self.ID,  self.name, self.date,
                   self.identity, self.exceptions, self.missing, self.projects))


class sb_project(object):
    """Science Base Project object."""

    def __init__(self, sb_id):
        """Initialize of sb_project object."""
        proj_json = SB.get_item(sb_id)
        project_items_specs = {"Project_File_Count": 0,
                               "Project_File_List": []}
        project_files_specs = {"Project_Item_Count": 0,
                               "Project_Item_List": []}
        self.ID = sb_id
        self.URL = proj_json['link']['url']
        self.ObjectType = "Project"
        self.name = proj_json['title']
        self.DataInProject = None
        self.DataPerFile = None
        self.ProjectItems = project_items_specs
        self.ProjectFiles = project_files_specs
        self.totalFYData = None

    def Print(self):
        """Print contents of sb_project object."""
        print("""
        Object Type: {0}
        URL: {1}
        ID: {2}
        Name: {3}
        Data In Project: {4}
        Data per File: {5}
        Project Items:
        {6}

        Project Files:
        {7}
        
        Total FY Data:
        {8}
        """.format(self.ObjectType, self.URL, self.ID,  self.name,
                   self.DataInProject, self.DataPerFile, self.ProjectItems,
                   self.ProjectFiles, self.totalFYData))

class sb_item(object):
    """Science Base Item object."""

    def __init__(self, sb_id):
        """Initialize of sb_item object."""
        item_json = SB.get_item(sb_id)
        self.ID = sb_id
        self.URL = item_json['link']['url']
        self.ObjectType = "Item"
        self.name = item_json['title']

    def Print(self):
        """Print contents of sb_item object."""
        print("""
        Object Type: {0}
        URL: {1}
        ID: {2}
        Name: {3}
        """.format(self.ObjectType, self.URL, self.ID, self.name))


items_to_be_parsed = []
items = []
projects = []
fiscalYears = []
on_the_fly_parsing = []

totalDataCount = 0
totalFYData = 0

current_item = None

ID = []  # Added
URL = []
object_type = []  # Added
name = []  # Added
fiscal_year = []  # Added
project = []  # Added
data_in_project = []   # Added
data_per_file = []   # Added
total_fy_data_list = []
running_data_total = []  # Added

project_files = {}
project_items = {}

# Other sheets
missing_data = []
exceptions = []

Excel_choice = None
