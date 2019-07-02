"""Module contianing functions for saving FYs, Projects, etc. to a db."""
from datetime import datetime
from app.updater import gl
from app.updater import fiscal_years
from app.models import MasterDetails, ProjectDetails

def save_master_details(app, item_details):
    """Save item details relevant to searching..

    Arguments:
        item_details -- (List) A list of items, where each item is a dictionary containing
                        item fields and values.
    """
    print('Saving master details to database...')
    changes_made = False
    errors = set()

    for detail in item_details:
        try:
            sb_id = detail['id']
            parentId = detail['parentId']
            projectId = detail['proj_id']
            casc = detail['casc']
            fy = detail['FY']
            url = detail['url']
            relatedItemsUrl = detail['relatedItemsUrl']
            title = detail['title']
            hasChildren = detail['hasChildren']
            summary = detail['summary']
            PI = ''
            CI = ''
            for contact in detail['contacts']:
                if contact['type'] == 'Principal Investigator':
                    PI = contact['name']
                elif contact['type'] in ['Co-Investigator', 'Cooperator/Partner']:
                    CI += contact['name'] + ';'
            CI = CI.strip(';')

            detail_row = MasterDetails(sb_id = sb_id,
                                        parentId = parentId,
                                        projectId = projectId,
                                        casc = casc,
                                        fy = fy,
                                        url = url,
                                        relatedItemsUrl = relatedItemsUrl,
                                        title = title,
                                        hasChildren = hasChildren,
                                        summary = summary,
                                        PI = PI,
                                        CI = CI)
            app.db.session.add(detail_row)
            changes_made = True
        except Exception as e:
            errors.add(e)
    
    if changes_made:
        app.db.session.commit()
        print('Master details saved to database')

        # print('Testing items...')
        # test = app.db.session.query(app.MasterDetails).filter(app.MasterDetails.sb_id == '50f8472de4b0faa3ef21ecb6').first()
        # if test is None:
        #     print('nope!')
        #     print('Done')
        # else:
        #     print('Success:')
        #     print(test.casc)
        #     print(test.fy)
        #     print(test.title)
        #     print('Done!')
    else:
        print('Errors encountered:')
        for e in errors:
            print(e)


