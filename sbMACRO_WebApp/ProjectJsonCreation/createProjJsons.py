import json
from pprint import pprint
import os, shutil
import pysb

sb = pysb.SbSession()

def main():
    # import our Google Sheet
    GoogleSheetJson = json.load(open('../GoogleSheetsInteraction/GoogleSheet.json'))
    # pprint(GoogleSheetJson)

    #delete all old project jsons

    projFolder = '../jsonCache/Projects'
    for the_file in os.listdir(projFolder):
        file_path = os.path.join(projFolder, the_file)
        try:
            if os.path.isfile(file_path):
                if file_path.endswith("sample.json"):
                    continue
                elif file_path.endswith(".json"):
                    os.unlink(file_path)
            #uncomment if you want directories deleted as well:
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    print("Done Deleting old Project files")
    fyFolder = "../jsonCache"
    for the_file in os.listdir(fyFolder):
        filePath = os.path.join(fyFolder, the_file)
        print(filePath)  # Quantico
        try:
            if os.path.isfile(filePath):
                print("...is file")
                if filePath.endswith(".json"):
                    with open(filePath) as json_data:
                            currFY = json.load(json_data)
                            print('currFY file: ' + the_file)
                            # pprint(currFY)
                            try:
                                for i in currFY['report']:
                                    createProjFile(GoogleSheetJson, currFY, i)
                            except KeyError as e:
                                print(e)
                                print("Not a FY json")
            #uncomment if you want directories inside jsonCache to be searched as well:
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            else:
                print("...is not file")
        except Exception as e:
            print(e)
                    

def createProjFile(GSheet, currFY, proj):
    projJson = {}
    projJson['Date'] = currFY['Date']
    projID = proj['ID']
    projJson['identity'] = {}
    projIdentity = projJson['identity']
    projIdentity['CSC'] = currFY['identity']["CSC"]
    projIdentity['ID'] = projID
    projIdentity['FY'] = proj['FY']
    projJson['title'] = proj["name"]
    projJson['URL'] = proj['URL']
    projJson['Files'] = proj['ProjectFileDict']
    projJson['Items'] = proj['ProjectItems']
    sbProjJson = sb.get_item(projID)
    # pprint(sbProjJson)
    projJson['summary'] = sbProjJson['summary']
    projJson['contacts'] = sbProjJson['contacts']
    try:
        gHistory = GSheet[projID]['History']
        if gHistory.isspace(): # checks if the string has any characters other than blank space. If true (only whitespace exists), default text is added, otherwise, the text is added.
            projJson['history'] = "No data steward history provided"
        else:
            projJson['history'] = gHistory
        gDMP = GSheet[projID]['DMP Status']
        if gDMP.isspace():  # checks if the string has any characters other than blank space. If true (only whitespace exists), default text is added, otherwise, the text is added.
            projJson['DMP'] = "No DMP status provided"
        else:
            projJson['DMP'] = gDMP
        gPProducts= GSheet[projID]['Expected Products']
        if gPProducts.isspace():  # checks if the string has any characters other than blank space. If true (only whitespace exists), default text is added, otherwise, the text is added.
            projJson['Potential_Products'] = "No DMP status provided"
        else:
            projJson['Potential_Products'] = gPProducts
    except KeyError as e:
        projJson['history'] = "Project not currently tracked by Data Steward"
        projJson['DMP'] = "Project not currently tracked by Data Steward"
        projJson['Potential_Products'] = "Project not currently tracked by Data Steward"

    try:
        projJson['Received_Products'] = proj['project_children']
    except:
        projJson['Received_Products'] = "Not yet implemented"
    with open('../jsonCache/Projects/'+projID+'.json', 'w') as sheet:
        json.dump(projJson, sheet)

    # GoogleSheetJson = whatever
    # go through each FY in jsonCache directory
    #     currFY = json file
    #     for i in currFY['report']
    #         projJson = {}
    #         projJson['Date'] = currFy['Date']
    #         sbProjJson = whatever I need here
    #         projID = i['ID']
    #         projJson['identity'] = {
    #             'CSC': currFY['identity']["CSC"]
    #             'ID': i['ID']
    #             'FY': i['FY']
    #         }
    #         projJson['title'] = i["name"]
    #         projJson['URL'] = i['URL']
    #         projJson['summary'] = sbProjJson['summary']
    #         projJson['Primary_Investigator'] = sbProjJson["Primary_Investigator"]
    #         projJson['history'] = GoogleSheetJson[projID]['History']
            # projJson['DMP'] = GoogleSheetJson[projID]['DMP Status']
            # projJson['Potential_Products'] = GoogleSheetJson[projID]['Expected Products']
            
    #         save as projID + ".json"



if __name__ == "__main__":
    main()
