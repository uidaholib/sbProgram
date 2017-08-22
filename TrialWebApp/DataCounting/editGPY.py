import gl
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify
import requests
import json
import pysb
import sys

from pprint import pprint

sb = pysb.SbSession()

def main():  # eyekeeper Quantico, this is called in ExcelPrint.py should figure out how to edit data or erase it.
    pass

def clearMemory():
    print("""
    Would you like to clear the memory of all of the data parsed so far"""+
    """, or keep all data to be placed into a single Excel spreadsheet """+
    """later?""")
    answer2 = input("> ").lower()
    if 'clear' in answer2 or 'empty' in answer2 or 'y' in answer2:
        g.ID[:] = []
        g.ObjectType[:] = []
        g.Name[:] = []
        g.FiscalYear[:] = []
        g.Project[:] = []
        g.DataInProject[:] = []
        g.DataPerFile[:] = []
        g.totalFYData = 0
        runningDataToo()
        print("""
    Memory Cleared.""")
        return
    elif 'keep' in answer2 or 'save' in answer2 or 'n' in answer2:
        print('''
    Ok. Memory contents kept.''')
        return
    else:
        clearMemory()

def runningDataToo():
    print('''
    Would you also like to reset the Running Total Data?
    (Y / N)
    ''')
    answer = input("> ").lower()
    if 'y' in answer:
        g.RunningDataTotal[:] = []
        print("Running Total Data reset.")
    elif 'n' in answer:
        print("Running Total Data kept.")
    else:
        print("I didn't get that. Please ")
