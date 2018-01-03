# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify
from functools import wraps
from flask import g as g1
from pprint import pprint
import json
import requests
import pysb
import subprocess
import jsonpickle
import sys
import os
import datetime


sb = pysb.SbSession()


# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'


class JsonTransformer(object):
    def transform(self, myObject):
        return jsonpickle.encode(myObject, unpicklable=False)

def get_NW_FYs():
    NWCSC_FYs_OrderedDict = {}
    SWCSC_FYs_OrderedDict = {}
    NWCSC_FYs = sb.get_child_ids("4f8c64d2e4b0546c0c397b46")
    # NWCSC_FYs = ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8"]  # Delete later
    #print(NWCSC_FYs)
    NWCSC_FYs_Dict = {}
    # TitleNum = 2018  # Delete later
    for ID in NWCSC_FYs:
        json = sb.get_item(ID)
        title = 'NWCSC '+json['title']
        # title = "Fiscal Year "+str(TitleNum)  # Delete later
        # TitleNum -= 1  # Delete later

        NWCSC_FYs_Dict.update({title: ID})
    print("Original NWCSC_FYs_Dict")
    print(NWCSC_FYs_Dict)
    sortNW = sorted(NWCSC_FYs_Dict)
    #print(sort)
    NWCSC_FYs_OrderedDict = {}
    for i in sortNW:
        NWCSC_FYs_OrderedDict.update({i: NWCSC_FYs_Dict[i]})
    print("Newly Order NWCSC_FYs_Dict: NWCSC_FYs_OrderedDict")
    print(NWCSC_FYs_OrderedDict)
    # flash(NWCSC_FYs_OrderedDict)
    return(NWCSC_FYs_OrderedDict)



def get_SW_FYs():
    SWCSC_FYs = sb.get_child_ids("4f8c6580e4b0546c0c397b4e")
    # SWCSC_FYs = ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8"]  # Delete later

    #print(SWCSC_FYs)
    SWCSC_FYs_Dict = {}
    # TitleNum = 2018  # Delete later
    for ID in SWCSC_FYs:
        json = sb.get_item(ID)
        title = 'SWCSC '+json['title']
        # title = "Fiscal Year "+str(TitleNum)  # Delete later
        # TitleNum -= 1  # Delete later
        SWCSC_FYs_Dict.update({title: ID})
    print("Original SWCSC_FYs")
    print(SWCSC_FYs_Dict)
    sortSW = sorted(SWCSC_FYs_Dict)
    #print(sort)
    SWCSC_FYs_OrderedDict = {}
    for i in sortSW:
        SWCSC_FYs_OrderedDict.update({i: SWCSC_FYs_Dict[i]})
    print("Newly Order SWCSC_FYs_Dict: SWCSC_FYs_OrderedDict")
    print(SWCSC_FYs_OrderedDict)
    # flash(SWCSC_FYs_OrderedDict)
    return(SWCSC_FYs_OrderedDict)

def defined_hard_search():
    # To run this function from command line: python -c 'from app import defined_hard_search; defined_hard_search()'
    
    import sys
    sys.path.insert(0, './DataCounting')
    import gl
    import parse
    gl.Excel_choice = "One_Excel_for_all_FYs"
    answer = None
    requestItems = []
    while answer != 'done':
        print('Please enter an ID you would like parsed. When done, type \'done\'.')
        answer = input('sbID: ')
        if answer != 'done' and answer != None:
            requestItems.append(answer)
    for i in requestItems:
        gl.itemsToBeParsed.append(i)
        #  Need parse.main() to return reportDict of everything from ExcelPrint.py, jasontransform it, and pass that to download.html.
    if gl.itemsToBeParsed != []:
        parse.main()
    else:
        return
    print("""
    
    ===========================================================================
    
                    Hard Search is now finished.""")
            


