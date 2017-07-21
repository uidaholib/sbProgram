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
import traceback as tback
from pprint import pprint



def excepthook(type_, value, traceback):
    if type is Exception:
        trying = tback.extract_tb(traceback)
        pprint(trying)
        trying2 = tback.format_tb(traceback)
        pprint(trying2)
        trying3 = tback.print_tb(traceback)
        pprint(trying3)
        CodeString = inspect.getsource(traceback)
        print(CodeString)
        tb = traceback
        while 1:
            if not tb.tb_next:
                break
            tb = tb.tb_next
        stack = []
        f = traceback.tb_frame
        while f:
            stack.append(f)
            f = f.f_back
        CodeStringLines = inspect.getsourcelines(tb)
        print(CodeStringLines[0])
        RevCodeStringLines = CodeStringLines[0][::-1]
        print(RevCodeStringLines)
        for i in RevCodeStringLines: #this is working sort of. I just have to find out how to get it to the corect frame.
        #Perhaps go to the last frame in a traceback that goes until the exception, then find the last "sb." thing, then the variable before that.
            if "sb." in i:
                print(i)
            else:
                print("Does not contain sb.")
        print("""

        """)
        for i in CodeStringLines[0]: #this is working sort of. I just have to find out how to get it to the corect frame.
        #Perhaps go to the last frame in a traceback that goes until the exception, then find the last "sb." thing, then the variable before that.
            if "sb." in i:
                print(i)
            else:
                print("Does not contain sb.")

        # What I need is to iterate through the reversed frame, looking for sb. in each line.



def example():
#from http://code.activestate.com/recipes/52215-get-more-information-from-tracebacks/
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    tb = traceback
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = traceback.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    print('Raised %d: %d') % type_, value
    print("Locals by frame, innermost last")
    for frame in stack:
        print()
        print("Frame %s in %s at line %s") % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.items():
            print("\t%20s = ") % key,
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:
                print(value)
            except:
                print("<ERROR WHILE PRINTING VALUE>")
#-------------------------------------------------------------------------------
#example problem script:

if __name__ == '__main__':
    #A simplistic demonstration of the kind of problem this approach can help
    #with. Basically, we have a simple function which manipulates all the
    #strings in a list. The function doesn't do any error checking, so when
    #we pass a list which contains something other than strings, we get an
    #error. Figuring out what bad data caused the error is easier with our
    #new function.

    data = ["1", "2", 3, "4"] #Typo: We 'forget' the quotes on data[2]
    def pad4(seq):
        """
        Pad each string in seq with zeros, to four places. Note there
        is no reason to actually write this function, Python already
        does this sort of thing much better.
        Just an example.
        """
        return_value = []
        for thing in seq:
            return_value.append("0" * (4 - len(thing)) + thing)
        return(return_value)

    #First, show the information we get from a normal traceback.print_exc().
    try:
        pad4(data)
    except:
        traceback.print_exc()
    print()
    print("----------------")
    print()

    #Now with our new function. Note how easy it is to see the bad data that
    #caused the problem. The variable 'thing' has the value 3, so we know
    #that the TypeError we got was because of that. A quick look at the
    #value for 'data' shows us we simply forgot the quotes on that item.
    try:
        pad4(data)
    except:
        print_exc_plus()

#-----------------------------------------------------------------------------



def pause():
    if type is Exception:
        trying = tback.extract_tb(traceback)
        pprint(trying)
        trying2 = tback.format_tb(traceback)
        pprint(trying2)
        trying3 = tback.print_tb(traceback)
        pprint(trying3)
        CodeString = inspect.getsource(traceback)
        print(CodeString)
        tb = traceback
        while tb.tb_next:
            tb = traceback.tb_next

        CodeStringLines = inspect.getsourcelines(tb)
        print(CodeStringLines[0])
        RevCodeStringLines = CodeStringLines[0][::-1]
        print(RevCodeStringLines)
        for i in RevCodeStringLines: #this is working sort of. I just have to find out how to get it to the corect frame.
        #Perhaps go to the last frame in a traceback that goes until the exception, then find the last "sb." thing, then the variable before that.
            if "sb." in i:
                print(i)
            else:
                print("Does not contain sb.")
        print("""

        """)
        for i in CodeStringLines[0]: #this is working sort of. I just have to find out how to get it to the corect frame.
        #Perhaps go to the last frame in a traceback that goes until the exception, then find the last "sb." thing, then the variable before that.
            if "sb." in i:
                print(i)
            else:
                print("Does not contain sb.")

        # What I need is to iterate through the reversed frame, looking for sb. in each line.




