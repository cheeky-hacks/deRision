import sys
import utilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if len(sys.argv) < 2: print("Usage: python3 " + sys.argv[0] + " <username list>")
else:
    notes = input("Please enter some note text for all students: ")
    driver = utilities.initialiseDriver()
    # utilities.hideBrowser(driver)

    for i in range(1,len(sys.argv)):
        nextUsername = sys.argv[i]
        studentNumber = utilities.getStudentNumber(driver, nextUsername)
        utilities.logAttendanceForStudent(driver, studentNumber, notes)
