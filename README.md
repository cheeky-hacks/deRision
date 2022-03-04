# deRision

This project aims to provide a number of python scripts to automate common eVision activities.
These are implemented as a set of browser macros that automate navigation through the pages of the eVision site.

## Installation
Download a copy of the scripts by either cloning this repository or by
[downloading a zip file of it](https://github.com/cheeky-hacks/deRision/edit/main/README.md)
In order to use these scripts, you will need to install a
[browser driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
that matches your platform and browser. Once downloaded and unzipped, place the driver in the `driver` folder of this project.

You will also need to install the Python bindings for the browser driver. This can be down with:
```
pip install selenium
```
Note that you might need to use `pip3` if you also have python2 installed

## Running the scripts
To run the scripts `cd` into the project folder and run:
```
python scripts/quick-register.py
```
