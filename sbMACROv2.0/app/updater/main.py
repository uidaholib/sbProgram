"""Main module from which all Science Base data gathering branches."""
import os
import time
import pickle
import sciencebasepy
import app.updater.gl
from datetime import datetime
from app.updater import db_save
from app.updater import projects
from app.updater import fiscal_years

file_path = os.getcwd() + '/app/main/templates/static/'

def load_details_from_file(file_location):

    details = [] # a list of dicts

    try:
        with open(file_location, 'rb') as details_file:
            details = pickle.load(details_file)
    except Exception as e:
        print('error: ' + str(e))

    return details

def refresh_master_tables(app, source):

    # load or collect details
    if source == 'file':
        items_file_path = file_path + 'master_details_full.pkl'
        projs_file_path = file_path + 'proj_details.pkl'
        item_details = load_details_from_file(items_file_path)
        proj_details = load_details_from_file(projs_file_path)
    elif source == 'sciencebase':
        item_details, proj_details = get_details_from_source()

    # write details to database
    db_save.save_master_details(app, item_details)
    db_save.save_project_details(app, proj_details)

def get_details_from_source():

    print('Collecting details...')

    casc_ids = {
        'Alaska':        '4f831626e4b0e84f6086809b',
        'National':      '5050cb0ee4b0be20bb30eac0',
        'North Central': '4f83509de4b0e84f60868124',
        'Northeast':     '4f8c648de4b0546c0c397b43',
        'Northwest':     '4f8c64d2e4b0546c0c397b46',
        'Pacific':       '4f8c650ae4b0546c0c397b48',
        'South Central': '4f8c652fe4b0546c0c397b4a',
        'Southeast':     '4f8c6557e4b0546c0c397b4c',
        'Southwest':     '4f8c6580e4b0546c0c397b4e'
    }

    item_details_list = []
    proj_details_list = []

    start = time.time()
    total_items = process_casc_ids(casc_ids, proj_details_list, item_details_list)
    end = time.time()

    duration = end - start
    mins = int(duration/60)
    secs = duration % 60

    print('\n{} total items collected in {} minutes and {} seconds'.format(total_items, mins, secs))

    return item_details_list, proj_details_list

def process_casc_ids(casc_ids, proj_details_list, item_details_list):
    
    total_items = 0
    for casc in casc_ids:
        num_items = 0
        casc_id = casc_ids[casc]
        casc += ' CASC'
        fy_ids = sb.get_child_ids(casc_id)
        num_items = process_proj_ids(casc, fy_ids, proj_details_list, item_details_list)
        total_items += num_items
        print('\n========={} itmes=========\n'.format(num_items))

    return total_items

def process_proj_ids(casc, fy_ids, proj_details_list, item_details_list):

    num_items = 0
    print(casc + ':')
    for fy_id in fy_ids:
        time.sleep(2) # to ease pressure on sciencebase servers
        fy_json = sb.get_item(fy_id)
        fy = fy_json['title'].split()[1]
        if fy.isnumeric():
            proj_ids = sb.get_child_ids(fy_id)
            num_items += process_approved_ids(casc, fy, proj_ids, proj_details_list, item_details_list)

    return num_items

def process_approved_ids(casc, fy, proj_ids, proj_details_list, item_details_list):

    num_items = 0
    print(str(fy), end = '') # fiscal year is being processed
    for proj_id in proj_ids:
        #-----build project details-----
        approved_dataset_items = []
        proj_details = {}
        
        proj_details['id'] = proj_id
        proj_details['casc'] = casc
        proj_details['fy'] = fy
        time.sleep(2) # to ease pressure on sciencebase servers
        proj_json = sb.get_item(proj_id)
        proj_details['title'] = proj_json['title']
        proj_details['size'] = 0
        try:
            proj_files = proj_json['files']
            for proj_file in proj_files:
                proj_details['size'] += proj_file['size']
        #-------------------------------
        except:
            pass
        
        proj_title = proj_details['title']
        proj_size = proj_details['size']
        
        proj_details_list.append(proj_details)
        
        # build approved dataset list
        dataset_ids = sb.get_child_ids(proj_id)
        for dataset_id in dataset_ids:
            time.sleep(2) # to ease pressure on sciencebase servers
            dataset_json = sb.get_item(dataset_id)
            if dataset_json['title'].lower() == 'approved datasets':
                approved_dataset_items = get_approved_items(dataset_id)
                num_items += collect_item_details(casc, fy, proj_id, proj_title, proj_size, approved_dataset_items, item_details_list)
        
    return num_items

