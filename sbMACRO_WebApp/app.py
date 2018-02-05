"""This module controls data, json scraping, and page rendering for sbMACRO."""

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
import gl, parse, parseFY, saveJson  # pylint: disable=E0401,C0413,C0410,C0411
import edit_gpy  # pylint: disable=E0401,C0413,C0410,C0411,W0611

SB = pysb.SbSession()


# create the application object
app = Flask(__name__)  # pylint: disable=C0103

# config
app.secret_key = 'my precious'


class JsonTransformer(object):  # pylint: disable=R0903
    """Class for transforming complicated python objects to JSON."""

    def transform(self, my_object):  # pylint: disable=R0201
        """Class Method for transforming objects to JSON."""
        return jsonpickle.encode(my_object, unpicklable=False)


def get_fiscal_years(csc_id=None):
    """Create a sorted dict of fiscal years from NWCSC and return it.

    Arguments:
        csc_id -- the sciencebase id to be parsed (default None)

    Returns:
       fiscal_years_dict_ordered -- ordered dict of ScienceBase fiscal year ids

    Raises:
        ValueError: if no argument passed to csc_id

    """
    if csc_id is None:
        print("No id passed to get_fiscal_years")
        raise ValueError
    try:
        fiscal_years = SB.get_child_ids(csc_id)
    except Exception:  # pylint: disable=W0703
        print("----------Exception Raised in get_fiscal_years (1)")
        parseFY.exceptionLoop(csc_id)
        fiscal_years = SB.get_child_ids(csc_id)
    fiscal_years_dict = {}
    for sb_id in fiscal_years:
        try:
            json_ = SB.get_item(sb_id)
        except Exception:  # pylint: disable=W0703
            print("----------Exception Raised in get_fiscal_years (2)")
            parseFY.exceptionLoop(sb_id)
            json_ = SB.get_item(sb_id)
        title = 'NWCSC '+json_['title']
        fiscal_years_dict.update({title: sb_id})
    print("Original fiscal_years_dict")
    print(fiscal_years_dict)
    sorted_dict = sorted(fiscal_years_dict)
    fiscal_years_dict_ordered = {}
    for i in sorted_dict:
        fiscal_years_dict_ordered.update({i: fiscal_years_dict[i]})
    print("Newly Ordered fiscal_years_dict: fiscal_years_dict_ordered")
    print(fiscal_years_dict_ordered)
    return fiscal_years_dict_ordered


def defined_hard_search():
    """Perform hard search on specific ids via user-input.

    The function first prompts the user for a ScienceBase id.
    Then, once done, the ids are placed into gl.items_to_be_parsed, and
    parse.main() is called to begin the hard search. This ends with new jsons
    being created and saved for whatever fiscal years were designated.
    """
    # To run this function from command line:
    # python -c 'from app import defined_hard_search; defined_hard_search()'

    gl.Excel_choice = "One_Excel_for_all_FYs"
    answer = None
    request_items = []
    while answer != 'done':
        print('Please enter an ID you would like parsed. '
              + 'When done, type \'done\'.')
        if not request_items:  # if request_items is empty (false)
            pass
        else:
            print("Currently in line:")
            print("------------------")
            for i in request_items:
                print(i)
            print("------------------")
        answer = input('sbID: ')
        if ((answer != 'done')
                and (answer != None)
                and (answer not in request_items)):
            request_items.append(answer)
    for i in request_items:
        gl.items_to_be_parsed.append(i)
    if gl.items_to_be_parsed != []:
        parse.main()  # pylint: disable=E1101
    else:
        return
    print("""

    ===========================================================================

                    Hard Search is now finished.""")


