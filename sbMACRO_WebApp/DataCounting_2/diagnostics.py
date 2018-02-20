from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify
# eyekeeper Quantico this is not finished in any way, shape or form

def diagnostics(projects, projectDictNumber, exceptionItems, exceptionFound, currentProjectJson):
    print("There appear to have been exceptions raised for the following items:")
    print(exceptionItems)
    print('''

    I am done looking through the \''''+str(currentProjectJson['title']) +
          '''' project folder.''')
    projectDictNumber += 1
    whatNext(projects, projectDictNumber, exceptionItems, exceptionFound)
