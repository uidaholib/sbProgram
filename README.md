# sbMACRO

### sbMACRO CLI
This is a program meant to work with the SciencBase.gov REST API to do things like count data, search, etc. The current iteration of the program can search ScienceBase and print results to the console, as well as parse through entire fiscal years in the Northwest and Southwest Climate Science Center directories on ScienceBase.gov, count the data in each item, project, and fiscal year. It then prints out a report to the console and gives the user the option to create an Excel spreadsheet with the data from the report.

Eventually, the program will be able to parse and count data in specific item IDs/URLs, and project IDs/URLs, as well as batch upload and download items, edit items, and more.

Entire commit history and contributor history can be found here: https://github.com/uidaholib/sbProgram

### sbMACRO [Under Construction]

This is a program and web app meant to work with the SciencBase.gov REST API to do things like count data, search, etc. The current iteration of the project can search ScienceBase and print results to the console, as well as parse through entire fiscal years in the Northwest and Southwest Climate Science Center directories on ScienceBase.gov, count the data in each item, project, and fiscal year.

Currently, the GUI and user interface is being constructed to allow the user to choose more than just a fiscal year to be parsed and to display the results. GUI has much work yet to do to be production-ready, however, the script to create the data works well and currently prints the findings to the command line console.

Entire commit history and contributor history can be found here: https://github.com/uidaholib/sbProgram

## Getting Started

Make sure you have python installed and that you know how to install python libraries.

### Prerequisites

Python 3.6 is required to run this program.

Libraries you need to install to run sbMACRO CLI:
* openpyxl==2.4.8
* pandas==0.20.3
* pysb==1.5.2
* requests==2.18.4

Libraries you need to install to run sbMACRO Web App:
* certifi==2017.7.27.1
* chardet==3.0.4
* click==6.7
* et-xmlfile==1.0.1
* Flask==0.12.2
* idna==2.5
* itsdangerous==0.24
* jdcal==1.3
* Jinja2==2.9.6
* jsonpickle==0.9.5
* MarkupSafe==1.0
* mpmath==1.0.0
* numpy==1.13.1
* openpyxl==2.4.8
* pandas==0.20.3
* pysb==1.5.2
* python-dateutil==2.6.1
* pytz==2017.2
* requests==2.18.3
* scipy==0.19.1
* six==1.10.0
* sympy==1.1.1
* urllib3==1.22
* Werkzeug==0.12.2
* XlsxWriter==0.9.9

The easiest way to make sure you have all dependencies/prerequisites is to download the "requirements.txt" file and run
```
pip install -r requirements.txt
```
in the TrialWebApp directory.

Alternatively, to install each library manually, simply type
```
pip install <library name>
```

Some necessary libraries come pre-installed on python and have not been included in the prerequisites list above. They can be found in the "requirements.txt" file.

NOTE: pysb may need to be installed manually. To install pysb manually, follow instructions here: https://my.usgs.gov/bitbucket/projects/SBE/repos/pysb/browse

### Installing
Simply install all libraries and python 3 before running the program in your favorite command line/terminal program.

Creating a virtual environment is highly recommended so you do not affect your global version of python by installing all of these libraries. Information on virtualenv can be found here: https://virtualenv.pypa.io/en/stable/ . It is easy and highly recommended.

## Deployment
### sbMACRO CLI:
The simplest way to deploy the program is to clone this repository to your local machine, open your favorite command line/terminal program, cd into the directory into which you cloned the repository,and install the prerequisites/dependencies as shown above. 

Once you have the program installed (and your virtual environment is activated if applicable), run start.py
```
python start.py
```

The program should be up and running!

### sbMACRO Web App

The simplest way to deploy the program is to clone the *TrialWebApp* directory to your local machine, open your favorite command line/terminal program, cd into the directory into which you cloned TrialWebApp,and install the prerequisites/dependencies as shown above. 

Once you have the program installed (and your virtual environment is activated if applicable), run app2Dict.py
```
python app2Dict.py
```

The program should be up and running!

Go to your favorite browser and type in
```
http://localhost:5000/
```

You can now interact with the sbMACRO Web Application

## Built With
ScienceBase API,
Python,
Flask

## Contributing
Taylor Rogers


## Authors

* **Taylor Rogers** - *Initial work* - [Capt.Rogers](https://gitlab.com/Capt.Rogers) and [trogers1](https://github.com/trogers1)



## License
                sbMACRO CLI PUBLIC LICENSE
                 Version 2, December 2004

Copyright (C) 2017 Taylor Rogers <taylorrogers@outlook.com>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           sbMACRO CLI PUBLIC LICENSE PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. Freedom is a beautiful thing. Use and modification of this program is permitted, but copyright holder takes no responsibility for said use or modification.


## Acknowledgments

* Thanks to everyone who helped me learn so much by working on this program, including the countless people on the internet willing to answer the questions of a stranger
* Thanks to Jeremy Kenyon for supporting this project professionally and fiscally
* Thanks to the USGS ScienceBase team who made such a wonderful API.
