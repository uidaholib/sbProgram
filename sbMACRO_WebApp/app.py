"""This module controls data, json scraping, and page rendering for sbMACRO"""

# import the Flask class from the flask module
import sys
import os
from pprint import pprint
# from functools import wraps
import json
# import subprocess
import datetime
import pysb  # pylint: disable=wrong-import-order
from flask import Flask, render_template  # pylint: disable=E0401
from flask import redirect, request  # pylint: disable=E0401
#from flask import flash, session, url_for
import jsonpickle  # pylint: disable=E0401

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "DataCounting/"))
import gl, parse, parseFY, saveJson  # pylint: disable=E0401,C0413,C0410

SB = pysb.SbSession()


# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'


class JsonTransformer(object):
    def transform(self, myObject):
        return jsonpickle.encode(myObject, unpicklable=False)

def get_FYs(CSC_id=None):
    """Create a sorted dict of fiscal years from NWCSC and return it.
    
    Arguments:
        CSC_id -- the sciencebase id to be parsed (default None)
    """
    if CSC_id == None:
        print("No id passed to get_FYs")
        return
    try:
        FYs = SB.get_child_ids(CSC_id)
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in get_FYs (1)")
        parseFY.exceptionLoop("4f8c64d2e4b0546c0c397b46")
        FYs = SB.get_child_ids("4f8c64d2e4b0546c0c397b46")

    FYs_Dict = {}
    for ID in FYs:
        try:
            json_ = SB.get_item(ID)
        except Exception:  # pylint: disable=W0703
            print("----------Exception Raised in get_FYs (2)")
            parseFY.exceptionLoop(ID)
            json_ = SB.get_item(ID)

        title = 'NWCSC '+json_['title']

        FYs_Dict.update({title: ID})
    print("Original FYs_Dict")
    print(FYs_Dict)
    sortNW = sorted(FYs_Dict)
    FYs_OrderedDict = {}
    for i in sortNW:
        FYs_OrderedDict.update({i: FYs_Dict[i]})
    print("Newly Order FYs_Dict: FYs_OrderedDict")
    print(FYs_OrderedDict)
    return FYs_OrderedDict


def defined_hard_search():
    # To run this function from command line:
    # python -c 'from app import defined_hard_search; defined_hard_search()'

    # absolute path to this file:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # join the script path with the DataCounting directory to get to the files
    # there and insert it into the system path.
    # Now you can import your python files.
    sys.path.insert(0, os.path.join(script_dir, "DataCounting/"))
    gl.Excel_choice = "One_Excel_for_all_FYs"
    answer = None
    requestItems = []
    while answer != 'done':
        print('Please enter an ID you would like parsed. '
              + 'When done, type \'done\'.')
        if len(requestItems) == 0:
            pass
        else:
            print("Currently in line:")
            print("------------------")
            for i in requestItems:
                print(i)
            print("------------------")
        answer = input('sbID: ')
        if ((answer != 'done')
                and (answer != None)
                and (answer not in requestItems)):
            requestItems.append(answer)
    for i in requestItems:
        gl.itemsToBeParsed.append(i)
    if gl.itemsToBeParsed != []:
        parse.main()  # pylint: disable=E1101
    else:
        return
    print("""

    ===========================================================================

                    Hard Search is now finished.""")


