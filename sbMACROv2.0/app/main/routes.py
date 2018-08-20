"""Define main application routes."""
from datetime import datetime
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
import json

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
        print("Form submitted!")
        id_list = []
        projects = []
        for fy in list_fy:
            fy_attr = getattr(form, fy)
            selected = fy_attr.data
            # print("{0} selected: {1}".format(fy, selected))
            if selected:
                id_list.append(fy.replace("fy", ""))
        # print("id_list:")
        for i in id_list:
            # print("\t{}".format(i))
            fy_projs = db.session.query(Project).filter(
                Project.fiscal_years.any(id=i)).all()
            # print("\tProjects:")
            for proj in fy_projs:
                # print("\t\t{}".format(proj.id))
                projects.append(proj.id)

        session["projects"] = projects
        return redirect(url_for('main.report'))
    elif request.method == 'GET':
        pass

    return render_template('fiscalYears.html',
                           form=form,
                           cascs_and_fys=cascs_and_fys,
                           title="Select Fiscal Years")

@bp.route('/try', methods=['GET', 'POST'])  # Also accepts
def fy():
    class NewForm(FyForm):
        pass
    record = {
        '1': 'label1',
        '2': 'label2',
        '3': 'label3',
        '4': 'label4'
    }
    for key, value in record.items():
        setattr(NewForm, key, BooleanField(value, id="flush"))
    form = NewForm()
    return render_template('try.html', record=record, form=form, title="Good luck")

@bp.route('/select_project')
@bp.route('/select_projects')
def project():
    """Display and implement selection/searching for projects by URL."""
    return "Page under construction"


@bp.route('/report')
def report():
    """Gather appropriate report information and display."""
    projects = session["projects"]
    projects2 = []

    return render_template("report.html", projects=projects2)

@bp.route('/user/<username>')
@login_required
def user(username):
    """Load user and render user.html template if found, else 404."""
    # Change to lowercase to make case insensitive
    usr = User.query.filter_by(username=username.lower()).first_or_404()

    return render_template('user.html', user=usr)


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