def full_hard_search():
    # To run this function from command line: python -c 'from app import full_hard_search; full_hard_search()'
    NWCSC_FYs_OrderedDict = get_NW_FYs()
    SWCSC_FYs_OrderedDict = get_SW_FYs()
    import sys
    # eyekeeper: THIS WILL NEED CHANGED WHEN IT GOES ELSEWHERE
    sys.path.insert(0, './DataCounting')
    # Dev Windows path: C:/Users/Taylor/Documents/!USGS/Python/sbProgramGitRepo/TrialWebApp/DataCounting
    # Dev MacOS path: /Users/taylorrogers/Documents/#Coding/sbProgram/TrialWebApp/DataCounting
    import gl
    import parse
    import countData_proj
    import ExcelPrint
    gl.Excel_choice = "One_Excel_for_all_FYs"
    requestItems = []
    for key, value in SWCSC_FYs_OrderedDict.items():
        print("{0}: {1} added to requestItems from SWCSC.".format(key, value))
        requestItems.append(value)
    for key, value in NWCSC_FYs_OrderedDict.items():
        print("{0}: {1} added to requestItems from NWCSC.".format(key, value))
        requestItems.append(value)
    IDsToBeDeleted = []
    for root, dirs, files in os.walk("./jsonCache"):
                for filename in files:  # this looks at each file's name for each item
                    filePath = "./jsonCache/" + filename
                    print(filePath)  # Quantico
                    if filename.endswith(".json"):
                        with open(filePath) as json_data:
                            data = json.load(json_data)
                            try:    # If, for some reason, date doesn't exist, replace it.
                                dataDate = data['Date']['date']
                            except KeyError:
                                continue
                            now = datetime.datetime.now()
                            currentDate = now.strftime("%Y%m%d")
                            if currentDate > dataDate:
                                continue
                            else:
                                ID = filename.replace(".json", "")
                                print("ID from today: {0}".format(ID))  # Quantico
                                IDsToBeDeleted.append(ID)
    for ID in IDsToBeDeleted:
        while ID in requestItems:
            requestItems.remove(ID)
                                
    for i in requestItems:
        gl.itemsToBeParsed.append(i)
        #  Need parse.main() to return reportDict of everything from ExcelPrint.py, jasontransform it, and pass that to download.html.
    if gl.itemsToBeParsed != []:
        parse.main()
    if len(requestItems) == 0:
        print("""
    
    ===========================================================================
    
                    Hard Search is now finished.""")
        exit(0)
    elif len(requestItems) != 0:
        full_hard_search()
    # reportDict = ExcelPrint.main()
    # FullReportJson = JsonTransformer()
    # FullReportJson = JsonTransformer.transform(FullReportJson, reportDict)


@app.route('/', methods=['GET'])
def index():
    sys.path.insert(0, './DataCounting')
    import editGPY
    editGPY.clearMemory()
    error = None
    return(render_template('index.html', **locals(), title="Project Data Count"))


@app.route('/fiscalYears', methods=['GET', 'POST'])
def fiscalYearsF():
    sys.path.insert(0, './DataCounting')
    import editGPY
    editGPY.clearMemory()
    error = None
    NWCSC_FYs_OrderedDict = get_NW_FYs()
    SWCSC_FYs_OrderedDict = get_SW_FYs()
    print("Now local?")
    print(NWCSC_FYs_OrderedDict)
    print(SWCSC_FYs_OrderedDict)

    return(render_template('fiscalYears.html', **locals(), title="Home"))


@app.route('/projects', methods=['GET'])
def projects():
    sys.path.insert(0, './DataCounting')
    import editGPY
    editGPY.clearMemory()
    error = None
    return(render_template('projects.html', **locals(), title="Project Data Count"))


