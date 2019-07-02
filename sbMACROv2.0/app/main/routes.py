"""Define main application routes."""
import os
import sys
import openpyxl
from datetime import datetime
from collections import OrderedDict
from flask import render_template, redirect, url_for, request, jsonify, current_app, session
from flask_login import current_user, login_required
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms import BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, Email
from wtforms.validators import Optional
from app import db


from app.main.forms import EditProfileForm, FyForm, SearchForm
from app.models import User, casc, FiscalYear, Project, Item, SbFile

from app.main import bp
from app.main.metadata import write_metadata
from app.main.forms import EditProfileForm, FyForm, GeneralForm
from app.models import User, casc, FiscalYear, Project, Item, SbFile
from app.auth.read_sheets import get_sheet_name, parse_values
from app.updater.__init__ import update, refresh_master_tables
from app.updater.main import get_item_details, get_proj_details
import multiprocessing

from nltk.corpus import stopwords

from config import Config
# from sbmacro import socketio
from pprint import pprint


my_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(my_root, 'templates/static/')


@bp.before_app_request
def before_request():
    """Update user 'last seen' field before each request."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        current_user.search_form = SearchForm()

@bp.route('/', methods = ['GET', 'POST'])  # Also accepts
@bp.route('/index', methods = ['GET', 'POST'])  # Default
def index():
    # class F(GeneralForm):
    #     def __init__(self, buttonText):
    #         super(F, self).__init__()
    #         # self.name = BooleanField('static field')
    #         self.submit = SubmitField(buttonText)

    # form = F('Refresh Metadata')

    class F(FyForm):
        pass

    form = F()

    """Render splash page for sbMACRO."""
    return(render_template('index.html', **locals(), title = "Welcome to sbMACRO"))


@bp.route('/metadata', methods = ['GET', 'POST'])
def metadata():

    tag_to_search = request.form['tag_to_search']
    custom_stopwords = ['climate', 'change']
    protocol = 'xml'
    url_file_name = 'metadata_urls.csv'
    us_states_file_name = 'us-states.csv'

    us_states = []
    with open(file_path + us_states_file_name, 'r') as file:
        for state in file:
            us_states.append(state.strip().lower())

    stop_words = us_states + stopwords.words('english') + custom_stopwords

    if request.method == 'POST':
        casc_name = request.form['casc_name']

        metadata_urls = []

        with open(file_path + url_file_name, 'r') as file:
            for line in file:
                casc, url = line.split(',')
                if casc == casc_name:
                    metadata_urls.append(url)

        # write to csv to be read by wordcloud module
        write_metadata(casc_name, tag_to_search, metadata_urls, stop_words)

    return ''


@bp.route('/fiscal_years')
@bp.route('/fiscalyears')
@bp.route('/select_fiscalyear', methods=['GET', 'POST'])  # Also accepts
@bp.route('/select_fiscalyears', methods=['GET', 'POST'])  # Default
def fiscalyear():
    """Retrieve Fiscal Years and display for selection by user."""
    cascs = db.session.query(casc).order_by(casc.name).all()
    cascs_and_fys = {}

    class F(FyForm):
        pass

    list_fy = []
    for curr_casc in cascs:
        cascs_and_fys[curr_casc.name] = {}
        cascs_and_fys[curr_casc.name]["id"] = curr_casc.id
        fys = db.session.query(FiscalYear).order_by(
            FiscalYear.name).filter(
            FiscalYear.casc_id == curr_casc.id).all()
        cascs_and_fys[curr_casc.name]["fiscal_years"] = []
        for fy in fys:
            fiscal_year = {}
            list_fy.append("fy" + str(fy.id))
            fiscal_year["id"] = fy.id
            fiscal_year["name"] = fy.name
            cascs_and_fys[curr_casc.name]["fiscal_years"].append(fiscal_year)
            setattr(F, "fy" + str(fy.id), BooleanField(fy.name))

    form = F()
    if form.validate_on_submit():
        id_list = []
        projects = []
        for fy in list_fy:
            fy_attr = getattr(form, fy)
            selected = fy_attr.data
            if selected:
                id_list.append(fy.replace("fy", ""))

        for i in id_list:
            fy_model = db.session.query(FiscalYear).get(i)
            for proj in fy_model.projects:
                project_dict = {}
                project_dict['fy_id'] = i
                project_dict['casc_id'] = fy_model.casc_id
                project_dict['proj_id'] = proj.id
                projects.append(project_dict)

        session["projects"] = projects
        return redirect(url_for('main.report'))
    elif request.method == 'GET':
        pass

    return render_template('fiscalYears.html',
                           form=form,
                           cascs_and_fys=cascs_and_fys,
                           title="Select Fiscal Years")


@bp.route('/update_db', methods=['GET', 'POST'])
def update_db():
    """Retrieve CASCs and display for selection by user."""

    if request.method == 'POST':
        try:
            refresh_master_details = request.form['refresh_master_details']
            if refresh_master_details:
                session['refresh_master_details'] = refresh_master_details
                return redirect(url_for('main.updates'))
        except:
            pass

    list_of_cascs = []
    cascs_to_update = []

    cascs = db.session.query(casc).order_by(casc.name).all()

    class F(FyForm):
        pass

    for curr_casc in cascs:
        list_of_cascs.append(str(curr_casc.name))
        setattr(F, str(curr_casc.name), BooleanField(curr_casc.name.replace(' CASC', '')))

    form = F()
    if form.validate_on_submit():
        
        for csc in list_of_cascs:
            csc_attr = getattr(form, csc)

            selected = csc_attr.data
            if selected:
                cascs_to_update.append(csc.replace(' CASC', ''))

        session['cascs_to_update'] = cascs_to_update

        return redirect(url_for('main.updates'))

    elif request.method == 'GET':
        pass

    return render_template('update_db.html', form = form, list_of_cascs = list_of_cascs)

# @socketio.on('connect', namespace='/test')
@bp.route('/updates')
def updates():
    """Update the cascs selected for update, or refresh master details table"""
    refresh_master_details = False
    cascs_to_update = []
    try:
        refresh_master_details = session['refresh_master_details']
        if refresh_master_details:
            print('Starting refresh process')
            # items_file_path = file_path + 'item_ids.csv'
            items_file_path = file_path + 'item_details.pkl'
            projs_file_path = file_path + 'proj_details.pkl'
            item_details = get_item_details(items_file_path)
            proj_details = get_proj_details(projs_file_path)
            print('Starting item_details thread')
            items_refresh_thread = multiprocessing.Process(target = refresh_master_tables, args = (item_details, 'items',))
            items_refresh_thread.start()
            print('Starting proj_details thread')
            projs_refresh_thread = multiprocessing.Process(target = refresh_master_tables, args = (proj_details, 'projs',))
            projs_refresh_thread.start()
            return render_template("updates.html", cascs_to_update = cascs_to_update, refresh_master_details = refresh_master_details)
    except:
        pass
    try:
        cascs_to_update = session['cascs_to_update']
        if cascs_to_update:
            casc_update_thread = multiprocessing.Process(target = update, args = (cascs_to_update,))
            casc_update_thread.start()
            return render_template("updates.html", cascs_to_update = cascs_to_update, refresh_master_details = refresh_master_details)
    except:
        pass

    return render_template("updates.html", cascs_to_update = cascs_to_update, refresh_master_details = refresh_master_details)


@bp.route('/projects', methods=['GET', 'POST'])
@bp.route('/select_project', methods=['GET', 'POST'])
@bp.route('/select_projects', methods=['GET', 'POST'])
def project():
    """Display and implement selection/searching for projects by URL."""
    if request.method == 'POST':
        sb_urls = request.form.getlist("SBurls")
        print("sb_urls:")
        pprint(sb_urls)
        projects = []
        for url in sb_urls:
            project_dict = {}
            proj = db.session.query(Project).filter(Project.url == url).first()
            if proj is None:
                print("---Error: Could not find project for {}".format(url))
                continue
            else:
                print("Found: {0}: {1}".format(proj.id, proj.name))
            fys = proj.fiscal_years
            if len(fys) > 1:
                project_dict['fy_id'] = []
                project_dict['casc_id'] = []
                for fy in fys:
                    project_dict['fy_id'].append(fy.id)
                    project_dict['casc_id'].append(fy.casc_id)
            else:
                fy = fys[0]
                project_dict['fy_id'] = fy.id
                project_dict['casc_id'] = fy.casc_id

            project_dict['proj_id'] = proj.id
            projects.append(project_dict)
            session["projects"] = projects
        return redirect(url_for('main.report'))

    return(render_template('projects.html', title="Select Projects to Report"))


@bp.route('/report')
def report():
    """Gather appropriate report information and display."""

    excel_file = 'CASC Data Management Tracking for Projects - v2.xlsx'
    project_list = session["projects"]
    projects = []
    workbook = None

    # Decide whether to load project tracking excel workbook
    if current_user.is_authenticated and current_user.access_level > 0:
        for project in project_list:
            casc_item = db.session.query(casc).get(project['casc_id'])
            if get_sheet_name(casc_item.name):
                # Load workbook
                try:
                    print('Opening {}...'.format(excel_file))
                    workbook = openpyxl.load_workbook(excel_file)
                    print('Successfully opened {}'.format(excel_file))
                except:
                    print('File error: {}'.format(excel_file))
                # No need to continue if workbook has just been loaded
                break
    
    class ReportItem(object):
        """Object to be passed to front-end for display in table and modal."""

        name = None
        id = None
        sb_id = None
        url = None
        obj_type = None
        data_in_project_GB = None
        num_of_files = None
        total_data_in_fy_GB = None
        timestamp = None
        dmp_status = None
        pi_list = []
        summary = None
        history = None
        item_breakdown = None
        potential_products = None
        products_received = []
        file_breakdown = []

        # Possibly necessary info:
        casc = None
        fiscal_year = None
        project = None
        item = None

        def __init__(self, obj_type, obj_db_id, fy_db_id, casc_db_id):
            """Initialize ReportItem class object.

            Arguments:
                obj_type -- (string) 'project', 'fiscal year', 'casc', 'item',
                            'sbfile', or 'problem item' to determine the type
                            of object being created.
                obj_db_id -- (int) the database id for the item being created.
                fy_db_id -- (int or list) the database id for the item's
                            fiscal year of concern.
                casc_db_id -- (int or list) the database id for the item's
                              casc year of concern.

            """

            sheet = {}

            if obj_type == 'project':
                self.obj_type = obj_type
                proj = db.session.query(Project).filter(
                    Project.id == obj_db_id).first()
                if proj == None:
                    raise Exception  # It has to be there somewhere...
                else:
                    self.name = proj.name
                    self.id = obj_db_id
                    self.sb_id = proj.sb_id
                    self.url = proj.url
                    # convert from MB -> GB
                    self.data_in_project_GB = proj.total_data / 1000
                    self.num_of_files = proj.files.count()
                    if fy_db_id is list:
                        self.fiscal_year = []
                        self.casc = []
                        self.total_data_in_fy_GB = []
                        for fy_id in fy_db_id:
                            fy = db.session.query(FiscalYear).get(fy_id)
                            self.fiscal_year.append(fy.name)
                            casc_model = db.session.query(casc).get(fy.casc_id)
                            self.casc.append(casc_model.name)
                            # convert from MB -> GB
                            self.total_data_in_fy_GB.append(
                                fy.total_data / 1000)

                    else:
                        fy = db.session.query(FiscalYear).get(fy_db_id)
                        self.fiscal_year = fy.name
                        casc_model = db.session.query(casc).get(casc_db_id)
                        self.casc = casc_model.name
                        # convert from MB -> GB
                        self.total_data_in_fy_GB = fy.total_data / 1000
                    self.timestamp = proj.timestamp
                    self.pi_list = []
                    for pi in proj.principal_investigators:
                        curr_pi = {'name': pi.name, 'email': pi.email}
                        self.pi_list.append(curr_pi)
                    self.summary = proj.summary
                    self.products_received = []
                    for item in proj.items:
                        curr_item = {'name': item.name, 'url': item.url}
                        self.products_received.append(curr_item)
                    # Things that depend on user access level:
                    if current_user.is_authenticated:
                        if current_user.access_level > 0:

                            # Parse excel sheet
                            sheet_name = get_sheet_name(self.casc)
                            if sheet_name:
                                values = []
                                for vals in workbook[sheet_name].values:
                                    if vals[0] is None:
                                        break
                                    values.append(vals)

                                sheet = parse_values(values)

    # ACTION ITEM: In a production app, you likely
                            #       want to save these credentials in a
                            #       persistent database instead.
                            session['credentials'] = credentials_to_dict(
                                credentials)
                            try:
                                # DMP Status
                                self.dmp_status = sheet[proj.sb_id]['DMP Status']
                                if self.dmp_status is None or self.dmp_status.isspace() or self.dmp_status == "":

                                    self.dmp_status = "No DMP status provided"
                                # History
                                self.history = sheet[proj.sb_id]['History']
                                if self.history is None or self.history.isspace() or self.history == "":
                                    self.history = "No data steward history provided"
                                # Potential Products
                                self.potential_products = sheet[proj.sb_id]['Expected Products']
                                if self.potential_products is None or self.potential_products.isspace() or self.potential_products == "":
                                    self.potential_products = "No data potential products provided"
                            except KeyError:
                                self.dmp_status = "Project not currently tracked by Data Steward"
                                self.history = "Project not currently tracked by Data Steward"
                                self.potential_products = "Project not currently tracked by Data Steward"

                        else:
                            self.dmp_status = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.history = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.potential_products = "Please email "\
                                + "administrators at {} to receive access "\
                                .format(current_app.config['ADMINS'][0])\
                                + "privileges to view this content."
                    else:
                        self.dmp_status = "Please login to view this content."
                        self.history = "Please login to view this content."
                        self.potential_products = "Please login to view this content."
                    self.file_breakdown = []
                    proj_file_list = []
                    for sbfile in proj.files:
                        proj_file_list.append(sbfile.id)
                    if len(proj_file_list) > 0:
                        file_breakdown_list = db.session.query(
                            SbFile.content_type, db.func.count(
                                SbFile.content_type)).group_by(
                                    SbFile.content_type).filter(
                                        SbFile.id.in_(proj_file_list[:999])).all()  # sqlalchemy max query items is 999
                        proj_file_list[:] = []
                        for _tuple in file_breakdown_list:
                            temp_dict = {}
                            temp_dict['label'] = _tuple[0]
                            temp_dict['count'] = _tuple[1]
                            proj_file_list.append(temp_dict)
                        self.file_breakdown = sorted(
                            proj_file_list,
                            key=lambda k: k['count'],
                            reverse=True)

            elif obj_type == 'fiscal year':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'casc':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'sbfile':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'problem item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
    for project in project_list:
        new_obj = ReportItem(
            'project', project['proj_id'], project['fy_id'], project['casc_id'])
        projects.append(new_obj.__dict__)

    return render_template("report.html", projects=projects)

@bp.route('/verticalbar')
def verticalbar():
    """Gather appropriate report information and display."""

    excel_file = 'CASC Data Management Tracking for Projects - v2.xlsx'
    project_list = session["projects"]
    projects = []
    workbook = None

    # Decide whether to load project tracking excel workbook
    if current_user.is_authenticated and current_user.access_level > 0:
        for project in project_list:
            casc_item = db.session.query(casc).get(project['casc_id'])
            if get_sheet_name(casc_item.name):
                # Load workbook
                try:
                    print('Opening {}...'.format(excel_file))
                    workbook = openpyxl.load_workbook(excel_file)
                    print('Successfully opened {}'.format(excel_file))
                except:
                    print('File error: {}'.format(excel_file))
                # No need to continue if workbook has just been loaded
                break

    class ReportItem(object):
        """Object to be passed to front-end for display in table and modal."""

        name = None
        id = None
        sb_id = None
        url = None
        obj_type = None
        data_in_project_GB = None
        num_of_files = None
        total_data_in_fy_GB = None
        timestamp = None
        dmp_status = None
        pi_list = []
        summary = None
        history = None
        item_breakdown = None
        potential_products = None
        products_received = []
        file_breakdown = []

        # Possibly necessary info:
        casc = None
        fiscal_year = None
        project = None
        item = None

        def __init__(self, obj_type, obj_db_id, fy_db_id, casc_db_id):
            """Initialize ReportItem class object.

            Arguments:
                obj_type -- (string) 'project', 'fiscal year', 'casc', 'item',
                            'sbfile', or 'problem item' to determine the type
                            of object being created.
                obj_db_id -- (int) the database id for the item being created.
                fy_db_id -- (int or list) the database id for the item's
                            fiscal year of concern.
                casc_db_id -- (int or list) the database id for the item's
                              casc year of concern.

            """

            sheet = {}

            if obj_type == 'project':
                self.obj_type = obj_type
                proj = db.session.query(Project).filter(
                    Project.id == obj_db_id).first()
                if proj == None:
                    raise Exception  # It has to be there somewhere...
                else:
                    self.name = proj.name
                    self.id = obj_db_id
                    self.sb_id = proj.sb_id
                    self.url = proj.url
                    # convert from MB -> GB
                    self.data_in_project_GB = proj.total_data / 1000
                    self.num_of_files = proj.files.count()
                    if fy_db_id is list:
                        self.fiscal_year = []
                        self.casc = []
                        self.total_data_in_fy_GB = []
                        for fy_id in fy_db_id:
                            fy = db.session.query(FiscalYear).get(fy_id)
                            self.fiscal_year.append(fy.name)
                            casc_model = db.session.query(casc).get(fy.casc_id)
                            self.casc.append(casc_model.name)
                            # convert from MB -> GB
                            self.total_data_in_fy_GB.append(
                                fy.total_data / 1000)

                    else:
                        fy = db.session.query(FiscalYear).get(fy_db_id)
                        self.fiscal_year = fy.name
                        casc_model = db.session.query(casc).get(casc_db_id)
                        self.casc = casc_model.name
                        # convert from MB -> GB
                        self.total_data_in_fy_GB = fy.total_data / 1000
                    self.timestamp = proj.timestamp
                    self.pi_list = []
                    for pi in proj.principal_investigators:
                        curr_pi = {'name': pi.name, 'email': pi.email}
                        self.pi_list.append(curr_pi)
                    self.summary = proj.summary
                    self.products_received = []
                    for item in proj.items:
                        curr_item = {'name': item.name, 'url': item.url}
                        self.products_received.append(curr_item)
                    # Things that depend on user access level:
                    if current_user.is_authenticated:
                        if current_user.access_level > 0:

                            # Parse excel sheet
                            sheet_name = get_sheet_name(self.casc)
                            if sheet_name:
                                values = []
                                for vals in workbook[sheet_name].values:
                                    if vals[0] is None:
                                        break
                                    values.append(vals)

                                sheet = parse_values(values)

    # ACTION ITEM: In a production app, you likely
                            #       want to save these credentials in a
                            #       persistent database instead.
                            session['credentials'] = credentials_to_dict(
                                credentials)
                            try:
                                # DMP Status
                                self.dmp_status = sheet[proj.sb_id]['DMP Status']
                                if self.dmp_status is None or self.dmp_status.isspace() or self.dmp_status == "":

                                    self.dmp_status = "No DMP status provided"
                                # History
                                self.history = sheet[proj.sb_id]['History']
                                if self.history is None or self.history.isspace() or self.history == "":
                                    self.history = "No data steward history provided"
                                # Potential Products
                                self.potential_products = sheet[proj.sb_id]['Expected Products']
                                if self.potential_products is None or self.potential_products.isspace() or self.potential_products == "":
                                    self.potential_products = "No data potential products provided"
                            except KeyError:
                                self.dmp_status = "Project not currently tracked by Data Steward"
                                self.history = "Project not currently tracked by Data Steward"
                                self.potential_products = "Project not currently tracked by Data Steward"

                        else:
                            self.dmp_status = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.history = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.potential_products = "Please email "\
                                + "administrators at {} to receive access "\
                                .format(current_app.config['ADMINS'][0])\
                                + "privileges to view this content."
                    else:
                        self.dmp_status = "Please login to view this content."
                        self.history = "Please login to view this content."
                        self.potential_products = "Please login to view this content."
                    self.file_breakdown = []
                    proj_file_list = []
                    for sbfile in proj.files:
                        proj_file_list.append(sbfile.id)
                    if len(proj_file_list) > 0:
                        file_breakdown_list = db.session.query(
                            SbFile.content_type, db.func.count(
                                SbFile.content_type)).group_by(
                                    SbFile.content_type).filter(
                                        SbFile.id.in_(proj_file_list[:999])).all()  # sqlalchemy max query items is 999
                        proj_file_list[:] = []
                        for _tuple in file_breakdown_list:
                            temp_dict = {}
                            temp_dict['label'] = _tuple[0]
                            temp_dict['count'] = _tuple[1]
                            proj_file_list.append(temp_dict)
                        self.file_breakdown = sorted(
                            proj_file_list,
                            key=lambda k: k['count'],
                            reverse=True)

            elif obj_type == 'fiscal year':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'casc':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'sbfile':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'problem item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.

    for project in project_list:
        new_obj = ReportItem(
            'project', project['proj_id'], project['fy_id'], project['casc_id'])
        projects.append(new_obj.__dict__)

    return render_template("verticalbar.html", projects=projects)


@bp.route('/horizontalbar')
def horizontalbar():
    """Gather appropriate report information and display."""

    excel_file = 'CASC Data Management Tracking for Projects - v2.xlsx'
    project_list = session["projects"]
    projects = []
    workbook = None

    # Decide whether to load project tracking excel workbook
    if current_user.is_authenticated and current_user.access_level > 0:
        for project in project_list:
            casc_item = db.session.query(casc).get(project['casc_id'])
            if get_sheet_name(casc_item.name):
                # Load workbook
                try:
                    print('Opening {}...'.format(excel_file))
                    workbook = openpyxl.load_workbook(excel_file)
                    print('Successfully opened {}'.format(excel_file))
                except:
                    print('File error: {}'.format(excel_file))
                # No need to continue if workbook has just been loaded
                break

    class ReportItem(object):
        """Object to be passed to front-end for display in table and modal."""

        name = None
        id = None
        sb_id = None
        url = None
        obj_type = None
        data_in_project_GB = None
        num_of_files = None
        total_data_in_fy_GB = None
        timestamp = None
        dmp_status = None
        pi_list = []
        summary = None
        history = None
        item_breakdown = None
        potential_products = None
        products_received = []
        file_breakdown = []

        # Possibly necessary info:
        casc = None
        fiscal_year = None
        project = None
        item = None

        def __init__(self, obj_type, obj_db_id, fy_db_id, casc_db_id):
            """Initialize ReportItem class object.

            Arguments:
                obj_type -- (string) 'project', 'fiscal year', 'casc', 'item',
                            'sbfile', or 'problem item' to determine the type
                            of object being created.
                obj_db_id -- (int) the database id for the item being created.
                fy_db_id -- (int or list) the database id for the item's
                            fiscal year of concern.
                casc_db_id -- (int or list) the database id for the item's
                              casc year of concern.

            """

            sheet = {}

            if obj_type == 'project':
                self.obj_type = obj_type
                proj = db.session.query(Project).filter(Project.id == obj_db_id).first()
                if proj == None:
                    raise Exception  # It has to be there somewhere...
                else:
                    self.name = proj.name
                    self.id = obj_db_id
                    self.sb_id = proj.sb_id
                    self.url = proj.url
                    # convert from MB -> GB
                    self.data_in_project_GB = proj.total_data / 1000
                    self.num_of_files = proj.files.count()
                    if fy_db_id is list:
                        self.fiscal_year = []
                        self.casc = []
                        self.total_data_in_fy_GB = []
                        for fy_id in fy_db_id:
                            fy = db.session.query(FiscalYear).get(fy_id)
                            self.fiscal_year.append(fy.name)
                            casc_model = db.session.query(casc).get(fy.casc_id)
                            self.casc.append(casc_model.name)
                            # convert from MB -> GB
                            self.total_data_in_fy_GB.append(fy.total_data / 1000)

                    else:
                        fy = db.session.query(FiscalYear).get(fy_db_id)
                        self.fiscal_year = fy.name
                        casc_model = db.session.query(casc).get(casc_db_id)
                        self.casc = casc_model.name
                        # convert from MB -> GB
                        self.total_data_in_fy_GB = fy.total_data / 1000
                    self.timestamp = proj.timestamp
                    self.pi_list = []
                    for pi in proj.principal_investigators:
                        curr_pi = {'name': pi.name, 'email': pi.email}
                        self.pi_list.append(curr_pi)
                    self.summary = proj.summary
                    self.products_received = []
                    for item in proj.items:
                        curr_item = {'name': item.name, 'url': item.url}
                        self.products_received.append(curr_item)
                    # Things that depend on user access level:
                    if current_user.is_authenticated:
                        if current_user.access_level > 0:

                            # Parse excel sheet
                            sheet_name = get_sheet_name(self.casc)
                            if sheet_name:
                                values = []
                                try:
                                    for vals in workbook[sheet_name].values:
                                        if vals[0] is None:
                                            break
                                        values.append(vals)

                                    sheet = parse_values(values)
                                except:
                                    pass

    # ACTION ITEM: In a production app, you likely
                            #       want to save these credentials in a
                            #       persistent database instead.
                            session['credentials'] = credentials_to_dict(credentials)
                            try:
                                try:
                                    # DMP Status
                                    self.dmp_status = sheet[proj.sb_id]['DMP Status']
                                    if self.dmp_status is None or self.dmp_status.isspace() or self.dmp_status == "":

                                        self.dmp_status = "No DMP status provided"
                                    # History
                                    self.history = sheet[proj.sb_id]['History']
                                    if self.history is None or self.history.isspace() or self.history == "":
                                        self.history = "No data steward history provided"
                                    # Potential Products
                                    self.potential_products = sheet[proj.sb_id]['Expected Products']
                                    if self.potential_products is None or self.potential_products.isspace() or self.potential_products == "":
                                        self.potential_products = "No data potential products provided"
                                except KeyError:
                                    self.dmp_status = "Project not currently tracked by Data Steward"
                                    self.history = "Project not currently tracked by Data Steward"
                                    self.potential_products = "Project not currently tracked by Data Steward"
                            except:
                                pass
                        else:
                            self.dmp_status = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.history = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.potential_products = "Please email "\
                                + "administrators at {} to receive access "\
                                .format(current_app.config['ADMINS'][0])\
                                + "privileges to view this content."
                    else:
                        self.dmp_status = "Please login to view this content."
                        self.history = "Please login to view this content."
                        self.potential_products = "Please login to view this content."
                    self.file_breakdown = []
                    proj_file_list = []
                    for sbfile in proj.files:
                        proj_file_list.append(sbfile.id)
                    if len(proj_file_list) > 0:
                        file_breakdown_list = db.session.query(
                            SbFile.content_type, db.func.count(
                                SbFile.content_type)).group_by(
                                    SbFile.content_type).filter(
                                        SbFile.id.in_(proj_file_list[:999])).all()  # sqlalchemy max query items is 999
                        proj_file_list[:] = []
                        for _tuple in file_breakdown_list:
                            temp_dict = {}
                            temp_dict['label'] = _tuple[0]
                            temp_dict['count'] = _tuple[1]
                            proj_file_list.append(temp_dict)
                        self.file_breakdown = sorted(
                            proj_file_list,
                            key=lambda k: k['count'],
                            reverse=True)

            elif obj_type == 'fiscal year':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'casc':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'sbfile':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'problem item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.

    for project in project_list:
        new_obj = ReportItem(
            'project', project['proj_id'], project['fy_id'], project['casc_id'])
        projects.append(new_obj.__dict__)

    return render_template("horizontalbar.html", projects=projects)



@bp.route('/treemap')
def treemap():

    """Gather appropriate report information and display."""

    excel_file = 'CASC Data Management Tracking for Projects - v2.xlsx'
    project_list = session["projects"]
    projects = []
    workbook = None

    # Decide whether to load project tracking excel workbook
    if current_user.is_authenticated and current_user.access_level > 0:
        for project in project_list:
            casc_item = db.session.query(casc).get(project['casc_id'])
            if get_sheet_name(casc_item.name):
                # Load workbook
                try:
                    print('Opening {}...'.format(excel_file))
                    workbook = openpyxl.load_workbook(excel_file)
                    print('Successfully opened {}'.format(excel_file))
                except:
                    print('File error: {}'.format(excel_file))
                # No need to continue if workbook has just been loaded
                break

    class ReportItem(object):
        """Object to be passed to front-end for display in table and modal."""

        name = None
        id = None
        sb_id = None
        url = None
        obj_type = None
        data_in_project_GB = None
        num_of_files = None
        total_data_in_fy_GB = None
        timestamp = None
        dmp_status = None
        pi_list = []
        summary = None
        history = None
        item_breakdown = None
        potential_products = None
        products_received = []
        file_breakdown = []

        # Possibly necessary info:
        casc = None
        fiscal_year = None
        project = None
        item = None

        def __init__(self, obj_type, obj_db_id, fy_db_id, casc_db_id):
            """Initialize ReportItem class object.

            Arguments:
                obj_type -- (string) 'project', 'fiscal year', 'casc', 'item',
                            'sbfile', or 'problem item' to determine the type
                            of object being created.
                obj_db_id -- (int) the database id for the item being created.
                fy_db_id -- (int or list) the database id for the item's
                            fiscal year of concern.
                casc_db_id -- (int or list) the database id for the item's
                              casc year of concern.

            """

            sheet = {}

            if obj_type == 'project':
                self.obj_type = obj_type
                proj = db.session.query(Project).filter(
                    Project.id == obj_db_id).first()
                if proj == None:
                    raise Exception  # It has to be there somewhere...
                else:
                    self.name = proj.name
                    self.id = obj_db_id
                    self.sb_id = proj.sb_id
                    self.url = proj.url
                    # convert from MB -> GB
                    self.data_in_project_GB = proj.total_data / 1000
                    self.num_of_files = proj.files.count()
                    if fy_db_id is list:
                        self.fiscal_year = []
                        self.casc = []
                        self.total_data_in_fy_GB = []
                        for fy_id in fy_db_id:
                            fy = db.session.query(FiscalYear).get(fy_id)
                            self.fiscal_year.append(fy.name)
                            casc_model = db.session.query(casc).get(fy.casc_id)
                            self.casc.append(casc_model.name)
                            # convert from MB -> GB
                            self.total_data_in_fy_GB.append(
                                fy.total_data / 1000)

                    else:
                        fy = db.session.query(FiscalYear).get(fy_db_id)
                        self.fiscal_year = fy.name
                        casc_model = db.session.query(casc).get(casc_db_id)
                        self.casc = casc_model.name
                        # convert from MB -> GB
                        self.total_data_in_fy_GB = fy.total_data / 1000
                    self.timestamp = proj.timestamp
                    self.pi_list = []
                    for pi in proj.principal_investigators:
                        curr_pi = {'name': pi.name, 'email': pi.email}
                        self.pi_list.append(curr_pi)
                    self.summary = proj.summary
                    self.products_received = []
                    for item in proj.items:
                        curr_item = {'name': item.name, 'url': item.url}
                        self.products_received.append(curr_item)
                    # Things that depend on user access level:
                    if current_user.is_authenticated:
                        if current_user.access_level > 0:

                            # Parse excel sheet
                            sheet_name = get_sheet_name(self.casc)
                            if sheet_name:
                                values = []
                                for vals in workbook[sheet_name].values:
                                    if vals[0] is None:
                                        break
                                    values.append(vals)

                                sheet = parse_values(values)

    # ACTION ITEM: In a production app, you likely
                            #       want to save these credentials in a
                            #       persistent database instead.
                            session['credentials'] = credentials_to_dict(
                                credentials)
                            try:
                                # DMP Status
                                self.dmp_status = sheet[proj.sb_id]['DMP Status']
                                if self.dmp_status is None or self.dmp_status.isspace() or self.dmp_status == "":

                                    self.dmp_status = "No DMP status provided"
                                # History
                                self.history = sheet[proj.sb_id]['History']
                                if self.history is None or self.history.isspace() or self.history == "":
                                    self.history = "No data steward history provided"
                                # Potential Products
                                self.potential_products = sheet[proj.sb_id]['Expected Products']
                                if self.potential_products is None or self.potential_products.isspace() or self.potential_products == "":
                                    self.potential_products = "No data potential products provided"
                            except KeyError:
                                self.dmp_status = "Project not currently tracked by Data Steward"
                                self.history = "Project not currently tracked by Data Steward"
                                self.potential_products = "Project not currently tracked by Data Steward"

                        else:
                            self.dmp_status = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.history = "Please email administrators at"\
                                + " {} to receive access privileges to view "\
                                .format(current_app.config['ADMINS'][0])\
                                + "this content."
                            self.potential_products = "Please email "\
                                + "administrators at {} to receive access "\
                                .format(current_app.config['ADMINS'][0])\
                                + "privileges to view this content."
                    else:
                        self.dmp_status = "Please login to view this content."
                        self.history = "Please login to view this content."
                        self.potential_products = "Please login to view this content."
                    self.file_breakdown = []
                    proj_file_list = []
                    for sbfile in proj.files:
                        proj_file_list.append(sbfile.id)
                    if len(proj_file_list) > 0:
                        file_breakdown_list = db.session.query(
                            SbFile.content_type, db.func.count(
                                SbFile.content_type)).group_by(
                                    SbFile.content_type).filter(
                                        SbFile.id.in_(proj_file_list[:999])).all()  # sqlalchemy max query items is 999
                        proj_file_list[:] = []
                        for _tuple in file_breakdown_list:
                            temp_dict = {}
                            temp_dict['label'] = _tuple[0]
                            temp_dict['count'] = _tuple[1]
                            proj_file_list.append(temp_dict)
                        self.file_breakdown = sorted(
                            proj_file_list,
                            key=lambda k: k['count'],
                            reverse=True)

            elif obj_type == 'fiscal year':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'casc':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'sbfile':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.
            elif obj_type == 'problem item':
                pass  # We don't do anything with fiscal year objects on the
                # front-end yet.

    for project in project_list:
        new_obj = ReportItem(
            'project', project['proj_id'], project['fy_id'], project['casc_id'])
        projects.append(new_obj.__dict__)

    return render_template("treemap.html", projects=projects)

@bp.route('/user/<username>')
@login_required
def user(username):
    """Load user and render user.html template if found, else 404."""
    # Change to lowercase to make case insensitive
    user = User.query.filter_by(username=username.lower()).first_or_404()
    admin_email = current_app.config['ADMINS'][0]
    return render_template('user.html', user=user, adminEmail=admin_email)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Define form for editing a profile."""
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():

        if form.username.data:
            current_user.username = str(form.username.data).lower()
        if form.about.data:
            current_user.about = str(form.about.data)
        if form.email.data:
            current_user.email = str(form.email.data)
        if form.password.data:
            # current_user.password = str(form.password.data)
            user = current_user
            user.set_password(form.password.data)
            db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
        form.email.data = current_user.email

    return render_template(
        'edit_profile.html', title='Edit Profile', form=form)



@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    current_user.search_form = SearchForm()
    d= str(current_user.search_form.data)
    d=d.split(':')
    d=d[1]
    d=d.split(',')
    d=str(d[0])
    d=d.strip("' '")
    print(len(d))

    # Using Project.query.filter('%'+d+'%')
    if(len(d)==0):
        courses=["Please Enter The Keyword To Search"]
        return render_template('search_results.html', courses = courses, length=len(d))

    courses =Project.query.filter(Project.name.like('%'+d+'%')).all()
    length=len(courses)
    print(length)
    print(type(courses))
    return render_template('search_results.html',query=d, courses = courses, length= length)