def get_approved_items(dataset_id):
        
    approved_items = []
    
    def get_items(parent_id):
        child_id_list = sb.get_child_ids(parent_id)
        for child_id in child_id_list:
            child_json = sb.get_item(child_id)
            if child_json['hasChildren']: # keep drilling down into folders (depth first search)
                get_items(child_id)
            else:
                approved_items.append(child_id)
    
    get_items(dataset_id)
    
    return approved_items

def collect_item_details(casc, fy, proj_id, proj_title, proj_size, approved_dataset_items, item_details_list):
    
    num_items = 0
    print('p', end = '') # project is being processed
    for item_id in approved_dataset_items:

        print('*', end = '') # file is being processed
        
        #-----build item details-----
        item_details = {}

        item_details['id'] = item_id
        item_details['casc'] = casc
        item_details['FY'] = fy
        item_details['proj_id'] = proj_id
        item_details['proj_title'] = proj_title
        item_details['proj_size'] = proj_size

        time.sleep(2) # to ease pressure on sciencebase servers
        item_json = sb.get_item(item_id)

        try:
            item_details['title'] = item_json['title']
        except:
            item_details['title'] = ''
        try:
            item_details['url'] = item_json['link']['url']
        except:
            item_details['url'] = ''
        try:
            item_details['relatedItemsUrl'] = item_json['relatedItems']['link']['url']
        except:
            item_details['relatedItemsUrl'] = ''
        try:
            item_details['summary'] = item_json['summary']
        except:
            item_details['summary'] = ''
        try:
            item_details['hasChildren'] = item_json['hasChildren']
        except:
            item_details['hasChildren'] = ''
        try:
            item_details['parentId'] = item_json['parentId']
        except:
            item_details['parentId'] = ''

        xml_urls = ''
        try:
            for item_file in item_json['files']:
                if 'xml' in item_file['contentType'] and 'xml' in item_file['name']:
                    xml_urls += item_file['url'] + ',' # separate by commas
            xml_urls = xml_urls.strip(',')
        except:
            pass
        item_details['xml_urls'] = xml_urls

        try:
            item_details['num_files'] = len(item_json['files'])
        except:
            item_details['num_files'] = 0

        item_details['pub_date'] = ''
        item_details['start_date'] = ''
        item_details['end_date'] = ''
        try:
            for date_item in item_json['dates']:
                try:
                    if date_item['type'].lower() == 'publication' or date_item['label'] == 'publication date':
                        item_details['pub_date'] = date_item['dateString']
                except:
                    item_details['pub_date'] = ''
                try:
                    if date_item['type'].lower() == 'start':
                        item_details['start_date'] = date_item['dateString']
                except:
                    item_details['start_date'] = ''
                try:
                    if date_item['type'].lower() == 'end':
                        item_details['end_date'] = date_item['dateString']
                except:
                    item_details['end_date'] = ''
        except:
            pass

        item_details['contacts'] = []
        try:
            contacts = item_json['contacts']
            for contact in contacts:
                details = {}
                try:
                    details['name'] = contact['name']
                except:
                    details['name'] = ''
                try:
                    details['type'] = contact['type']
                except:
                    details['type'] = ''
                try:
                    details['email'] = contact['email']
                except:
                    details['email'] = ''
                try:
                    details['jobTitle'] = contact['jobTitle']
                except:
                    details['jobTitle'] = ''
                try:
                    details['orcId'] = contact['orcId']
                except:
                    details['orcId'] = ''

                item_details['contacts'].append(details)
        #----------------------------
        except:
            pass

        item_details_list.append(item_details)
        num_items += 1
        
    return num_items