def full_hard_search():
    """Perform hard search on any ids older than 1 day.

    The function calls get_fiscal_years on all desired CSCs to get ordered
    dictionaries of each CSC's fiscal years. All fiscal year IDs are added to
    the request_items list. Then, it  parses the appropriate fiscal year's
    json file (if it exists) to see if any of those fiscal years have been
    hard search that day. If so, it removes them from the list. The list is
    used to populate gl.items_to_be_parsed before calling parse.main(). This
    ends with new jsons being created and saved for whatever fiscal years were
    designated.
    """
    # To run this function from command line:
    # python -c 'from app import full_hard_search; full_hard_search()'
    nwcsc_fys_ordered_dict = get_fiscal_years("4f8c64d2e4b0546c0c397b46")
    swcsc_fys_ordered_dict = get_fiscal_years("4f8c6580e4b0546c0c397b4e")
    # absolute path to app.py:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(script_dir)
    # Join the script path with the DataCounting directory to get to the
    # files there and insert it into the system path. Now you can import your
    # python files.
    print(os.path.join(script_dir, "DataCounting/"))
    sys.path.insert(0, os.path.join(script_dir, "DataCounting/"))
    gl.Excel_choice = "One_Excel_for_all_FYs"
    request_items = []
    request_items[:] = []
    for key, value in swcsc_fys_ordered_dict.items():
        print("{0}: {1} added to request_items from SWCSC.".format(key, value))
        request_items.append(value)
    for key, value in nwcsc_fys_ordered_dict.items():
        print("{0}: {1} added to request_items from NWCSC.".format(key, value))
        request_items.append(value)
    ids_to_be_deleted = []
    fiscal_year_folder = "./jsonCache"
    for the_file in os.listdir(fiscal_year_folder):
        file_path = os.path.join(fiscal_year_folder, the_file)
        try:
            if os.path.isfile(file_path):
                if file_path.endswith(".json"):
                    with open(file_path) as json_data:
                        data = json.load(json_data)
                        try:  # If date doesn't exist replace it.
                            data_date = data['Date']['date']
                        except KeyError:
                            continue
                        now = datetime.datetime.now()
                        current_date = now.strftime("%Y%m%d")

                        if current_date > data_date:
                            continue
                        else:
                            # uncomment 'continue' if you want to do all FYs
                            # regardless of when they were last done:
                            # continue
                            fy_id = the_file.replace(".json", "")
                            print("fy_id from today: {0}".format(fy_id))
                            # Quantico
                            ids_to_be_deleted.append(fy_id)
            else:
                print("Not a file")
        except Exception as err:  # pylint: disable=W0703
            print("Exception: " + err)
    for fy_id in ids_to_be_deleted:
        while fy_id in request_items:
            request_items.remove(fy_id)
    for i in request_items:
        gl.items_to_be_parsed.append(i)
    if gl.items_to_be_parsed != []:
        parse.main()  # pylint: disable=E1101
    if not request_items:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    elif request_items:
        full_hard_search()


@app.route('/', methods=['GET'])
def index():
    """Clear gl variables and render the index.html page."""
    edit_gpy.clear_memory()
    return(render_template('index.html',
                           **locals(),
                           title="Project Data Count"))


@app.route('/fiscalYears', methods=['GET', 'POST'])
def fiscal_years_func():
    """Clear gl variables, call get_fiscal_years, render fiscalYears.html."""
    edit_gpy.clear_memory()
    # pylint: disable=W0612
    nwcsc_fys_ordered_dict = get_fiscal_years("4f8c64d2e4b0546c0c397b46")
    swcsc_fys_ordered_dict = get_fiscal_years("4f8c6580e4b0546c0c397b4e")
    print("Now local?")

    return render_template('fiscalYears.html', **locals(), title="Home")


@app.route('/projects', methods=['GET'])
def projects():
    """Clear gl variables and render the projects.html page.

    The function clears any memory in gl.py and renders the
    projects.html page.
    """
    edit_gpy.clear_memory()
    return(render_template('projects.html',
                           **locals(),
                           title="Project Data Count"))