def save_project_details(app, proj_details):
    """Save project details relevant to searching..

    Arguments:
        proj_details -- (List) A list of projects, where each project is a dictionary containing
                        project fields and values.
    """
    print('Saving project details to database...')
    changes_made = False
    errors = set()

    for detail in proj_details:
        try:
            sb_id = detail['id']
            casc = detail['casc']
            fy = detail['fy']
            title = detail['title']
            size = detail['size']

            detail_row = ProjectDetails(sb_id = sb_id,
                                        casc = casc,
                                        fy = fy,
                                        title = title,
                                        size = size)
            app.db.session.add(detail_row)
            changes_made = True
        except Exception as e:
            errors.add(e)
    
    if changes_made:
        app.db.session.commit()
        print('Project details saved to database')

        # print('Testing projects...')
        # test = app.db.session.query(app.ProjectDetails).filter(app.ProjectDetails.sb_id == '4f833dabe4b0e84f608680d5').first()
        # if test is None:
        #     print('nope!')
        #     print('Done')
        # else:
        #     print('Success:')
        #     print(test.casc)
        #     print(test.fy)
        #     print(test.title)
        #     print('Done!')
    else:
        print('Errors encountered:')
        for e in errors:
            print(e)


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
              .format(name.encode('utf-8')))
        casc = app.casc(sb_id=sb_id,
                        name=name,
                        url=url,
                        total_data=-1)  # Reset so we know it needs done.
        app.db.session.add(casc)
    else:
        print("---------SQL--------- [casc] Found {} in database..."
              .format(name.encode('utf-8')))
        if casc.sb_id != sb_id:
            casc.sb_id = sb_id
        if casc.name != name:
            casc.name = name
        if casc.url != url:
            casc.url = url
        casc.total_data = -1  # Reset so we know it needs done.
    app.db.session.commit()
    print("---------SQL--------- [casc] Done with {}.".format(name.encode('utf-8')))
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
              "{} in database...".format(fiscal_year.name.encode('utf-8')))
        fy = app.FiscalYear(sb_id=fiscal_year.ID,
                            url=fiscal_year.URL,
                            name=fiscal_year.name,
                            total_data=fiscal_year.total_fy_data,
                            # Backrefs (need db model):
                            casc_id=casc_model.id)
        app.db.session.add(fy)
    else:
        print("---------SQL--------- [FiscalYear] Found {} in database..."
              .format(fiscal_year.name.encode('utf-8')))
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
          .format(fiscal_year.name.encode('utf-8')))
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
              "{} in database...".format(project.name.encode('utf-8')))
        pi_list = get_pi_list(app, project.sb_json)
        proj = app.Project(sb_id=project.ID,
                           url=project.URL,
                           name=project.name,
                           total_data=project.data_in_project,
                           item_count=project.project_items\
                                              ["Project_Item_Count"],
                           file_count=project.project_files\
                                              ["Project_File_Count"],
                           start_date=get_sb_date("start", project.sb_json),
                           end_date=get_sb_date("end", project.sb_json),
                           summary=project.sb_json['summary'])
        # Many-to-many relationship definitions:
        proj.cascs.append(casc_model)
        proj.fiscal_years.append(fy_model)
        for pi_model in pi_list:
            proj.principal_investigators.append(pi_model)
        app.db.session.add(proj)
    else:
        print("---------SQL--------- [Project] Found {} in database..."
              .format(project.name.encode('utf-8')))
        pi_list = get_pi_list(app, project.sb_json)
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
        proj.start_date = get_sb_date("start", project.sb_json)
        proj.end_date = get_sb_date("end", project.sb_json)
        if proj.summary != project.sb_json['summary']:
            proj.summary = project.sb_json['summary']

        # Many-to-many relationships (need db model):
        # Check if the casc is already related to the project by iterating
        # through proj.cascs and seeing if the ids match. If not found, add it.
        if not (any(casc.id == casc_model.id for casc in proj.cascs)):
            proj.cascs.append(casc_model)
        if not (any(fy.id == fy_model.id for fy in proj.fiscal_years)):
            proj.fiscal_years.append(fy_model)
        for pi_model in pi_list:
            if not (any(pi.id == pi_model.id for pi in \
                            proj.principal_investigators)):
                proj.principal_investigators.append(pi_model)

        # Add new timestamp
        proj.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("---------SQL--------- [Project] Done with {}.".format(proj.name.encode('utf-8')))
    return proj


def get_pi_list(app, project):
    """Create/gather list of Principal Investigators for a project.

    Arguments:
        project -- (JSON) the Science Base JSON for a project item.
    
    Returns:
        pi_list -- (list) a list of PrincipalInvestigator models (defined in
                   models.py) that are related to the project.

    """
    pi_list = []
    for person in project['contacts']:
        try:
            if person['type'].lower() == "principal investigator":
                PI = app.db.session.query(app.PI).filter(
                    app.PI.name == person['name']).first()
                try:
                    email = person['email']
                except KeyError:
                    email = None
                # Update/Create PI:
                if PI is None:
                    PI = app.PI(name=person['name'],
                                email=email)
                    app.db.session.add(PI)
                else:
                    if PI.name != person['name']:
                        PI.name = person['name']
                    if PI.email != email:
                        PI.email = email
                app.db.session.commit()
                pi_list.append(PI)
                if PI.name == "Scott Rupp":
                    print("""
                    
                    
                    
                    
                    
                    
                    
                    
                    Name: {0}
                    Email: {1}
                    email variable: {2}
                    """.format(PI.name.encode('utf-8'), PI.email.encode('utf-8'), email.encode('utf-8')))
                    exit(0)
        except KeyError:
            continue
    return pi_list


