#pylint: disable=W0703
"""Fiscal Year, Project, and Item class definitions and exception_loop()."""
import pysb  # pylint: disable=wrong-import-order

SB = pysb.SbSession()

class SbFiscalYear(object):  # pylint: disable=R0902,R0903
    """Science Base Fiscal Year object."""

    def __init__(self, sb_id, csc):
        """Initialize of SbFiscalYear object."""
        try:
            fy_json = SB.get_item(sb_id)
        except Exception:
            if __debug__:
                print("Exception Raised when creating Fiscal Year object for"
                      + " {0}".format(sb_id))
            fy_json = exception_loop(sb_id, ".get_item")
        self.ID = sb_id  # pylint: disable=C0103
        self.URL = fy_json['link']['url']  # pylint: disable=C0103
        self.object_type = "Fiscal Year"
        self.name = fy_json['title'].replace(' Projects', '')
        self.csc = csc
        self.date = None
        self.total_fy_data = 0
        self.exceptions = []
        self.missing = []
        self.projects = []
        self.sb_json = fy_json

    def Print(self, long=False):  # pylint: disable=C0103
        """Print contents of SbFiscalYear object.

        Pass 'True' to this function to print out all Fiscal Year info.

        Arguments:
            long -- (boolean, optional) if True, Project Item and File lists
                    are also printed.

        """
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


class SbProject(object):  # pylint: disable=R0902,R0903
    """Science Base Project object."""

    def __init__(self, proj_id, fy):
        """Initialize of SbProject object."""
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
        self.ID = proj_json['id']  # pylint: disable=C0103
        self.URL = proj_json['link']['url']  # pylint: disable=C0103
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

    def Print(self, long=False):  # pylint: disable=C0103
        """Print contents of SbProject object.

        If 'True' is sent as argument, All items and files are printed as
        well.

        Arguments:
            long -- (boolean, optional) if True, Project Item and File lists
                    are also printed.

        """
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
        """.format(self.object_type, self.ID, self.name, self.fiscal_year,
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


class SbItem(object):  # pylint: disable=R0902,R0903
    """Science Base Item object."""

    def __init__(self, sb_id):
        """Initialize SbItem object."""
        try:
            item_json = SB.get_item(sb_id)
        except Exception:
            if __debug__:
                print("Exception Raised when creating Item object for"
                      + " {0}".format(sb_id))
            item_json = exception_loop(sb_id, ".get_item")
        item_data = check_for_files(item_json)
        self.ID = sb_id  # pylint: disable=C0103
        self.URL = item_json['link']['url']  # pylint: disable=C0103
        self.object_type = "Item"
        self.name = item_json['title']
        self.size = item_data['size']
        self.num_files = item_data['num_files']
        self.file_list = item_data['file_list']
        self.sb_json = item_json

    def Print(self):  # pylint: disable=C0103
        """Print contents of SbItem object."""
        print("""
        Object Type: {0}
        URL: {1}
        ID: {2}
        Name: {3}
        """.format(self.object_type, self.URL, self.ID, self.name))

def check_for_files(item_json):
    """Find all files and extentions of an item, add their size together.

    Arguments:
        item_json -- (json) the json of the item being parsed.

    Returns:
        item_data -- (dictionary) a dictionary including a list of all
                        file jsons attached to the item, the total size of
                        the item, and the number of files found within the
                        item.

    """
    file_list = []
    size = 0
    try:
        files = item_json["files"]
        for sb_file in files:
            file_list.append(sb_file)
            size += sb_file["size"]
    except KeyError:
        pass  # No files
    try:
        extentions = item_json["facets"]
        for extention in extentions:
            try:
                files = extention["files"]
                for sb_file in files:
                    file_list.append(sb_file)
                    size += sb_file["size"]
            except KeyError:
                pass  # No files
    except KeyError:
        pass  # No extentions
    num_files = len(file_list)
    item_data = {"file_list": file_list,
                 "size": size,
                 "num_files": num_files}
    return item_data


def exception_loop(item_id, sb_action):
    """Control loop to handle Exception raised by Science Base.

    Arguments:
        item_id -- (string) the Science Base ID whose request raised the
                   Exception from Science Base.
        sb_action -- (string) the Science Base function name that was being
                     used when the Exception was raised by Science Base.

    Returns:
        result -- (json, string, or list) the result of the appropriate
                  Science Base function if it was successful.

    """
    import exception_raised
    result = exception_raised.main(item_id, sb_action)
    if result != False:
        return result
    elif result is False:
        exception_loop(item_id, sb_action)
