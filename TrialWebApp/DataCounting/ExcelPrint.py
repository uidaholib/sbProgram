import gl

from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify, send_from_directory, send_file
import os
import pandas
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from pprint import pprint

import requests
import json
import pysb

import io  # For the creation of download file in-memory


sb = pysb.SbSession()

def main():
    #try:
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

    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    if gl.MissingData != []:
        ws_missing = wb.create_sheet("Missing", 1) #Inserts a new sheet, named "Missing" in the second position
        #ws_missing.sheet_properties.tabColor = "1072BA" #Makes the tab for the sheet red so it draws attention.
    if gl.Exceptions != []:
        ws_exceptions = wb.create_sheet("Exceptions", 2) #Inserts a new sheet, named "Exceptions" in the third position
        #ws_exceptions.sheet_properties.tabColor = "1072BA" #Makes the tab for the sheet red so it draws attention.


    report_Dict = {'ID': gl.ID, 'Object Type': gl.ObjectType, 'Name': gl.Name,
                    'Fiscal Year': gl.FiscalYear, 'Project': gl.Project,
                    'Data in Project (GB)': gl.DataInProject,
                    'Data per File (KB)': gl.DataPerFile,
                    'Fiscal Year Total Data (GB)': gl.totalFYData,
                    'Running Data Total (GB)': gl.RunningDataTotal,
                        }
    print(report_Dict)  # Quantico
                        #include these eventually: 'Missing Data?': L7MissingData, 'Exceptions/Permissions Issues': L9Exceptions

                #include these eventually: 'Missing Data?', 'Exceptions/Permissions Issues'
    #if gl.MissingData != []:
    report_Missing = {'Missing Data ID': gl.MissingData,
                            'Missing Data URL': MissingDataURL}

    #if gl.Exceptions != []:
    report_Exceptions = {'Exception/Permission Issue ID': gl.Exceptions,
                               'Exception/Permission Issue URL':
                               PossiblePermissionsIssuesURL} 
                               #include 'Exception ID': L10Exceptions_IDs, later
 #include 'Exception ID' later


    # for r in dataframe_to_rows(dfOrdered, index=False, header=True):
    #     ws.append(r)

    # for cell in ws[1]:
    #     cell.style = 'Pandas'


    reportDict = {}
    reportDict['report'] = report_Dict

    WriteMissing = None
    WriteExceptions = None
    if MissingDataURL != []:
        WriteMissing = True
        reportDict['missing'] = report_Missing
    elif MissingDataURL == []:
        WriteMissing = False
        reportDict['missing'] = 'None'
    else:
        print('Something went wrong when transfering report_Missing to reportDict in ExcelPring.py')
        # for r in dataframe_to_rows(df_missing, index=False, header=True):
        #     ws_missing.append(r)

        # for cell in ws_missing[1]:
        #     cell.style = 'Pandas'

    if gl.Exceptions != []:
        WriteExceptions = True
        reportDict['exceptions'] = report_Exceptions
    elif gl.Exceptions == []:
        WriteExceptions = False
        reportDict['exceptions'] = 'None'
    else:
        print('Something went wrong when transfering report_Exceptions to reportDict in ExcelPring.py')
        # for r in dataframe_to_rows(df_exceptions, index=False, header=True):
        #     ws_exceptions.append(r)

        # for cell in ws_exceptions[1]:
        #     cell.style = 'Pandas'

    #print(df)
    #print('''

#    ---------Let\'s try reordering that...

 #   ''')
    #print(dfOrdered)
    #flash(dfOrdered['ID'])
    #flash(dfOrdered['Object Type'])
    #flash(dfOrdered['Name'])
    #flash(dfOrdered['Fiscal Year'])
    #flash(dfOrdered['Project'])
    #flash(dfOrdered['Data in Project (GB)'])
    #flash(dfOrdered['Data per File (KB)'])
    #flash(dfOrdered['Fiscal Year Total Data (GB)'])
    #flash(dfOrdered['Running Data Total (GB)'])
    #if gl.Exceptions != [] or gl.MissingData != []:
    #    print('''

    #Items missing data:
    #          ''')
    #    print(df_missing)
    #    print('''

    #Exceptions raised:
    #          ''')
    #    print(df_exceptions)
    #print('''
    #Does that look correct?
    #(Y / N)
    #''')
    #correct = input("> ").lower()
    #if 'y' in correct:
    #    ask(wb)
    #elif 'n' in correct:
    #    import editGPY
    #    editGPY.main()
    #    main()
    #ask(wb)
    #download_log(wb, dfOrdered, df_missing, df_exceptions, WriteMissing, WriteExceptions)
    #saveExcel(wb)
    # reportDict = createJson(wb, dfOrdered, df_missing, df_exceptions, WriteMissing, WriteExceptions)
    return(reportDict)

