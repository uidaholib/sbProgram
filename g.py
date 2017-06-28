"""This module contains variables that need accessed by all modules in the
ScienceBase MACRO program.

This module contains empty lists to be populated with all ScienceBase items,
projects, and Fiscal Years to be accessed from all other modules via "g.items",
"g.projects", "g.FiscalYears" and g.itemsToBeParsed. It also contains the total
data count, and the variables needed to print data counting info to excel."""

itemsToBeParsed = ["4f8c64d2e4b0546c0c397b46", "5006c2c9e4b0abf7ce733f42", "55e4d96be4b05561fa208585", "58111fafe4b0f497e79892f7"]
items = []
projects = []
fiscalYears = ["5006e94ee4b0abf7ce733f56"]
onTheFlyParsing = []

totalDataCount = 0

# Lists to be printed to Excel:
# Project sheet:
ID = []
ObjectType = []
Name = []
FiscalYear = []
Project = []
DataInProject = []
DataPerFile = []
RunningDataTotal = []
NestedData = []

# Other sheets
MissingData = []
Exceptions = []
