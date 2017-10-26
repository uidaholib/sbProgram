# from https://stackoverflow.com/questions/34072525/getting-information-from-html-form-with-checkboxes-with-python-flask

from flask import Flask, render_template, request, redirect

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'


CASES = ['test1', 'test2', 'test3', 'test4']

@app.route("/")
def template_test():
    return(render_template('template.html', title="Home"))

@app.route("/TestCases")
def TestCases():
    return(render_template('ex1template.html', cases=CASES, title="Test Cases"))

@app.route("/info", methods=['POST'])
def getinfo():
    if request.method == 'POST':
        test = request.form.getlist('checks')
        print(test)
        return(redirect('/'))
    else:
        return(redirect('/'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
