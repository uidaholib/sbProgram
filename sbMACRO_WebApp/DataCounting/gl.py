"""This module contains variables that need accessed by all modules in the
ScienceBase MACRO program.

This module contains empty lists to be populated with all ScienceBase items,
projects, and Fiscal Years to be accessed from all other modules via "gl.items",
"gl.projects", "gl.FiscalYears" and gl.itemsToBeParsed. It also contains the total
data count, and the variables needed to print data counting info to excel."""

#itemsToBeParsed = ["4f8c64d2e4b0546c0c397b46", "5006c2c9e4b0abf7ce733f42", "55e4d96be4b05561fa208585", "58111fafe4b0f497e79892f7"]
#itemsToBeParsed = ["5006c1e5e4b0abf7ce733f3b", "5006c2c9e4b0abf7ce733f42"]
itemsToBeParsed = []
items = []
#projects = ["5006e99ee4b0abf7ce733f58", "55ae7b23e4b066a249242391", "5006e94ee4b0abf7ce733f56"]
projects = []
fiscalYears = []
onTheFlyParsing = []

totalDataCount = 0
totalFYData = 0

Current_Item = None
# # Lists to be printed to Excel:
# # Project sheet:
ID = []  # Added
ObjectType = []  # Added
Name = []  # Added
FiscalYear = []  # Added
Project = []  # Added
DataInProject = []   # Added
DataPerFile = []   # Added
totalFYDataList = []
RunningDataTotal = []  # Added
# For debugging:
# ID = ['1', '2', '3', '4']  # Added
# ObjectType = ['Project1', 'Project2', 'Project3', 'Project4']  # Added
# Name = ['Name1', 'Name2', 'Name3', 'Name4']  # Added
# FiscalYear = ['2020', '2020', '2020', '2020']  # Added
# Project = ['Project Name1', 'Project Name2',
#            'Project Name3', 'Project Name4']  # Added
# DataInProject = ['1', '2', '3', '4']   # Added
# DataPerFile = ["['2023', '39930', '9938']",
#                "['3536', '5479', '57221']", "['5682', '3984368930', '94658938']", "['34633', '3975437930']"]   # Added
# totalFYDataList = ['939239549', '939239549', '939239549', '939239549']
# RunningDataTotal = ['9284054281', '9284054282',
#                     '9284054283', '9284054284']  # Added


# Other sheets
MissingData = []
Exceptions = []

Excel_choice = None
