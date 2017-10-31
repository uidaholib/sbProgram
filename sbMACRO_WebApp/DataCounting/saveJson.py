import gl

import os

from pprint import pprint

import requests
import json
import pysb
import jsonpickle

import io  # For the creation of download file in-memory


sb = pysb.SbSession()

class sbItem(object):
    
    def __init__(self):
        self.ID = "No information provided"
        self.ObjectType = "No information provided"
        self.name = "No information provided"
        self.FY = "No information provided"
        self.project = "No information provided"
        self.DataInProject = "No information provided"
        self.DataPerFile = "No information provided"
        self.totalFYData = "No information provided"
        self.RunningDataTotal = "No information provided"

    def Print(self):
        print("""
        ID: {0}
        ObjType: {1}
        Name: {2}
        FY: {3}
        Project: {4}
        DataInProj: {5}
        DataPerFile: {6}
        TotalFYdata: {7}
        RunningTotal: {8}
        """.format(self.ID, self.ObjectType, self.name, self.FY, self.project, 
                   self.DataInProject, self.DataPerFile, self.totalFYData, 
                   self.RunningDataTotal)
        )

    def toJSON(self):
        return(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))


class JsonTransformer(object):
    def transform(self, myObject):
        return jsonpickle.encode(myObject, unpicklable=False)


class problemSBitem(object):

    def __init__(self):
        self.ID = "No information provided"
        self.URL = "No information provided"
    
    def toJSON(self):
        return(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))

def format_to_array_of_arrays_For_Json(report_Dict, sbItemList):
    report_Array = []
    # heading_Array = ['ID', 'Object Type', 'Name', 'Fiscal Year', 'Project', 'Data in Project(GB)', 'Data per File (KB)', 'Fiscal Year Total Data (GB)', 'Running Data Total(GB)']
    # report_Array.append(heading_Array)
    # item_Array = []
    num = 0
    for i in sbItemList:
        # item_Array[:] = []
        report_Array.append([])
        print("Current item object:")
        i.Print()
        print("report_Array new added: {0}".format(report_Array))
        report_Array[num].append(i.ID)
        report_Array[num].append(i.ObjectType)
        report_Array[num].append(i.name)
        report_Array[num].append(i.FY)
        report_Array[num].append(i.project)
        report_Array[num].append(i.DataInProject)
        report_Array[num].append(i.DataPerFile)
        report_Array[num].append(i.totalFYData)
        report_Array[num].append(i.RunningDataTotal)
        print("report_Array all added: {0}".format(report_Array))

        # report_Array.append(item_Array)
        print("report_Array after append: {0}".format(report_Array))
        num += 1
    print('Here\'s the new report_Array: ')
    print(report_Array)
    return(report_Array)


def formatForJson(report_Dict):
    sbItemList = []
    numItems = len(report_Dict["ID"])
    print("numItems")
    print(numItems)
    for i in range(0, numItems):
        x = sbItem()
        x.ID = report_Dict['ID'][i]
        x.ObjectType = report_Dict['Object Type'][i]
        x.name = report_Dict['Name'][i]
        x.FY = report_Dict['Fiscal Year'][i]
        x.project = report_Dict['Project'][i]
        x.DataInProject = report_Dict['Data in Project (GB)'][i]
        x.DataPerFile = report_Dict['Data per File (KB)'][i]
        x.totalFYData = report_Dict['Fiscal Year Total Data (GB)'][i]
        x.RunningDataTotal = report_Dict['Running Data Total (GB)'][i]
        sbItemList.append(x)

    print("sbItemList: ")
    print(sbItemList)
    for i in sbItemList:
        print("i.Print():")
        i.Print()
    # report_Array = format_to_array_of_arrays_For_Json(report_Dict, sbItemList)
    return(sbItemList)
    # return(report_Array)
    
def format_Missing_and_Exceptions(IDlist, URLlist):
    outputList = []
    numItems = len(IDlist)
    for i in range(0, numItems):
        x = problemSBitem()
        x.ID = IDlist[i]
        x.URL = URLlist[i]
        outputList.append(x)
    return(outputList)

def getDate():
    import datetime
    dateinfo = {}
    now = datetime.datetime.now()
    dateinfo['dateTime'] = now
    date = now.strftime("%Y%m%d")
    dateinfo['date'] = date
    return dateinfo

def getCSC(Current_Item):
    NWCSC_FYs = sb.get_child_ids("4f8c64d2e4b0546c0c397b46")
    SWCSC_FYs = sb.get_child_ids("4f8c6580e4b0546c0c397b4e")
    if Current_Item in NWCSC_FYs:
        return("NWCSC")
    elif Current_Item in SWCSC_FYs:
        return("SWCSC")
    else:
        return("Something went wrong: saveJson.getCSC()")


def main():
    PossiblePermissionsIssuesURL = []
    PossiblePermissionsIssuesURL[:] = []
    MissingDataURL= []
    MissingDataURL[:] = []
    if gl.Exceptions != []:
        for i in gl.Exceptions:
            json = sb.get_item(i)
            PossiblePermissionsIssuesURL.append(json['link']['url'])
    if gl.MissingData != []:
        for i in gl.MissingData:
            json = sb.get_item(i)
            MissingDataURL.append(json['link']['url'])

    report_Dict = {'ID': gl.ID, 'Object Type': gl.ObjectType, 'Name': gl.Name,
                    'Fiscal Year': gl.FiscalYear, 'Project': gl.Project,
                    'Data in Project (GB)': gl.DataInProject,
                    'Data per File (KB)': gl.DataPerFile,
                    'Fiscal Year Total Data (GB)': gl.totalFYDataList,
                    'Running Data Total (GB)': gl.RunningDataTotal,
                        }
    print("report_Dict:")  # Quantico
    print(report_Dict)  # Quantico
    print("before report")  # Quantico
    report = formatForJson(report_Dict)
    print(report)  # Quantico

    reportDict = {}
    identity = {}
    identity['name'] = gl.FiscalYear[0]
    identity['ID'] = gl.Current_Item
    identity['CSC'] = getCSC(gl.Current_Item)
    reportDict['identity'] = identity
    reportDict['report'] = report

    reportDict['Date'] = getDate()

    WriteMissing = None
    WriteExceptions = None
    if MissingDataURL != []:
        WriteMissing = True
        report_Missing = format_Missing_and_Exceptions(gl.MissingData, 
                                                       MissingDataURL)
        reportDict['missing'] = report_Missing
    elif MissingDataURL == []:
        WriteMissing = False
        reportDict['missing'] = 'None'
    else:
        print('Something went wrong when transfering report_Missing to reportDict in ExcelPring.py')

    if gl.Exceptions != []:
        WriteExceptions = True
        report_Exceptions = format_Missing_and_Exceptions(gl.Exceptions,
                                                PossiblePermissionsIssuesURL)
        reportDict['exceptions'] = report_Exceptions
    elif gl.Exceptions == []:
        WriteExceptions = False
        reportDict['exceptions'] = 'None'
    else:
        print('Something went wrong when transfering report_Exceptions to reportDict in ExcelPring.py')

    FullReportJson = JsonTransformer()
    FullReportJson = JsonTransformer.transform(FullReportJson, reportDict)
    ID = gl.Current_Item
    import json
    with open('./jsonCache/{0}.json'.format(ID), 'w') as outfile:
        outfile.write(FullReportJson)
    pprint(FullReportJson)  # Quantico

    return

if __name__ == '__main__':
    main()
