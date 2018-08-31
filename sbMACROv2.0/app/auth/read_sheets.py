import os
import flask
import requests

import google.oauth2.credentials
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = 'auth.client_secret_web_service.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SPREADSHEET_ID = '1gj0MqRLBYJeWjSTb_nKMiuYdc_2RDXVxBBKOyKpQ00Q'


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



def parse_values(values):
    """Create a new dictionary version from the sheet values passed in.

    Arguments:
        values -- (list) a 2d list of values from the google sheet
    Returns:
        new_sheet -- (dictionary) a dictionary representation of 'values'

    """
    from pprint import pprint
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
    # print("New Sheet:")
    # print(new_sheet)
    return new_sheet