# def createJson(wb, dfOrdered, df_missing, df_exceptions, WriteMissing, WriteExceptions):
#     reportDict = {}
#     #print(dfOrdered)
#     report = dfOrdered.to_json()
#     #pprint(report)
#     reportDict['report'] = report
#     #pprint(reportDict)
#     if WriteMissing:
#         missing = df_missing.to_json()
#         reportDict['missing'] = missing
#     if WriteExceptions:
#         exceptions = df_exceptions.to_json()
#         reportDict['exceptions'] = exceptions
#     return(reportDict)

# def download_log(wb, dfOrdered, df_missing, df_exceptions, WriteMissing, WriteExceptions):
#    output = io.BytesIO()
#    writer = pandas.ExcelWriter(output, engine='xlsxwriter')
#    dfOrdered.to_excel(writer, sheet_name='Report')
#    if WriteMissing:
#         df_missing.to_excel(writer, sheet_name='Missing')
#    if WriteExceptions:
#        df_exceptions.to_excel(writer, sheet_name='Exceptions')
#    writer.save()
#    output.seek(0)
#    excelDownload = output.read()
#    #print(excelDownload)
#    return send_file(excelDownload, mimetype='application/vnd.ms-excel.sheet.binary.macroenabled.12', attachment_filename = 'sbMACRO-output.xlsx',
#                     as_attachment=True)

# def new_download_log(wb, dfOrdered, df_missing, df_exceptions, WriteMissing, WriteExceptions):
#    output = io.BytesIO()
#    writer = pandas.ExcelWriter(output, engine='xlsxwriter')
#    dfOrdered.to_excel(writer, sheet_name='Report')
#    if WriteMissing:
#         df_missing.to_excel(writer, sheet_name='Missing')
#    if WriteExceptions:
#        df_exceptions.to_excel(writer, sheet_name='Exceptions')
#    writer.save()
#    output.seek(0)
#    excelDownload = output.read()
#    return send_file(excelDownload, mimetype='application/vnd.ms-excel.sheet.binary.macroenabled.12', attachment_filename = 'sbMACRO-output.xlsx',
#                     as_attachment=True)

# def ask(wb):
#     print ('''

#     Would you like to save this?
#     (Y / N)''')
#     answer = input('> ').lower()
#     if 'y' in answer:
#         print('''
#     Where would you like to save the file? Copy and paste a file path or '''+
#     '''type "Desktop" to save it to the desktop (If you run Linux, you must'''+
#     ''' paste a path).''')
#         answer2 = input("> ").lower()
#         if 'desk' in answer2:
#             filePath = os.path.expanduser("~/Desktop/")
#             saveExcel(wb, filePath)
#         elif '/' in answer2 or '\\' in answer2:
#             filePath = answer2
#             saveExcel(wb, filePath)
#         else:
#             print('''
#     That didn't appear to be a path. Please try again.''')
#             ask(wb)

#     elif 'n' in answer:
#         print('''
#         Ok, we won't save it.''')
#         return
# #    except (ValueError, Exception) as e:
# #        print('''
# #    ----------------------------WARNING: Something went wrong in the function "main" in ExcelPrint.py.''')
# #        exit()

# def saveExcel(wb):
#     filepath = "C:/Users/Taylor/Documents/!USGS/Python/sbProgramGitRepo/TrialWebApp/static/"   # Quantico, eyekeeper, must change this in final hosted version.
#     name = 'sbMACRO-output.xlsx'
#     wb.save(filepath+name)
#     print("file saved")
#     return send_from_directory(filepath, name, mimetype='application/vnd.ms-excel.sheet.binary.macroenabled.12', as_attachment=True)

# def saveExcel_old(wb, filePath):
#     ChosenFiscalYear = gl.FiscalYear[-1]  # Most recent Fiscal Year.
#     print('''
#     Would you like to name it something other than "'''+str(ChosenFiscalYear)+
#     ''' Data Metrics.xlsx"?
#     Beware: chosing the same name as an existing file overwrites that file '''+
#     '''without warning.''')
#     answer = input('> ').lower()
#     if 'y' in answer or 'other' in answer:
#         print('''
#     What name would you like to give the Excel file?''')
#         name = input('> ')
#         wb.save(str(filePath)+str(name)+".xlsx")
#         print('''
#     Workbook saved as "'''+str(name)+'''.xlsx" in \''''+str(filePath)+'''\'.''')
#         return
#     elif 'n' in answer or 'keep' in answer:
#         wb.save(str(filePath)+str(ChosenFiscalYear)+" Data Metrics.xlsx")
#         print('''
#     Workbook saved as "'''+str(ChosenFiscalYear)+''' Data Metrics.xlsx" in \''''+str(filePath)+'''\'.''')
#         return
#     else:
#         print('''
#     I'm sorry, I didn't get that. Please type 'y', 'other', 'n', or 'keep'
#     ''')
#         saveExcel(wb, filePath)
