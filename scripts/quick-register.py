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
        nextStudentNumber = sys.argv[i]
        # Just use the last 7 characters - in case the ident starts with a nickname
        nextStudentNumber = nextStudentNumber[-7:]
        utilities.logAttendanceForStudent(driver, nextStudentNumber, notes)
