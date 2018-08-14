"""Module contianing functions for saving FYs, Projects, etc. to a db."""
from datetime import datetime
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
    casc = app.db.session.query(app.casc).filter(
           app.casc.sb_id == sb_id).first()
    # casc = app.casc.query.filter_by(sb_id=sb_id).first()
    if casc is None:  # casc is not in the db and must be created
        print("---------SQL--------- [casc] Could not find {} in database..."
              .format(name))
        casc = app.casc(sb_id=sb_id,
                        name=name,
                        url=url,
                        total_data=-1)  # Reset so we know it needs done.
        app.db.session.add(casc)
    else:
        print("---------SQL--------- [casc] Found {} in database..."
              .format(name))
        if casc.sb_id != sb_id:
            casc.sb_id = sb_id
        if casc.name != name:
            casc.name = name
        if casc.url != url:
            casc.url = url
        casc.total_data = -1  # Reset so we know it needs done.
    app.db.session.commit()
    print("---------SQL--------- [casc] Done with {}.".format(name))
    return casc


def save_fy(app, fiscal_year, casc_model):
    """Save Fiscal Year data to a database.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fiscal_year -- (SbFiscalYear) A completed SbFiscalYear object (defined
                       in 'gl.py') to be parsed and saved to the database.
        casc_model -- (casc model) As defined in `models.py`, the casc_model
                      is a database model class.
    Returns:
        fy -- (fy model) As defined in `models.py`, the fy is a
                database model class.

    """
    # casc_model = app.casc.query.filter_by(id=casc_model).first()
    fy = app.db.session.query(app.FiscalYear).filter(
         app.FiscalYear.sb_id == fiscal_year.ID).first()
    # fy = app.FiscalYear.query.filter_by(sb_id=fiscal_year.ID).first()
    if fy is None:  # The Fiscal Year was not found in the db
        print("---------SQL--------- [FiscalYear] Could not find " +
              "{} in database...".format(fiscal_year.name))
        fy = app.FiscalYear(sb_id=fiscal_year.ID,
                            url=fiscal_year.URL,
                            name=fiscal_year.name,
                            total_data=fiscal_year.total_fy_data,
                            # Backrefs (need db model):
                            casc_id=casc_model.id)
        app.db.session.add(fy)
    else:
        print("---------SQL--------- [FiscalYear] Found {} in database..."
              .format(fiscal_year.name))
        if fy.sb_id != fiscal_year.ID:
            fy.sb_id = fiscal_year.ID
        if fy.name != fiscal_year.name:
            fy.name = fiscal_year.name
        if fy.url != fiscal_year.URL:
            fy.url = fiscal_year.URL
        if fy.total_data != fiscal_year.total_fy_data:
            fy.total_data = fiscal_year.total_fy_data
        # Backrefs (need db model):
        if fy.casc_id != casc_model.id:
            fy.casc_id = casc_model.id

        # Add new timestamp
        fy.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("---------SQL--------- [FiscalYear] Done with {}."
          .format(fiscal_year.name))
    return fy



def save_proj(app, project, fy_model, casc_model):
    """Save Project data to a database.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        project -- (SbProject) A completed SbFiscalYear object (defined in
                   'gl.py') to be parsed and saved to the database.
        fy_model -- (FiscalYear model) As defined in `models.py`, the fy_model
                    is a database model class.
        casc_model -- (casc model) As defined in `models.py`, the casc_model
                      is a database model class.
    Returns:
        proj -- (Project model) As defined in `models.py`, the proj is a
                database model class.

    """
    # casc_model = app.casc.query.filter_by(id=casc_model).first()
    # fy_model = app.FiscalYear.query.filter_by(id=fy_model).first()

    proj = app.db.session.query(app.Project).filter(
           app.Project.sb_id == project.ID).first()
    if proj is None:  # The Fiscal Year was not found in the db
        print("---------SQL--------- [Project] Could not find " +
              "{} in database...".format(project.name))
        proj = app.Project(sb_id=project.ID,
                           url=project.URL,
                           name=project.name,
                           total_data=project.data_in_project,
                           item_count=project.project_items\
                                              ["Project_Item_Count"],
                           file_count=project.project_files\
                                              ["Project_File_Count"],
                           start_date=get_sb_date("start", project),
                           end_date=get_sb_date("end", project),
                           # Backrefs (need db model):
                           casc_id=casc_model.id,
                           fy_id=fy_model.id)
        app.db.session.add(proj)
    else:
        print("---------SQL--------- [Project] Found {} in database..."
              .format(project.name))
        if proj.sb_id != project.ID:
            proj.sb_id = project.ID
        if proj.name != project.name:
            proj.name = project.name
        if proj.url != project.URL:
            proj.url = project.URL
        if proj.total_data != project.data_in_project:
            proj.total_data = project.data_in_project
        if proj.item_count != project.project_items["Project_Item_Count"]:
            proj.item_count = project.project_items["Project_Item_Count"]
        if proj.file_count != project.project_files["Project_File_Count"]:
            proj.file_count = project.project_files["Project_File_Count"]
        proj.start_date = get_sb_date("start", project)
        proj.end_date = get_sb_date("end", project)

        # Backrefs (need db model):
        if proj.casc_id != casc_model.id:
            proj.casc_id = casc_model.id
        if proj.fy_id != fy_model.id:
            proj.fy_id = fy_model.id

        # Add new timestamp
        proj.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("---------SQL--------- [Project] Done with {}.".format(proj.name))
    return proj


