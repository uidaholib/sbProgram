# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify
from functools import wraps
from flask import g as g1
import g
from pprint import pprint
import json
import requests
import pysb


#sb = pysb.SbSession()


# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    NWCSC_FYs_OrderedDict = get_NW_FYs()
    SWCSC_FYs_OrderedDict = get_SW_FYs()
    print("Now local?")
    print(NWCSC_FYs_OrderedDict)
    print(SWCSC_FYs_OrderedDict)

    return(render_template('index.html', **locals(), title="Home"))

def get_NW_FYs():
    NWCSC_FYs_OrderedDict = {}
    SWCSC_FYs_OrderedDict = {}
    # NWCSC_FYs = sb.get_child_ids("4f8c64d2e4b0546c0c397b46")
    NWCSC_FYs = ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8"]  # Delete later
    #print(NWCSC_FYs)
    NWCSC_FYs_Dict = {}
    TitleNum = 2018  # Delete later
    for ID in NWCSC_FYs:
        # json = sb.get_item(ID)
        #title = json['title']
        title = "Fiscal Year "+str(TitleNum)  # Delete later
        TitleNum -= 1  # Delete later

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
    flash(NWCSC_FYs_OrderedDict)
    return(NWCSC_FYs_OrderedDict)



def get_SW_FYs():
    # SWCSC_FYs = sb.get_child_ids("4f8c6580e4b0546c0c397b4e")
    SWCSC_FYs = ["ID1", "ID2", "ID3", "ID4", "ID5", "ID6", "ID7", "ID8"]  # Delete later

    #print(SWCSC_FYs)
    SWCSC_FYs_Dict = {}
    TitleNum = 2018  # Delete later
    for ID in SWCSC_FYs:
        # json = sb.get_item(ID)
        # title = json['title']
        title = "Fiscal Year "+str(TitleNum)  # Delete later
        TitleNum -= 1  # Delete later
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
    flash(SWCSC_FYs_OrderedDict)
    return(SWCSC_FYs_OrderedDict)



@app.route('/differentThing', methods=['POST'])
def differentThing():
    if request.method == 'POST':
        for i in request.form:
            print(i)
            flash(i)
        if request.form['NWFY2011']:
            print(request.form['NWFY2011'])
            flash(request.form['NWFY2011'])
            error = 'Invalid Credentials. Please try again.'
    return(render_template('index.html'))

@app.route('/count_data', methods=['POST'])
def handle_data():
    if request.method == 'POST':
        for i in request.form:
            print(i)
            flash(i)
    if request.method == 'POST':
        test = request.form.getlist('FY-Select')
        print(test)
        return(redirect('/'))
    else:
        return(redirect('/'))
    return(render_template('count-data.html'))
    #your code

# use decorators to link the function to a url
@app.route('/getChildren', methods=['GET', 'POST'])
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


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
