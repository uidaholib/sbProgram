from google.oauth2 import service_account
import gspread

# SCOPES = [
#     'https://spreadsheets.google.com/feeds',
#     'https://www.googleapis.com/auth/drive',
#     'https://www.googleapis.com/auth/spreadsheets.readonly'
# ]
# SERVICE_ACCOUNT_FILE = 'sbmacro-214622-2cd3a4c8b25b.json'

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)

from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(credentials)

def main():
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(
        "CASC Data Management Tracking for Projects - v2").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)

if __name__ == "__main__":
    main()