# deRision

This project aims to provide a number of python scripts to automate common eVision activities.  
These are implemented as a set of browser macros that automate navigation through the pages of the eVision site.

## Installation
Download a copy of the scripts by either cloning this repository or by
[downloading a zip file of it](https://github.com/cheeky-hacks/deRision/archive/refs/heads/main.zip).

In order to use these scripts, you will need to install a
[browser driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
that matches your platform and browser.  
Once downloaded and unzipped, place the driver in the `driver` folder of this project.

You will also need to install the Python bindings for the browser driver. This can be down with:
```
pip install selenium
```

## Running the "Quick Register" script
To run the "Quick Register" personal tutorial attendance script, `cd` into the project root folder and run:
```
python scripts/quick-register.py 1911111 1922222 1933333
```
Where the numbers at the end are student numbers of the students you wish to log attendance for.  
You will then be prompted to enter some note text which will be added to all students attendance records.
Following this, a new browser window will open and you will be asked to sign in to eVision.  
Once you have signed in, the script will take over and automate the tasks involved in logging attendance.

By default, the script will use the current date and time for the logged personal tutorial.  
If you are registering attendance some time after the tutorial meeting, it is possible to specify time and/or date with:
```
python scripts/quick-register.py -t 11:30 -d 22/02/2022 1911111 1922222 1933333
```
