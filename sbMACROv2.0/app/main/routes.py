"""Define main application routes."""
import os, sys
from datetime import datetime
from collections import OrderedDict
from flask import render_template, redirect, url_for, request, \
    jsonify, current_app, session
from flask_login import current_user, login_required
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms import BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, Email
from wtforms.validators import Optional
from app import db
from app.main.forms import EditProfileForm, FyForm
from app.models import User, casc, FiscalYear, Project, Item, SbFile
from app.main import bp
from app.auth.read_sheets import API_SERVICE_NAME,\
        API_VERSION, get_sheet_name, parse_values, SPREADSHEET_ID
from app.auth.routes import credentials_to_dict, clear_credentials
import json, jsonpickle

from pprint import pprint


@bp.before_app_request
def before_request():
    """Update user 'last seen' field before each request."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])  # Also accepts
@bp.route('/index', methods=['GET', 'POST'])  # Default
def index():
    """Render splash page for sbMACRO."""
    return(render_template('index.html',
                           **locals(),
                           title="Welcome to sbMACRO"))


@bp.route('/fiscal_years')
@bp.route('/fiscalyears')
@bp.route('/select_fiscalyear', methods=['GET', 'POST'])  # Also accepts
@bp.route('/select_fiscalyears', methods=['GET', 'POST'])  # Default
def fiscalyear():
    """Retrieve Fiscal Years and display for selection by user."""
    cascs = db.session.query(casc).order_by(casc.name).all()
    cascs_and_fys = {}
    fy_list = []
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
            # new_attr_name = curr_casc.name + " " + fy.name
            setattr(F,
                    "fy"+str(fy.id),
                    BooleanField(fy.name))
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


# @bp.route('/try', methods=['GET', 'POST'])  # Also accepts
# def fy():
#     class NewForm(FyForm):
#         pass
#     record = {
#         '1': 'label1',
#         '2': 'label2',
#         '3': 'label3',
#         '4': 'label4'
#     }
#     for key, value in record.items():
#         setattr(NewForm, key, BooleanField(value, id="flush"))
#     form = NewForm()
#     return render_template('try.html', record=record, form=form, title="Good luck")

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
            proj = db.session.query(Project).filter(
                    Project.url == url).first()
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

    return(render_template('projects.html',
                           title="Select Projects to Report"))


@bp.route('/report')
def report():
    """Gather appropriate report information and display."""
    import google.oauth2.credentials
    import googleapiclient.discovery
    if current_user.is_authenticated and current_user.access_level > 0:
        if 'credentials' not in session:
            return redirect(url_for('auth.authorize_google'))


    project_list = session["projects"]
    projects = []
    sheets_dict = {}
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
                            # Load credentials from the session.
                            credentials = google.oauth2.credentials.\
                                Credentials(**session['credentials'])

                            # Build API client
                            service = googleapiclient.discovery.build(
                                API_SERVICE_NAME, API_VERSION,
                                    credentials=credentials)
                            sheet_name = get_sheet_name(self.casc)
                            if sheet_name:
                                try:
                                    sheet = sheets_dict[sheet_name]
                                except KeyError:
                                    print("Sheet not found in sheet_dict")
                                    result = service.spreadsheets().values().get(
                                        spreadsheetId=SPREADSHEET_ID,
                                        range=sheet_name).execute()
                                    values = result.get('values', [])
                                    sheet = parse_values(values)
                                    sheets_dict[sheet_name] = sheet
                            else:
                                sheet = {}

                            # Save credentials back to session in case access
                            #   token was refreshed.
                            # ACTION ITEM: In a production app, you likely
                            #       want to save these credentials in a
                            #       persistent database instead.
                            session['credentials'] = credentials_to_dict(credentials)

                            try:
                                # DMP Status
                                self.dmp_status = sheet[proj.sb_id]\
                                                            ['DMP Status']
                                if self.dmp_status.isspace() or \
                                        self.dmp_status == "":
                                    self.dmp_status = "No DMP status provided"
                            # History
                                self.history = sheet[proj.sb_id]['History']
                                if self.history.isspace() or \
                                        self.history == "":
                                    self.history = \
                                            "No data steward history provided"
                            #Potential Products
                                self.potential_products = sheet[proj.sb_id]\
                                                        ['Expected Products']
                                if self.potential_products.isspace() or \
                                        self.potential_products == "":
                                    self.potential_products = \
                                        "No data potential products provided"
                            except KeyError:
                                self.dmp_status = \
                            "Project not currently tracked by Data Steward"
                                self.history = \
                            "Project not currently tracked by Data Steward"
                                self.potential_products = \
                            "Project not currently tracked by Data Steward"
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
                        self.potential_products = "Please login to view this"\
                                                  + " content."
                    self.file_breakdown = []
                    proj_file_list = []
                    for sbfile in proj.files:
                        proj_file_list.append(sbfile.id)
                    if len(proj_file_list) > 0:
                        file_breakdown_list = db.session.query(
                            SbFile.content_type, db.func.count(
                                SbFile.content_type)).group_by(
                                    SbFile.content_type).filter(
                                        SbFile.id.in_(proj_file_list[:999])).all()
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
        new_obj = ReportItem('project',
                             project['proj_id'],
                             project['fy_id'],
                             project['casc_id'])
        projects.append(new_obj.__dict__)


    # clear_credentials()
    return render_template("report.html", projects=projects)


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
            current_user.password = str(form.password.data)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
        form.email.data = current_user.email

    return render_template(
        'edit_profile.html', title='Edit Profile', form=form)
