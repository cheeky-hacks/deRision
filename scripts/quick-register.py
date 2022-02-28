import sys
import utilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if len(sys.argv) < 2: print("Usage: python3 " + sys.argv[0] + " <student number list>")
else:
    notes = input("Please enter some note text for all students: ")
    driver = utilities.initialiseDriver()
    # utilities.hideBrowser(driver)

    for i in range(1,len(sys.argv)):
        # Get the student number from the parameter (which might be a filename)
        nextStudentNumber = extractNumberFromFilename(sys.argv[i])
        utilities.logAttendanceForStudent(driver, nextStudentNumber, notes)