def get_sb_date(date_type, project):
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
    try:
        for i in project.sb_json["dates"]:
            if i['type'].lower() == date_type:
                return i["dateString"]
        return "No " + date_type + " date provided."
    except KeyError:
        return "No " + date_type + " date provided."


def save_item(app, sb_item, proj_model, fy_model, casc_model):
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
        casc_model -- (casc model) As defined in `models.py`, the casc_model
                      is a database model class.
    Returns:
        item -- (Item model) As defined in `models.py`, the item is a
                database model class.

    """
    # casc_model = app.casc.query.filter_by(id=casc_model).first()
    # fy_model = app.FiscalYear.query.filter_by(id=fy_model).first()
    # proj_model = app.Project.query.filter_by(id=proj_model).first()

    item = app.db.session.query(app.Item).filter(
           app.Item.sb_id == sb_item.ID).first()
    # item = app.Item.query.filter_by(sb_id=sb_item.ID).first()
    if item is None:  # The Fiscal Year was not found in the db
        print("---------SQL--------- [Item] Could not find " +
              "{} in database...".format(sb_item.name))
        item = app.Item(sb_id=sb_item.ID,
                        url=sb_item.URL,
                        name=sb_item.name,
                        #Convert bytes to megabytes:
                        total_data=(sb_item.size/1000000),
                        file_count=sb_item.num_files,
                        start_date=get_sb_date("start", sb_item),
                        end_date=get_sb_date("end", sb_item),
                        # Backrefs (need db model):
                        casc_id=casc_model.id,
                        fy_id=fy_model.id,
                        proj_id=proj_model.id)
        app.db.session.add(item)
    else:
        print("---------SQL--------- [Item] Found {} in database..."
              .format(sb_item.name))
        if item.sb_id != sb_item.ID:
            item.sb_id = sb_item.ID
        if item.name != sb_item.name:
            item.name = sb_item.name
        if item.url != sb_item.URL:
            item.url = sb_item.URL
        if item.total_data != sb_item.size:
            item.total_data = sb_item.size
        if item.file_count != sb_item.num_files:
            item.file_count = sb_item.num_files
        item.start_date = get_sb_date("start", sb_item)
        item.end_date = get_sb_date("end", sb_item)

        # Backrefs (need db model):
        if item.casc_id != casc_model.id:
            item.casc_id = casc_model.id
        if item.fy_id != fy_model.id:
            item.fy_id = fy_model.id
        if item.proj_id != proj_model.id:
            item.proj_id = proj_model.id

        # Add new timestamp
        item.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("---------SQL--------- [Item] Done with {}.".format(item.name))
    return item


def save_file(app, file_json, item_model, proj_model, fy_model, casc_model):
    """Save Project data to a database.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        file_json -- (dictionary) The Science Base json for a file.
        item_model -- (Item model) As defined in `models.py`, the item_model
                      is a database model class.
        proj_model -- (Project model) As defined in `models.py`, the proj_model
                    is a database model class.
        fy_model -- (FiscalYear model) As defined in `models.py`, the fy_model
                    is a database model class.
        casc_model -- (casc model) As defined in `models.py`, the casc_model
                      is a database model class.
    Returns:
        sb_file -- (SbFile model) As defined in `models.py`, the sb_file is a
                database model class.

    """
    # casc_model = app.casc.query.filter_by(id=casc_model).first()
    # fy_model = app.FiscalYear.query.filter_by(id=fy_model).first()
    # proj_model = app.Project.query.filter_by(id=proj_model).first()
    # item_model = app.Item.query.filter_by(id=item_model).first()
    # Since there is not science base id for a file, url is best to find it:
    sb_file = app.db.session.query(app.Item).filter(
              app.Item.url == file_json["url"]).first()
    # sb_file = app.Item.query.filter_by(url=file_json["url"]).first()
    if sb_file is None:  # The Fiscal Year was not found in the db
        print("\t\t---------SQL--------- [SbFile] Could not find " +
              "{} in database...".format(sb_file["name"]))
        sb_file = app.Item(url=file_json["url"],
                           name=file_json["name"],
                           # Convert bytes to megabytes:
                           size=(file_json["size"]/1000000),
                           date_uploaded=file_json["dateUploaded"],
                           content_type=file_json["contentType"],
                           # Backrefs (need db model):
                           casc_id=casc_model.id,
                           fy_id=fy_model.id,
                           proj_id=proj_model.id,
                           item_id=item_model.id)
        app.db.session.add(sb_file)
    else:
        print("\t\t---------SQL--------- [SbFile] Found {} in database..."
              .format(sb_file["name"]))
        if sb_file.name != file_json["name"]:
            sb_file.name = file_json["name"]
        if sb_file.url != file_json["url"]:
            sb_file.url = file_json["url"]
        if sb_file.size != file_json["size"]:
            sb_file.size = file_json["size"]
        if sb_file.date_uploaded != file_json["dateUploaded"]:
            sb_file.date_uploaded = file_json["dateUploaded"]
        if sb_file.content_type != file_json["contentType"]:
            sb_file.content_type = file_json["contentType"]

        # Backrefs (need db model):
        if sb_file.casc_id != casc_model.id:
            sb_file.casc_id = casc_model.id
        if sb_file.fy_id != fy_model.id:
            sb_file.fy_id = fy_model.id
        if sb_file.proj_id != proj_model.id:
            sb_file.proj_id = proj_model.id
        if sb_file.proj_id != proj_model.id:
            sb_file.proj_id = proj_model.id
        if sb_file.item_id != item_model.id:
            sb_file.item_id = item_model.id

        # Add new timestamp
        sb_file.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("---------SQL--------- [SbFile] Done with {}.".format(sb_file.name))
    return sb_file