@app.route('/report', methods=['POST'])
def handle_data():
    """Find appropriate data in jsons or via hard search, render report.html.

    This function pulls the items to be parsed from request.form. Then it
    determines whether or not a hard search was requested. Then, using a hard
    search and/or the available jsons, the function creates the appropriate
    report dictionary (report_dict), which is transformed using jsonpickle to
    a more json-friendly object and passed to report.html which is rendered.
    """
    if request.method == 'POST':
        for i in request.form:
            print(i)
    if request.method == 'POST':
        hard_search_choice = request.form.getlist('HardSearch')
        print("HardSearch:")
        print(hard_search_choice)
        request_items = request.form.getlist('checks')
        print(request_items)
        gl.Excel_choice = request.form.get("Excel-choice")
        print(gl.Excel_choice)
    else:
        return redirect('/')
    report_dict = {}
    report_dict.clear()
    report_list = []
    report_list[:] = []
    date_list = []
    date_list[:] = []
    identity_list = []
    identity_list[:] = []
    ids_to_be_deleted = []
    # this is how we deal with projects:
    if not request_items and gl.Excel_choice is None:
        # this means its a project POST request
        report_dict = project_post_request(request, report_dict)
    elif not hard_search_choice:  # if hard_search_choice is empty
        print('hard_search_choice == []')
        for sb_id in request_items:
            fiscal_year_folder = "./jsonCache"
            for the_file in os.listdir(fiscal_year_folder):
                file_path = os.path.join(fiscal_year_folder, the_file)
                if sb_id in the_file:
                    ids_to_be_deleted.append(sb_id)
                    try:
                        if os.path.isfile(file_path):
                            if file_path.endswith(".json"):
                                with open(file_path) as json_data:
                                    data = json.load(json_data)
                                    # print(data)
                                    report_list.append(data['report'])
                                    date_list.append(data['Date'])
                                    # maybe add more things to report_dict???
                                    # Or Identity?
                                    identity_list.append(data['identity'])
                    except Exception as err:  # pylint: disable=W0703
                        print("Exception " + err)
        report_dict['report'] = report_list
        report_dict['date'] = date_list
        report_dict['identity'] = identity_list
    for sb_id in ids_to_be_deleted:
        while sb_id in request_items:
            request_items.remove(sb_id)
    if hard_search_choice == ['on'] or request_items != []:
        if hard_search_choice == ['on']:
            print('hard_search_choice == [\'on\']')
        elif request_items != []:
            print('request_items != []')
            print('request_items = :')
            for i in request_items:
                print("-- {0}".format(i))
        else:
            print('Something else caused quick search to not work.')
        if request_items != [] and hard_search_choice == ['on']:
            print('IN ADDITION: request_items != []')

        for i in request_items:
            gl.items_to_be_parsed.append(i)
        parse.main()  # pylint: disable=E1101
        report_dict = saveJson.main()

    #now we need to add all project-specific info for modals to report_dict
    project_dict = create_project_list(report_dict)

    report_dict['projects'] = project_dict


    full_report_json = JsonTransformer()
    full_report_json = JsonTransformer.transform(full_report_json, report_dict)
    # need to get the name of whatever the report was created for...
    # sb_id = gl.current_item #THIS IS NOT FINISHED

    print(full_report_json)
    print("full_report_json")
    return render_template('report.html', full_report_json=full_report_json)

def project_post_request(request_, report_dict):
    """Use local jsons to populate report_dict and returns it.

    Creates several lists and dictionaries, and, using the requests form to
    determine which projects to look for, it parses the project jsons and adds
    the appropriate info to report_dict and returns it.

    Arguments:
        request -- the request passed to handle_data() from flask
        report_dict -- the dictionary being formed by the function
    """
    report_list = []
    report_list[:] = []
    date_list = []
    date_list[:] = []
    identity_list = []
    identity_list[:] = []
    ids_to_be_deleted = []
    sb_urls = request_.form.getlist("SBurls")
    print("sb_urls")
    print(sb_urls)
    request_items = []
    for i in sb_urls:
        try:
            json1 = SB.get_json(i)
            item_id = json1['id']
            if item_id not in request_items:
                request_items.append(item_id)
        except Exception:  # pylint: disable=W0703
            print("Invalid URL")
    for sb_id in request_items:
        fiscal_year_folder = "./jsonCache"
        for the_file in os.listdir(fiscal_year_folder):
            file_path = os.path.join(fiscal_year_folder, the_file)
            try:
                if os.path.isfile(file_path):
                    if file_path.endswith(".json"):
                        with open(file_path) as json_data:
                            data = json.load(json_data)
                            for i in data['report']:
                                if i['ID'] == sb_id:
                                    ids_to_be_deleted.append(sb_id)
                                    matched_project = i
                                    # print("matched_project")
                                    # print(matched_project)
                                    matched_project_list = []
                                    matched_project_list.append(
                                        matched_project)
                                    report_list.append(matched_project_list)
                                    date_list.append(data['Date'])
                                    identity_list.append(data['identity'])
                                    # ^this may be wrong
            except Exception as err:  # pylint: disable=W0703
                print("Exception :" + err)
    report_dict['report'] = report_list
    report_dict['date'] = date_list
    report_dict['identity'] = identity_list
    return report_dict

def create_project_list(report_dict):
    """Create and return a dictionary of project data.

    Using the fiscal years it finds in report_dict, this
    function parses the Project Jsons to collect project
    data and include that data in a dictionary before returning
    that dictionary.

    Arguments:
        report_dict -- dictionary containing pertinent fiscal years
    Returns:
        project_dict -- dictionary containing project information for the
                        projects in the fiscal years in report_dict
    """
    project_dict = {}
    for year in report_dict['report']:
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
    """Render report.html page.

    The function takes formats report_dict and passes it to report.html.
    """
    report_dict = saveJson.main()
    full_report_json = JsonTransformer()
    full_report_json = JsonTransformer.transform(full_report_json, report_dict)
    print("full_report_json: ")  # Quantico
    pprint(full_report_json)  # Quantico

    return render_template('report.html', full_report_json=full_report_json)




# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True)