def update_cascs(app, casc_list):
    """Perform hard search on any ids older than 1 day.

    This function calls get_cascs() to populate the fy_obj_list list with
    fiscal year objects for each of the fiscal years present in each CSC.
    It begins the parsing process by calling parse_fiscal_years(), which finds
    all projects in each fiscal year and each item in each project to create a
    comprehensive database for each fiscal year in each CSC. All CSCs, fiscal
    years, projects, items, etc are added to their respective relational
    database tables.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        casc_list -- List of CASCs to be updated

    Raises:
        Exception -- If something was wrong and fy_obj_list was not cleared by
                     the end of the process.

    """
    # To run this package from command line:
    # python -c 'from __init__ import start; start()'

    start = time.time()

    fy_obj_list = fiscal_years.get_cascs(casc_list)

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fy_obj_list = fiscal_years.parse_fiscal_years(app, fy_obj_list)
    update_casc_total_data(app)

    end = time.time()

    print('Total time: ' + str(end - start))

    if not fy_obj_list:
        print("""

    ===========================================================================

                    CASC update completed.""")
    #     exit(0)
    # print("WHY AM I HERE???")
    # assert False, "Should never get here!!!!"
    # raise Exception("Something went wrong in full_hard_search()")


def full_hard_search(app):
    """Perform hard search on any ids older than 1 day.

    This function calls get_all_cscs() to populate the fy_obj_list list with
    fiscal year objects for each of the fiscal years present in each CSC.
    It begins the parsing process by calling parse_fiscal_years(), which finds
    all projects in each fiscal year and each item in each project to create a
    comprehensive database for each fiscal year in each CSC. All CSCs, fiscal
    years, projects, items, etc are added to their respective relational
    database tables.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.

    Raises:
        Exception -- If something was wrong and fy_obj_list was not cleared by
                     the end of the process.

    """
    # To run this package from command line:
    # python -c 'from __init__ import start; start()'

    fy_obj_list = fiscal_years.get_all_cscs()

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fy_obj_list = fiscal_years.parse_fiscal_years(app, fy_obj_list)
    update_casc_total_data(app)
    if not fy_obj_list:
        print("""

    ===========================================================================

                    Hard Search is now finished.""")
        exit(0)
    print("WHY AM I HERE???")
    assert False, "Should never get here!!!!"
    raise Exception("Something went wrong in full_hard_search()")


def defined_hard_search(app):
    """Perform hard search on specific fiscal years via user-input.

    This hard search function collects fiscal years from a user that are
    parsed to find projects, which are parsed to find items. All CSCs, fiscal
    years, projects, items, etc are added to their respective relational
    database tables.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.

    Raises:
        Exception -- If something was wrong and fy_obj_list was not cleared by
                     the end of the process.

    """
    # To run this function from command line:
    # python -c 'from main import defined_hard_search; defined_hard_search()'

    fy_id_list = fiscal_years.get_user_input_fys()
    fy_obj_list = fiscal_years.create_fy_objs(fy_id_list)

    if __debug__:
        print("fy_obj_list:\n{0}".format(fy_obj_list))
    fiscal_years.parse_fiscal_years(app, fy_obj_list)
    update_casc_total_data(app)
    if not fy_obj_list:
        print("""

    ===========================================================================

                    Defined Hard Search is now finished.""")
        exit(0)
    print("WHY AM I HERE???")
    assert False, "Should never get here!!!!"
    raise Exception("Something went wrong in full_hard_search()")