@app.route('/handle_data', methods=['POST'])
def handle_data():

    import sys
    sys.path.insert(0, './DataCounting')  #eyekeeper: THIS WILL NEED CHANGED WHEN IT GOES ELSEWHERE
    # Dev Windows path: C:/Users/Taylor/Documents/!USGS/Python/sbProgramGitRepo/TrialWebApp/DataCounting
    # Dev MacOS path: /Users/taylorrogers/Documents/#Coding/sbProgram/TrialWebApp/DataCounting
    import gl, parse, countData_proj, ExcelPrint

    if request.method == 'POST':
        # flash("Method was POST!")
        for i in request.form:
            print(i)
            # flash(i)
    if request.method == 'POST':
        hardSearch = request.form.getlist('HardSearch')
        print("HardSearch:")
        print(hardSearch)
        requestItems = request.form.getlist('checks')
        print(requestItems)
        # flash(requestItems)
        gl.Excel_choice = request.form.get("Excel-choice")
        # flash(gl.Excel_choice)
        print(gl.Excel_choice)
        fromFY = request.form.get("submitFY")
        print("fromFY")
        print(fromFY)
    else:
        return(redirect('/'))
    reportDict = {}
    reportDict.clear()
    reportList = []
    reportList[:] = []
    dateList = []
    dateList[:] = []
    identityList = []
    identityList[:] = []
    IDsToBeDeleted = []
    # this is how we deal with projects:
    if requestItems == [] and gl.Excel_choice == None:  # this means its a project POST request
        sb_urls = request.form.getlist("SBurls")
        print("sb_urls")
        print(sb_urls)
        requestItems = []
        for i in sb_urls:
            try:
                json1 = sb.get_json(i)
                # pprint(json)
                item_id = json1['id']
                if item_id not in requestItems:
                    requestItems.append(item_id)
            except:
                print("Invalid URL")
        for ID in requestItems:
            for root, dirs, files in os.walk("./jsonCache"):
                for filename in files:  # this looks at each file's name for each item
                    filePath = "./jsonCache/" + filename
                    if filename.endswith(".json"):
                        with open(filePath) as json_data:
                            data = json.load(json_data)
                            for i in data['report']:
                                if i['ID'] == ID:
                                    IDsToBeDeleted.append(ID)
                                    matchedProject = i
                                    print("matchedProject")
                                    print(matchedProject)
                                    matchedProjectArr = []
                                    matchedProjectArr.append(matchedProject)
                                    reportList.append(matchedProjectArr)
                                    dateList.append(data['Date'])
                                    identityList.append(data['identity'])  #this may be wrong
        reportDict['report'] = reportList
        reportDict['date'] = dateList
        reportDict['identity'] = identityList
    elif hardSearch == []:
        print('hardSearch == []')
        for ID in requestItems:
            for root, dirs, files in os.walk("./jsonCache"):
                for filename in files:  # this looks at each file's name for each item
                    if ID in filename:
                        IDsToBeDeleted.append(ID)
                        filePath = "./jsonCache/"+filename
                        with open(filePath) as json_data:
                            data = json.load(json_data)
                            print(data)
                            reportList.append(data['report'])
                            dateList.append(data['Date'])  # maybe add more things to reportDict??? Identity?
                            identityList.append(data['identity'])
        reportDict['report'] = reportList
        reportDict['date'] = dateList
        reportDict['identity'] = identityList
    for ID in IDsToBeDeleted:
        while ID in requestItems:
            requestItems.remove(ID)
        """For each ID in request items
            if json of that name exists
                reportDict['report'] += content of that json report
                reportDict['date'] += date of that json report
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
        #  Need parse.main() to return reportDict of everything from ExcelPrint.py, jasontransform it, and pass that to download.html.
        parse.main()
        reportDict = ExcelPrint.main()
    FullReportJson = JsonTransformer()
    FullReportJson = JsonTransformer.transform(FullReportJson, reportDict)
    #need to get the name of whatever the report was created for...
    # ID = gl.Current_Item #THIS IS NOT FINISHED

    # with open('{0}.json'.format(ID), 'w') as outfile:
    #     json.dump(FullReportJson, outfile)
    # print("FullReportJson: ")  # Quantico
    # pprint(FullReportJson)  # Quantico

    return(render_template('download.html', FullReportJson=FullReportJson))
    #your code

def getChildren():
    error = None
    if request.method == 'POST':
        flash(request.form['sb_id'])
        print(request.form['sb_id'])
        ID = request.form['sb_id']
        children = sb.get_child_ids(ID)
        print(children)
        flash(children)

    return(render_template('getChildren.html', error=error))

@app.route('/download_log', methods=['GET'])
def download_log():

    import sys
    sys.path.insert(0, './DataCounting')  #eyekeeper: THIS WILL NEED CHANGED WHEN IT GOES ELSEWHERE
    import gl, parse, countData_proj, ExcelPrint
    reportDict = ExcelPrint.main()
    FullReportJson = JsonTransformer()
    FullReportJson = JsonTransformer.transform(FullReportJson, reportDict)
    print("FullReportJson: ")  # Quantico
    pprint(FullReportJson)  # Quantico

    
    #print(report)

    return(render_template('download.html', FullReportJson=FullReportJson))


# return(render_template('download.html', reportDict=json.dumps(reportDict)))


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)
