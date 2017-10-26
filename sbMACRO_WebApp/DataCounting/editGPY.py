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
    # answer2 = input("> ").lower()
    answer2 = 'clear'
    if 'clear' in answer2 or 'empty' in answer2 or 'y' in answer2:
        gl.ID[:] = []
        gl.ObjectType[:] = []
        gl.Name[:] = []
        gl.FiscalYear[:] = []
        gl.Project[:] = []
        gl.DataInProject[:] = []
        gl.DataPerFile[:] = []
        gl.totalFYData = 0
        runningDataToo()
        print("""
    Memory Cleared.""")
        runningDataToo()
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
    # answer = input("> ").lower()
    answer = 'y'
    if 'y' in answer:
        gl.RunningDataTotal[:] = []
        print("Running Total Data reset.")
        return
    elif 'n' in answer:
        print("Running Total Data kept.")
    else:
        print("I didn't get that. Please ")