def full_hard_search():
    # To run this function from command line:
    # python -c 'from app import full_hard_search; full_hard_search()'
    NWCSC_FYs_OrderedDict = get_FYs("4f8c64d2e4b0546c0c397b46")
    SWCSC_FYs_OrderedDict = get_FYs("4f8c6580e4b0546c0c397b4e")
    # absolute path to app.py:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(script_dir)
    # Join the script path with the DataCounting directory to get to the
    # files there and insert it into the system path. Now you can import your
    # python files.
    print(os.path.join(script_dir, "DataCounting/"))
    sys.path.insert(0, os.path.join(script_dir, "DataCounting/"))
    gl.Excel_choice = "One_Excel_for_all_FYs"
    requestItems = []
    for key, value in SWCSC_FYs_OrderedDict.items():
        print("{0}: {1} added to requestItems from SWCSC.".format(key, value))
        requestItems.append(value)
    for key, value in NWCSC_FYs_OrderedDict.items():
        print("{0}: {1} added to requestItems from NWCSC.".format(key, value))
        requestItems.append(value)
    IDsToBeDeleted = []
    fyFolder = "./jsonCache"
    for the_file in os.listdir(fyFolder):
        filePath = os.path.join(fyFolder, the_file)
        try:
            if os.path.isfile(filePath):
                if filePath.endswith(".json"):
                    with open(filePath) as json_data:
                        data = json.load(json_data)
                        try:  # If date doesn't exist replace it.
                            dataDate = data['Date']['date']
                        except KeyError:
                            continue
                        now = datetime.datetime.now()
                        currentDate = now.strftime("%Y%m%d")

                        if currentDate > dataDate:
                            continue
                        else:
                            # uncomment 'continue' if you want to do all FYs 
                            # regardless of when they were last done:
                            # continue
                            ID = the_file.replace(".json", "")
                            print("ID from today: {0}".format(ID))  # Quantico
                            IDsToBeDeleted.append(ID)
            else:
                print("Not a file")
        except Exception as e:  # pylint: disable=W0703
            print("Exception: " + e)
    for ID in IDsToBeDeleted:
        while ID in requestItems:
            requestItems.remove(ID)
    for i in requestItems:
        gl.itemsToBeParsed.append(i)
    if gl.itemsToBeParsed != []:
        parse.main()  # pylint: disable=E1101
    if len(requestItems) == 0:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    elif len(requestItems) != 0:
        full_hard_search()
    # report_dict = saveJson.main()
    # full_report_json = JsonTransformer()
    # full_report_json = JsonTransformer.transform(full_report_json, report_dict)


@app.route('/', methods=['GET'])
def index():
    sys.path.insert(0, './DataCounting')
    import editGPY  # pylint: disable=E0401
    editGPY.clearMemory()
    return(render_template('index.html',
           **locals(),  # pylint: disable=
           title="Project Data Count"))


@app.route('/fiscalYears', methods=['GET', 'POST'])
def fiscal_years_func():
    sys.path.insert(0, './DataCounting')
    import editGPY  # pylint: disable=E0401
    editGPY.clearMemory()
    NWCSC_FYs_OrderedDict = get_FYs("4f8c64d2e4b0546c0c397b46")
    SWCSC_FYs_OrderedDict = get_FYs("4f8c6580e4b0546c0c397b4e")  # pylint disable=W0612
    print("Now local?")

    return render_template('fiscalYears.html', **locals(), title="Home")


@app.route('/projects', methods=['GET'])
def projects():
    """Render projects.html page
    
    The function clears any memory in gl.py and renders the
    projects.html page"""
    sys.path.insert(0, './DataCounting')
    import editGPY  # pylint: disable=E0401
    editGPY.clearMemory()
    return(render_template('projects.html',
           **locals(),
           title="Project Data Count"))


@app.route('/report', methods=['POST'])
def handle_data():
    sys.path.insert(0, './DataCounting')
    if request.method == 'POST':
        for i in request.form:
            print(i)
    if request.method == 'POST':
        hardSearch = request.form.getlist('HardSearch')
        print("HardSearch:")
        print(hardSearch)
        requestItems = request.form.getlist('checks')
        print(requestItems)
        gl.Excel_choice = request.form.get("Excel-choice")
        print(gl.Excel_choice)
        fromFY = request.form.get("submitFY")
        print("fromFY")
        print(fromFY)
    else:
        return redirect('/')
    report_dict = {}
    report_dict.clear()
    reportList = []
    reportList[:] = []
    dateList = []
    dateList[:] = []
    identityList = []
    identityList[:] = []
    IDsToBeDeleted = []
    # this is how we deal with projects:
    if requestItems == [] and gl.Excel_choice == None:
        # this means its a project POST request
        report_dict = project_post_request(request, report_dict)
    elif hardSearch == []:
        print('hardSearch == []')
        for ID in requestItems:
            fyFolder = "./jsonCache"
            for the_file in os.listdir(fyFolder):
                filePath = os.path.join(fyFolder, the_file)
                if ID in the_file:
                    IDsToBeDeleted.append(ID)
                    try:
                        if os.path.isfile(filePath):
                            if filePath.endswith(".json"):
                                with open(filePath) as json_data:
                                    data = json.load(json_data)
                                    # print(data)
                                    reportList.append(data['report'])
                                    dateList.append(data['Date'])
                                    # maybe add more things to report_dict???
                                    # Or Identity?
                                    identityList.append(data['identity'])
                    except Exception as e:  # pylint: disable=W0703
                        print("Exception " + e)
        report_dict['report'] = reportList
        report_dict['date'] = dateList
        report_dict['identity'] = identityList
    for ID in IDsToBeDeleted:
        while ID in requestItems:
            requestItems.remove(ID)
        """For each ID in request items
            if json of that name exists
                report_dict['report'] += content of that json report
                report_dict['date'] += date of that json report
                remove that item from requestItems"""
    if hardSearch == ['on'] or requestItems != []:
        if hardSearch == ['on']:
            print('hardSearch == [\'on\']')
        elif requestItems != []:
            print('requestItems != []')
            print('requestItems = :')
            for i in requestItems:
                print("-- {0}".format(i))
        else:
            print('Something else caused quick search to not work.')
        if requestItems != [] and hardSearch == ['on']:
            print('IN ADDITION: requestItems != []')

        for i in requestItems:
            gl.itemsToBeParsed.append(i)
        #  Need parse.main() to return report_dict of everything from saveJson.py, jasontransform it, and pass that to report.html.
        parse.main()  # pylint: disable=E1101
        report_dict = saveJson.main()

    #now we need to add all project-specific info for modals to report_dict
    project_dict = create_project_list(report_dict)

    report_dict['projects'] = project_dict


    full_report_json = JsonTransformer()
    full_report_json = JsonTransformer.transform(full_report_json, report_dict)
    # need to get the name of whatever the report was created for...
    # ID = gl.Current_Item #THIS IS NOT FINISHED

    print(full_report_json)
    print("full_report_json")
    return render_template('report.html', full_report_json=full_report_json)

