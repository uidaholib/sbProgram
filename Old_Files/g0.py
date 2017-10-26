"""This module contains variables that need accessed by all modules in the
ScienceBase MACRO program.

This module contains empty lists to be populated with all ScienceBase items,
projects, and Fiscal Years to be accessed from all other modules via "g.items",
"g.projects", "g.FiscalYears" and g.itemsToBeParsed. It also contains the total
data count, and the variables needed to print data counting info to excel."""

#itemsToBeParsed = ["4f8c64d2e4b0546c0c397b46", "5006c2c9e4b0abf7ce733f42", "55e4d96be4b05561fa208585", "58111fafe4b0f497e79892f7"]
#itemsToBeParsed = ["5006c2c9e4b0abf7ce733f42"]
itemsToBeParsed = []
items = []
#projects = ["5006e99ee4b0abf7ce733f58", "55ae7b23e4b066a249242391", "5006e94ee4b0abf7ce733f56"]
projects = []
fiscalYears = []
onTheFlyParsing = []

totalDataCount = 0
totalFYData = 0

# Lists to be printed to Excel:
# Project sheet:
ID = []  # Added
ObjectType = []  # Added
Name = []  # Added
FiscalYear = []  # Added
Project = []  # Added
DataInProject = []   # Added
DataPerFile = []   # Added
totalFYDataList = []
RunningDataTotal = []  # Added


# Other sheets
MissingData = []
Exceptions = []

import sys
import inspect
import traceback #as tback
from pprint import pprint



def excepthook(type_, value, tback_):
    if type_ is Exception:
        print(tback_)
        CodeString = inspect.getsource(tback_)
        print(CodeString)

        tbNext = tback_.tb_next
        print(tbNext)
        CodeString = inspect.getsource(tbNext)
        print(CodeString)

        tbNext2 = tbNext.tb_next
        print(tbNext2)
        CodeString = inspect.getsource(tbNext2)
        print(CodeString)

        print("Last frame:\n")
        tb = tback_
        while 1:
            print(tb)

            try:
                CodeString = inspect.getsource(tb)
                print(CodeString)
                lastTB = tb
                tb = tb.tb_next
            except TypeError:
                print("BREAK!")
                tb = lastTB
                print(tb)
                CodeString = inspect.getsource(tb)
                print(CodeString)
                break

        print("Last Frame")
        frame = tb.tb_frame
        print(frame)
        CodeString = inspect.getsource(frame)
        print(CodeString)

        findVariable(type_, value, tback_, frame)
        print("Finally! Here's your variable:")
        print(problemID)
        print("ProblemID: {0}".format(problemID))
    else:
        Error_Trace = traceback.format_tb(tback_)
        print(Error_Trace)

def findVariable(type_, value, tback_, frame):
    localVars = frame.f_locals
    pprint(localVars)
    problemID = None
    for key in localVars.keys():
        if key == 'ID':
            problemID = frame.f_locals['ID']
            print("Found it")
            print(problemID)
            return(problemID)         # AT THIS POINT, YOU HAVE THE VARIABLE. JUST NEED TO CHANGE ALL TO THE SAME VARIABLE, AND CALL EXCEPTION HANDLING FUNCTION
    if problemID != None:
        return(problemID)
    print("Frame back")
    frame = frame.f_back
    print(frame)
    CodeString = inspect.getsource(frame)
    print(CodeString)
    findVariable(type_, value, tback_, frame)
