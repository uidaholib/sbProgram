"""Module contianing functions for saving FYs, Projects, etc. to a db."""
import gl
import fiscal_years


def save_casc(app, fiscal_year):
    """Save CASC data to a database.
    
    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fiscal_year -- (SbFiscalYear) A completed SbFiscalYear object (defined
                       in 'gl.py') to be parsed and saved to the database.
    Returns:
        casc -- (casc model) As defined in `models.py`, the casc is a
                database model class.

    """
    sb_id, name, url = fiscal_years.get_csc_from_fy_id(fiscal_year.ID, True)
    casc = app.casc.query.filter_by(sb_id=sb_id).first()
    if casc is None:  # casc is not in the db and must be created
        casc = app.casc(sb_id=sb_id,
                        name=name,
                        url=url,
                        total_data=-1)  # Reset so we know it needs done.
        app.db.session.add(casc)
    else:
        if casc.sb_id != sb_id:
            casc.sb_id = sb_id
        if casc.name != name:
            casc.name = name
        if casc.url != url:
            casc.url = url
        casc.total_data = -1  # Reset so we know it needs done.
    app.db.session.commit()
    return casc


def save_fy(app, fiscal_year, casc):
    """Save Fiscal Year data to a database.
    
    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fiscal_year -- (SbFiscalYear) A completed SbFiscalYear object (defined
                       in 'gl.py') to be parsed and saved to the database.
        casc -- (casc model) As defined in `models.py`, the casc is a
                database model class.
    Returns:
        fy -- (fy model) As defined in `models.py`, the fy is a
                database model class.
    """

    fy = app.FiscalYear.query.filter_by(sb_id=fiscal_year.ID).first()
    if fy is None:  # The Fiscal Year was not found in the db
        fy = app.FiscalYear(sb_id=fiscal_year.ID,
                            url=fiscal_year.URL,
                            name=fiscal_year.name,
                            total_data=-1  # Reset so we know it needs done.
                            # Backrefs (need db model):
                            casc_id=casc)
        app.db.session.add(fy)
    else:
        if fy.sb_id != fiscal_year.ID:
            fy.sb_id = fiscal_year.ID
        if fy.name != fiscal_year.name:
            fy.name = fiscal_year.name
        if fy.url != fiscal_year.URL:
            fy.url = fiscal_year.URL
        fy.total_data = -1  # Reset so we know it needs done.
        # Backrefs (need db model):
        if fy.casc != casc:
            fy.casc != casc
    app.db.session.commit()
    return fy



def save_proj(app, project, fy_model, casc):
    """Save Project data to a database.
    
    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        project -- (SbProject) A completed SbFiscalYear object (defined in
                   'gl.py') to be parsed and saved to the database.
        fy_model -- (FiscalYear model) As defined in `models.py`, the fy_model
                    is a database model class.
        casc -- (casc model) As defined in `models.py`, the casc is a
                database model class.
    Returns:
        proj -- (proj model) As defined in `models.py`, the proj is a
                database model class.

    """

    proj = app.Project.query.filter_by(sb_id=project.ID).first()
    if proj is None:  # The Fiscal Year was not found in the db
        proj = app.Project(sb_id=project.ID,
                           url=project.URL,
                           name=project.name,
                           total_data=-1,  # Reset so we know it needs done.
                           item_count=-1,  # Reset so we know it needs done.
                           file_count=-1,  # Reset so we know it needs done.
                           start_date=get_proj_date("start", project),
                           end_date=get_proj_date("end", project),
                           # Backrefs (need db model):
                           casc_id=casc,
                           fy_id=fy_model)
        app.db.session.add(proj)
    else:
        if proj.sb_id != project.ID:
            proj.sb_id = project.ID
        if proj.name != project.name:
            proj.name = project.name
        if proj.url != project.URL:
            proj.url = project.URL
        proj.total_data = -1  # Reset so we know it needs done.
        proj.item_count = -1  # Reset so we know it needs done.
        proj.file_count = -1  # Reset so we know it needs done.
        proj.start_date = get_proj_date("start", project)
        proj.end_date = get_proj_date("end", project)

        # Backrefs (need db model):
        if proj.casc_id != casc:
            proj.casc_id = casc
        if proj.fy_id != fy_model:
            proj.fy_id = fy_model
    app.db.session.commit()
    return proj


def get_proj_date(date_type, project):
    """Get start of end date of a project.

    Arguments:
        date_type -- (string) "start" or "end" will cause the function to
                     search for either the start or end date of the project.
        project -- (SbProject) A completed SbFiscalYear object (defined in
                   'gl.py') to be parsed and saved to the database.
    Returns:
        (string) A date string for either the start or end date of a project,
        or a sting that says there was none provided.

    """
    for i in project.sb_json["dates"]:
        if i['type'].lower() == date_type:
            return i["dateString"]
    return "No " + date_type + " date provided."


def save_item(app, sb_item, proj_model, fy_model, casc):
    """Save Project data to a database.
    
    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        sb_item -- (SbItem) A completed SbItem object (defined in
                   'gl.py') to be parsed and saved to the database.
        proj_model -- (Project model) As defined in `models.py`, the proj_model
                    is a database model class.
        fy_model -- (FiscalYear model) As defined in `models.py`, the fy_model
                    is a database model class.
        casc -- (casc model) As defined in `models.py`, the casc is a
                database model class.
    Returns:
        item_ -- (proj model) As defined in `models.py`, the proj is a
                database model class.

    """

    item = app.Item.query.filter_by(sb_id=sb_item.ID).first()
    if item is None:  # The Fiscal Year was not found in the db
        item = app.Item(sb_id=sb_item.ID,
                           url=sb_item.URL,
                           name=sb_item.name,
                           total_data=-1,  # Reset so we know it needs done.
                           file_count=-1,  # Reset so we know it needs done.
                           start_date=get_proj_date("start", sb_item),
                           end_date=get_proj_date("end", sb_item),
                           # Backrefs (need db model):
                           casc_id=casc,
                           fy_id=fy_model,
                           proj_id=proj_model)
        app.db.session.add(item)
    else:
        if item.sb_id != sb_item.ID:
            item.sb_id = sb_item.ID
        if item.name != sb_item.name:
            item.name = sb_item.name
        if item.url != sb_item.URL:
            item.url = sb_item.URL
        item.total_data = -1  # Reset so we know it needs done.
        item.file_count = -1  # Reset so we know it needs done.
        item.start_date = get_proj_date("start", sb_item)
        item.end_date = get_proj_date("end", sb_item)
        
        # Backrefs (need db model):
        if item.casc_id != casc:
            item.casc_id = casc
        if item.fy_id != fy_model:
            item.fy_id = fy_model
    app.db.session.commit()
    return item