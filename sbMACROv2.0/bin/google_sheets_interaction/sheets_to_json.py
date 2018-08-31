#from __future__ import print_function
import httplib2
import os
from sys import exit
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-sbmacro-python.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API sbMacro Interaction'



def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-sbmacro-python.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_sheet_name(casc):
    """Return sheet name for provided CASC.
    
    Arguments:
        casc -- (string) The string name of a CASC
    Returns:
        sheet_name -- (string) the name of the corresponding sheet.

    """
    if casc.lower() == "Northwest CASC".lower():
        sheet_name = "NW"
    elif casc.lower() == "Southwest CASC".lower():
        sheet_name = "SW"
    elif casc.lower() == "Pacific Islands CASC".lower():
        sheet_name = "PI"
    else:
        return None
    return sheet_name


def main(casc):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object.

    Arguments:
        casc -- (string) The string name of a CASC
    Returns:
        paseValues(values) -- (dictionary) returned object from parse_values()

    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discovery_url)
    # get_sheet_id(service)
    spreadsheet_id = "1gj0MqRLBYJeWjSTb_nKMiuYdc_2RDXVxBBKOyKpQ00Q"
    sheet = get_sheet_name(casc) + "!"
    try:
        result = service.spreadsheets().values().get(
            spreadsheet_id=spreadsheet_id, range=sheet).execute()
        values = result.get('values', [])
    except:
        print("Sheets API Query failed.")
        exit(0)
    return parse_values(values)

def parse_values(values):
    """Create a new dictionary version from the sheet values passed in.

    Arguments:
        values -- (list) a 2d list of values from the google sheet
    Returns:
        new_sheet -- (dictionary) a dictionary representation of 'values'

    """
    new_sheet = {}
    header = values[0]
    values = values[1:]  # Shave off the first item (header)

    for i in values:
        proj_id = i[2]
        folder_url = "https://www.sciencebase.gov/catalog/folder/"
        item_url = "https://www.sciencebase.gov/catalog/item/"
        if folder_url in proj_id:
            proj_id = proj_id.replace(folder_url, '')
        if item_url in proj_id:
            proj_id = proj_id.replace(item_url, '')
        if '/' in proj_id:
            proj_id = proj_id.replace('/', '') # in case there is a trailing slash
        new_sheet[proj_id] = {}
        for n in range(0, len(header)):
            headerVal = header[n]
            try:
                val_val = i[n]
            except IndexError:
                val_val = "No Info Provided"
            # print(headerVal)
            # print(val_val)
            new_sheet[proj_id][headerVal] = val_val
    print("New Sheet:")
    print(new_sheet)
    # with open('GoogleSheet.json', 'w') as sheet:
    #     json.dump(new_sheet, sheet)
    return new_sheet