def oldagain():
        CodeString = inspect.getsource(traceback)
        print(CodeString)
        CodeStringLines = inspect.getsourcelines(traceback)
        print(CodeStringLines[0])
        RevCodeStringLines = CodeStringLines[0][::-1]
        print(RevCodeStringLines)
        for i in RevCodeStringLines: #this is working sort of. I just have to find out how to get it to the corect frame.
        #Perhaps go to the last frame in a traceback that goes until the exception, then find the last "sb." thing, then the variable before that.
            if "sb." in i:
                print(i)
            else:
                print("Does not contain sb.")
        print("""

        """)
        for i in CodeStringLines[0]: #this is working sort of. I just have to find out how to get it to the corect frame.
        #Perhaps go to the last frame in a traceback that goes until the exception, then find the last "sb." thing, then the variable before that.
            if "sb." in i:
                print(i)
            else:
                print("Does not contain sb.")

        # What I need is to iterate through the reversed frame, looking for sb. in each line.


        possibleLines = []
        num = 43 #need to parse above to get this
        IterCodeString = iter(CodeString.splitlines()) #This doesn't work
        print("IterCodeString")
        print(IterCodeString)
        for i in reversed(IterCodeString):
            if "sb." in i:
                possibleLines.append(i)

        loop(type, value, traceback, CodeString, num, possibleLines)
        print("Possible Lines")
        print(possibleLines)

def loop(type, value, traceback, CodeString, num, possibleLines):
    for i in range(0, 4):
        findVariable(type, value, traceback, CodeString, num, possibleLines)
    return

def findVariable(type, value, traceback, CodeString, num, possibleLines):
        for i, line in enumerate(CodeString):
            if i is num:
                if 'sb.' in i:
                    possibleLines.append(i)
                    num += -1
                    return
                else:
                    num += -1
                    findVariable(type, value, traceback, CodeString, num, possibleLines)


        print(possibleLines)


def oldIdeas():
        print(sys.stderr)
        localVars = locals()
        print("Local variables via 'locals()': ")
        print(localVars)
        tb = traceback
        cont = True
        sbCalls = []
        while cont is True:
            print(tb.tb_frame.f_locals)
            for var in tb.tb_frame.f_locals:
                if 'sb.' in tb.tb_frame.f_locals:
                    sbCalls.append()
            tb = traceback.tb_next
        print("Local variables via tb.locals():")
        print(tb)
        print('Unhandled error:', type, value, traceback)
        CodeString = inspect.getsource(traceback)
        print(CodeString)
        lasti = traceback.tb_lasti
        print("Last attempted instruction in bytecode: %s" % lasti)
        for word in reversed(CodeString):
            if "sb." in word:
                print(word)

        v1 = inspect.trace(traceback)
        print(v1)
        #for i in v1.f_locals:
        #    if "ID" in i:
        #        print(i)

        frame = traceback.tb_frame
        code = frame.f_code
        print(code)
        #v5 = inspect.getsourcelines(traceback)
        #print(v5)
        tb = traceback
        while tb.tb_next:
            tb = traceback.tb_next
        locvariables = tb.tb_frame.f_locals
        locvariables2 = traceback.tb_frame.f_locals
        print(len(locvariables2))
        for i in locvariables2:
            print(i)
        for i in locvariables:
            print(i)
        locvariables_list = []
        for key, value in locvariables.items():
            temp = [key,value]
            locvariables_list.append(temp)
        pprint(locvariables_list)
        #pprint(locvariables_list[-2])
        pprint(locvariables_list[1][1])
        #globvariables = traceback.tb_frame.f_globals
        #pprint(globvariables)

        #arg_spec = inspect.getargspec(function)
    #else:
        print('Raised %s: %s') % type, value
        print(sys.last_traceback)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(tb.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout))
