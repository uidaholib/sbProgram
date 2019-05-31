"""Test module for sb_data_gather package."""
import os
import json

# Run tests as follows: In package directory, run
# python -c "from __init__ import run_tests; run_tests()"
def test_old_v_new_data(app):
    """Test that old and new data match.

    This method determines if the data/database created by the new algorithm
    is accurate compared to the old algorithm and the jsons created by it.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
    Returns:
        True -- (boolean) Returns True if test is passed.
        False -- (boolean) Returns False if test is failed.

    """
    db = app.db
    print("""
    Would you like to use the default test case (NWCASC FY 2012)?
    If not, you must provide your own JSON test case.
          """)
    answer = input("(Y/N): ").lower()
    if not answer[0] == "y":
        print("""
        Please give the path to a fiscal year JSON file to check against:
              """)
        json_path = input("> ")
    else:
        json_path = os.path.abspath(os.path.dirname(__file__))
        json_path = os.path.join(json_path, "test_files/NWCASC_2012.json")
    with open(json_path) as json_file:
        fy_json = json.load(json_file)
    
    # Check for CASC presence in database
    print("Checking CASC name... ", end="")
    casc_name = fy_json["csc"]
    db_casc = db.session.query(app.casc).filter(
        app.casc.name == casc_name).first()
    if db_casc is None:
        casc_name2 = convert_casc_name(casc_name)
        db_casc = db.session.query(app.casc).filter(
            app.casc.name == casc_name).first()
        if db_casc is None:
            print("FAIL")
            print("Error: Could not find '{}' as a CASC in the database."
                .format(casc_name))
            exit(-1)
        else:
            print("PASS (Match-with-conversion: {0} -> {1})"
                  .format(casc_name, db_casc.name))
    else:
        print("PASS (Match: {})".format(db_casc.name))

    # Check that FY of the json exists in database
    fy_name = fy_json["name"]
    print("Checking Fiscal Year presence in both JSON and database... ",
          end="")
    db_fy = db.session.query(app.FiscalYear).filter(app.FiscalYear.sb_id == fy_json["ID"]).first()



def convert_casc_name(old_name):
    """Convert a 'csc' name to a full CASC name.
    
    Arguments:
        old_name -- (string) the old, shortened name of the CSCs before they
                    were CASCs.
    
    Returns:
        new_name -- (string) the new, full length version of old_name in the
                    style used in the database for CASCs.

    """
    if old_name.find("ALASKACSC") != -1:
        old_name = old_name.replace("ALASKACSC", "Alaska CASC")
    elif old_name.find("NCCWSC") != -1:
        old_name = old_name.replace("NCCWSC", "National CASC")
    elif old_name.find("NCCSC") != -1:
        old_name = old_name.replace("NCCSC", "North Central CASC")
    elif old_name.find("NECSC") != -1:
        old_name = old_name.replace("NECSC", "Northeast CASC")
    elif old_name.find("NWCSC") != -1:
        old_name = old_name.replace("NWCSC", "Northwest CASC")
    elif old_name.find("PacificCSC") != -1:
        old_name = old_name.replace("PacificCSC", "Pacific Islands CASC")
    elif old_name.find("SCCSC") != -1:
        old_name = old_name.replace("SCCSC", "South Central CASC")
    elif old_name.find("SECSC") != -1:
        old_name = old_name.replace("SECSC", "Southeast CASC")
    elif old_name.find("SWCSC") != -1:
        old_name = old_name.replace("SWCSC", "Southwest CASC")

    return old_name


def test_correct_projects(app, fy_json):
    """Test that projects were added correctly to db compared to an old json.
    
    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fy_json -- (json) a json created from a SbFiscalYear class (defined in gl.py) that represents a single fiscal year.
    Returns:
        True -- (boolean) Returns True if test is passed.
        False -- (boolean) Returns False if test is failed.

    """
    casc_name = fy_json["csc"]
    fy_name = fy_json[""]


def test_relations(app, fy_json):
    """Test that relationships within the database are functioning properly.

    Arguments:
        app -- (App class) As defined in the package's __init__.py, the class
               gives access to the application instance, the database, and the
               db models.
        fy_json -- (json) a json created from a SbFiscalYear class (defined in gl.py) that represents a single fiscal year.
    Returns:
        True -- (boolean) Returns True if all tests are passed.
        False -- (boolean) Returns False if any tests are failed.

    """