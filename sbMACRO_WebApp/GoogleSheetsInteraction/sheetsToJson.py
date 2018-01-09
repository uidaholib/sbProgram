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
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
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
                                   'sheets.googleapis.com-python-quickstart.json')

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


def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    # get_sheet_id(service)
    spreadsheetId = "1hapPsfgaku32eK7dJdN4Rx0LnjF5LLBxCUtbxX0JlJQ"
    sheet = "Sheet1"
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=sheet).execute()
        values = result.get('values', [])
    except:
        print("Sheets API Query failed.")
        exit(0)
    parseValues(values)

def parseValues(values):
    newSheet = {}
    header = values[0]
    values = values[1:]  # Shave off the first item (header)

    for i in values:
        projID = i[2]
        folderURL = "https://www.sciencebase.gov/catalog/folder/"
        itemURL = "https://www.sciencebase.gov/catalog/item/"
        if folderURL in projID:
            projID = projID.replace(folderURL, '')
        if itemURL in projID:
            projID = projID.replace(itemURL, '')
        if '/' in projID:
            projID = projID.replace('/', '') # in case there is a trailing slash
        newSheet[projID] = {}
        for n in range(0, len(header)):
            headerVal = header[n]
            try:
                valVal = i[n]
            except IndexError:
                valVal = "No Info Provided"
            # print(headerVal)
            # print(valVal)
            newSheet[projID][headerVal] = valVal
    print("new Sheet:")
    print(newSheet)
    with open('GoogleSheet.json', 'w') as sheet:
        json.dump(newSheet, sheet)

    

if __name__ == "__main__":
    main()
