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
        title = json['title']
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
        title = json['title']
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


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    NWCSC_FYs_OrderedDict = get_NW_FYs()
    SWCSC_FYs_OrderedDict = get_SW_FYs()
    print("Now local?")
    print(NWCSC_FYs_OrderedDict)
    print(SWCSC_FYs_OrderedDict)

    return(render_template('index.html', **locals(), title="Home"))


@app.route('/count-data', methods=['POST'])
def handle_data():

    import sys
    sys.path.insert(0, '/Users/taylorrogers/Documents/#Coding/sbProgram/TrialWebApp/DataCounting')  #eyekeeper: THIS WILL NEED CHANGED WHEN IT GOES ELSEWHERE
    # Dev Windows path: C:/Users/Taylor/Documents/!USGS/Python/sbProgramGitRepo/TrialWebApp/DataCounting
    # Dev MacOS path: /Users/taylorrogers/Documents/#Coding/sbProgram/TrialWebApp/DataCounting
    import gl, parse, countData_proj, ExcelPrint
    if request.method == 'POST':
        # flash("Method was POST!")
        for i in request.form:
            print(i)
            # flash(i)
    if request.method == 'POST':
        test = request.form.getlist('checks')
        print(test)
        # flash(test)
        gl.Excel_choice = request.form.get("Excel-choice")
        # flash(gl.Excel_choice)
        print(gl.Excel_choice)
    else:
        return(redirect('/'))

    for i in test:
        gl.itemsToBeParsed.append(i)
    #  Need parse.main() to return reportDict of everything from ExcelPrint.py, jasontransform it, and pass that to download.html.
    parse.main()
    reportDict = ExcelPrint.main()
    FullReportJson = JsonTransformer()
    FullReportJson = JsonTransformer.transform(FullReportJson, reportDict)
    print("FullReportJson: ")  # Quantico
    pprint(FullReportJson)  # Quantico

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
    # for Windows:
    # sys.path.insert(0, 'C:/Users/Taylor/Documents/!USGS/Python/sbProgramGitRepo/TrialWebApp/DataCounting')  #eyekeeper: THIS WILL NEED CHANGED WHEN IT GOES ELSEWHERE
    # For Mac:
    sys.path.insert(0, '/Users/taylorrogers/Documents/#Coding/sbProgram/TrialWebApp/DataCounting')  #eyekeeper: THIS WILL NEED CHANGED WHEN IT GOES ELSEWHERE
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