def get_sb_date(date_type, sb_json):
    """Get start of end date of a project.

    Arguments:
        date_type -- (string) "start", "end", or "publication" will cause the
                     function to search for either the start, end, or
                     publication date, respectively, of the project.
        sb_json -- (json) A science base json representing a science base file
                   to be parsed and saved to the database.
    Returns:
        (string) A date string for either the start or end date of a project,
        or a sting that says there was none provided.

    """
    try:
        for i in sb_json["dates"]:
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
              "{} in database...".format(sb_item.name.encode('utf-8')))
        item = app.Item(sb_id=sb_item.ID,
                        url=sb_item.URL,
                        name=sb_item.name,
                        #Convert bytes to megabytes:
                        total_data=(sb_item.size/1000000),
                        file_count=sb_item.num_files,
                        start_date=get_sb_date("start", sb_item.sb_json),
                        end_date=get_sb_date("end", sb_item.sb_json),
                        pub_date=get_sb_date("publication", sb_item.sb_json))
        # Many-to-many relationship definitions:
        item.cascs.append(casc_model)
        item.fiscal_years.append(fy_model)
        item.projects.append(proj_model)
        app.db.session.add(item)
    else:
        print("---------SQL--------- [Item] Found {} in database..."
              .format(sb_item.name.encode('utf-8')))
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
        item.start_date = get_sb_date("start", sb_item.sb_json)
        item.end_date = get_sb_date("end", sb_item.sb_json)
        item.pub_date = get_sb_date("publication", sb_item.sb_json)

        # Many-to-many relationships (need db model):
        if not (any(casc.id == casc_model.id for casc in item.cascs)):
            item.cascs.append(casc_model)
        if not (any(fy.id == fy_model.id for fy in item.fiscal_years)):
            item.fiscal_years.append(fy_model)
        if not (any(proj.id == proj_model.id for proj in item.projects)):
            item.projects.append(proj_model)

        # Add new timestamp
        item.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("---------SQL--------- [Item] Done with {}.".format(item.name.encode('utf-8')))
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
    sb_file = app.db.session.query(app.SbFile).filter(
              app.SbFile.url == file_json["url"]).first()
    # sb_file = app.Item.query.filter_by(url=file_json["url"]).first()
    if sb_file is None:  # The Fiscal Year was not found in the db
        print("\t\t---------SQL--------- [SbFile] Could not find " +
              "{} in database...".format(file_json["name"].encode('utf-8')))
        sb_file = app.SbFile(url=file_json["url"],
                           name=file_json["name"],
                           # Convert bytes to megabytes:
                           size=(file_json["size"]/1000000),
                           content_type=file_json["contentType"])
        # Many-to-many relationship definitions:
        sb_file.cascs.append(casc_model)
        sb_file.fiscal_years.append(fy_model)
        sb_file.projects.append(proj_model)
        sb_file.items.append(item_model)
        app.db.session.add(sb_file)
    else:
        print("\t\t---------SQL--------- [SbFile] Found {} in database..."
              .format(file_json["name"].encode('utf-8')))
        if sb_file.name != file_json["name"]:
            sb_file.name = file_json["name"]
        if sb_file.url != file_json["url"]:
            sb_file.url = file_json["url"]
        if sb_file.size != file_json["size"]:
            sb_file.size = file_json["size"]
        if sb_file.content_type != file_json["contentType"]:
            sb_file.content_type = file_json["contentType"]

        # Many-to-many relationships (need db model):
        if not (any(casc.id == casc_model.id for casc in sb_file.cascs)):
            sb_file.cascs.append(casc_model)
        if not (any(fy.id == fy_model.id for fy in sb_file.fiscal_years)):
            sb_file.fiscal_years.append(fy_model)
        if not (any(proj.id == proj_model.id for proj in sb_file.projects)):
            sb_file.projects.append(proj_model)
        if not (any(item.id == item_model.id for item in sb_file.items)):
            sb_file.items.append(item_model)

        # Add new timestamp
        sb_file.timestamp = datetime.utcnow()

    app.db.session.commit()
    print("\t\t---------SQL--------- [SbFile] Done with {}."
          .format(sb_file.name.encode('utf-8')))
    return sb_file
