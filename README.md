# sbMACRO

This is a program and web app meant to work with the ScienceBase.gov REST API to generate reports useful for USGS CASC Data Managers. The program can count data on [Science Base](https://www.sciencebase.gov/catalog/), determine DMP status, present Data Steward-PI history, and more. The current iteration of the project can parse through entire fiscal years or selected projects from any Climate Adaptation Science Center directories on ScienceBase.gov, and generate a report based on the selection provided. Data from Science Base is combined with data found in the combined Data Manager Google Sheets spreadsheet.


Entire commit history and contributor history can be found here: https://github.com/uidaholib/sbProgram

## Getting Started

### Prerequisites

[Python 3.6](https://www.python.org/downloads/) is required to run this program. The program is currently best used on a recent version of Google Chrome.

Libraries you need to install to run sbMACRO Web App are listed in sbMACROv2.0/requirements.txt. The recommended way to make sure you have all dependencies/prerequisites is to download the `requirements.txt` file and run
`python -m pip install -r requirements.txt` in the sbMACROv2.0 directory.

Alternatively, to install each library manually, simply type `python -m pip install <library_name>` without the brackets.

Some necessary libraries come pre-installed with python and may not have been included in the prerequisites list above. They can be found in the `requirements.txt` file. 

NOTE: sciencebasepy may need to be installed manually. To install sciencebasepy manually, follow instructions here: https://github.com/usgs/sciencebasepy.

If the Google Sheets API python module doesn't install, try: `python -m pip install --upgrade google-api-python-client`

The project is also mid-development, so if you have trouble, or `requirements.txt` is not up to date, create an issue on our GitHub page or [contact us](mailto:ad.sbmacro@gmail.com).

### Installing

Simply install all libraries and python 3 before running the program in your favorite command line/terminal program.

Creating a virtual environment is highly recommended so you do not affect your global version of python by installing all of these libraries. Information on virtualenv can be found here: https://virtualenv.pypa.io/en/stable/ . It is easy and highly recommended.

## Deployment

The simplest way to deploy the program is to clone the *sbMACROv2.0* directory to your local machine, open your favorite command line/terminal program, cd into the directory into which you cloned *sbMACROv2.0*,and install the prerequisites/dependencies as shown above. 

Once you have the program installed (and your virtual environment is activated if applicable), run sbmacro.py

```
python sbmacro.py
```

The program should be up and running!

Go to your favorite browser (while in development, sbMACRO works best on Google Chrome) and type in

```
http://localhost:5000/
```

You can then interact with the sbMACRO Web Application.

## Built With

ScienceBase API,
Python,
Flask,
Javascript

## Contributing

[Taylor Rogers](https://github.com/trogers1)

[Sandeep Ravindrababu](https://github.com/sgravi1992)

[Joel Oduro-Afriyie](https://github.com/KobyO)

## Authors

* **Taylor Rogers** - *Initial work* - [Capt.Rogers](https://gitlab.com/Capt.Rogers) as well as [trogers1](https://github.com/trogers1)
* **Sandeep Ravindrababu** - *Contributor* - [sgravi1992](https://github.com/sgravi1992)
* **Joel Oduro-Afriyie** - *Contributor* - [KobyO](https://github.com/KobyO)

## License
The MIT License

Copyright (c) 2017-2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Acknowledgments

* Thanks to everyone who helped me learn so much by working on this program, including the countless people on the internet willing to answer the questions of a stranger
* Thanks to Jeremy Kenyon, the University of Idaho, and the USGS Climate Adaptation Science Center program for supporting this project professionally and fiscally
* Thanks to the USGS ScienceBase team who made such a wonderful API.