def project_post_request(request_, report_dict):
    """Uses local jsons to populate report_dict and returns it

    Creates several lists and dictionaries, and, using the requests form to
    determine which projects to look for, it parses the project jsons and adds
    the appropriate info to report_dict and returns it.

    Arguments:
        request -- the request passed to handle_data() from flask
        report_dict -- the dictionary being formed by the function
    """
    reportList = []
    reportList[:] = []
    dateList = []
    dateList[:] = []
    identityList = []
    identityList[:] = []
    IDsToBeDeleted = []
    sb_urls = request_.form.getlist("SBurls")
    print("sb_urls")
    print(sb_urls)
    requestItems = []
    for i in sb_urls:
        try:
            json1 = SB.get_json(i)
            item_id = json1['id']
            if item_id not in requestItems:
                requestItems.append(item_id)
        except:
            print("Invalid URL")
    for ID in requestItems:
        fyFolder = "./jsonCache"
        for the_file in os.listdir(fyFolder):
            filePath = os.path.join(fyFolder, the_file)
            try:
                if os.path.isfile(filePath):
                    if filePath.endswith(".json"):
                        with open(filePath) as json_data:
                            data = json.load(json_data)
                            for i in data['report']:
                                if i['ID'] == ID:
                                    IDsToBeDeleted.append(ID)
                                    matchedProject = i
                                    # print("matchedProject")
                                    # print(matchedProject)
                                    matchedProjectArr = []
                                    matchedProjectArr.append(
                                                        matchedProject)
                                    reportList.append(matchedProjectArr)
                                    dateList.append(data['Date'])
                                    identityList.append(data['identity'])
                                    # ^this may be wrong
            except Exception as e:
                print("Exception :" + e)
    report_dict['report'] = reportList
    report_dict['date'] = dateList
    report_dict['identity'] = identityList
    return report_dict

def create_project_list(report_dict):
    """Create and return a dictionary of project data
    
    Using the fiscal years it finds in report_dict, this
    function parses the Project Jsons to collect project
    data and include that data in a dictionary before returning
    that dictionary.

    Arguments:
        report_dict -- dictionary containing pertinent fiscal years
    """
    project_dict = {}
    for year in report_dict['report']:  # pylint: disable=too-many-nested-blocks
        for proj in year:
            project_id = proj['ID']
            project_folder = './jsonCache/Projects'
            for the_file in os.listdir(project_folder):
                file_path = os.path.join(project_folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        if file_path.endswith(project_id + ".json"):
                            project_json_ = json.load(open(file_path))
                            project_dict[project_id] = project_json_
                except Exception as err:  # pylint: disable=broad-except
                    print("Error: " + err)
    return project_dict


@app.route('/download_log', methods=['GET'])
def download_log():
    """Render report.html page
    
    The function takes formats report_dict and passes it to report.html"""
    sys.path.insert(0, './DataCounting')
    report_dict = saveJson.main()
    full_report_json = JsonTransformer()
    full_report_json = JsonTransformer.transform(full_report_json, report_dict)
    print("full_report_json: ")  # Quantico
    pprint(full_report_json)  # Quantico

    return(render_template('report.html', full_report_json=full_report_json))




# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)
