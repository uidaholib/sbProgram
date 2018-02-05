# pylint: disable=C0103
"""Variables for access by all modules in the ScienceBase MACRO program.

This module contains empty lists to be populated with all ScienceBase items,
projects, and Fiscal Years to be accessed from all other modules via
"gl.items","gl.projects", "gl.FiscalYears" and gl.items_to_be_parsed. It also
contains the total data count, and the variables needed to print data counting
info to excel.
"""

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