def debug_projects():
    """For debugging/testing, find all items and calculate project size.

    The function can be given a fiscal year ID and CSC, or use a 'dummy'
    default (SWCSC FY 2011) if not important. It will then parse the project
    and its items as it normally would and print the results.
    """
    # To run this from the terminal, use the following:
    # python -c 'from main import debug_projects; debug_projects()'

    project_id = '1'
    while len(project_id) != 24:
        print("Please provide a Science Base Project ID.")
        project_id = input("Project ID: ")
    print("Provide a fiscal year ID and CSC, or use Dummy Fiscal Year?")
    preference = input("> ").lower()
    if "dum" in preference:
        # Dummy Fiscal Year:
        fiscal_year = gl.SbFiscalYear("50070504e4b0abf7ce733fd7", "SWCSC")
    else:
        fy_id = input("Fiscal Year ID: ")
        fy_csc = input("CSC: ")
        fiscal_year = gl.SbFiscalYear(fy_id, fy_csc)

    project = gl.SbProject(project_id, fiscal_year)
    projects.parse_project(project)
    print("\n\nAnother? (Y / N)")
    answer = input("> ").lower()
    if 'y' in answer:
        debug_projects()
    elif 'n' in answer:
        exit(0)
    else:
        print("Neither answer selected. Program ended.")


def id_in_list(obj_list, sb_object):
    """Check if a Science Base object exists in a list.

    Arguments:
        obj_list -- (list) a list of objects with an 'ID' attribute.
        sb_object -- (item_id, SbFiscalYear, SbProject, or SbItem)
                     Any item with an '.ID' field.

    Returns:
        True -- (boolean) returned if an item is encountered in obj_list with
                an .ID attribute that matches the .ID attribute of sb_object.
        False -- (boolean) returned if no such item is encountered after
                 iterating through obj_list.

    """
    if __debug__:
        print("Checking if sb_object in list...")
    for sb_objects in obj_list:
        if sb_object.ID == sb_objects.ID:
            if __debug__:
                print("Object in list.")
            return True
    if __debug__:
        print("Object not in list")
    return False


def get_date():
    """Return the current date as a string."""
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    return date

def save_to_db(app, fiscal_year):
    """Save Fiscal Year data to database.
    
    Call functions from the module 'db_save.py' to save Fiscal Year, Projects,
    Items, etc to the database.
    
    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fiscal_year -- (SbFiscalYear) A completed SbFiscalYear object (defined
                       in 'gl.py') to be parsed and saved to the database.

    """
    # Save casc to db and get db model for casc
    casc_model = db_save.save_casc(app, fiscal_year)

    fy_model = db_save.save_fy(app, fiscal_year, casc_model)

    for project in fiscal_year.projects:
        proj_model = db_save.save_proj(app, project, fy_model, casc_model)
        for item in project.project_items["Project_Item_List"]:
            item_model = db_save.save_item(app, item, proj_model, fy_model,
                                           casc_model)
            for file_json in item.file_list:
                db_save.save_file(app, file_json, item_model, proj_model,
                                  fy_model, casc_model)


def update_casc_total_data(app):
    print("""
------------------------------------------------------------------------------
          """)
    print("Updating all CASC `.total_data` fields...")
    cascs = app.db.session.query(app.casc).all()
    print("CASCs found:")
    num = 0
    for casc in cascs:
        num += 1
        total_data = 0
        print("\t{0}. {1}".format(num, casc.name))
        fys = casc.fiscal_years.all()
        for fy in fys:
            total_data += fy.total_data
            if (total_data - fy.total_data) == 0:
                print("{}".format(fy.total_data), end="")
            else:
                print(" + {}".format(fy.total_data), end="")
        print("\n")
        casc.total_data = total_data
        app.db.session.commit()
        print("Total Data in {0}:\n\t{1}\n\n"
              .format(casc.name, casc.total_data))

    print("""
------------------------------------------------------------------------------
          """)
