import os
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

def initialiseDriver():
    options = Options()
    options.page_load_strategy = "eager"
    driverBinaries = os.listdir("driver")
    for binaryFilename in driverBinaries:
        if (binaryFilename[0] != "."): driver = webdriver.Chrome(options=options, executable_path="driver" + os.sep + binaryFilename)
    driver.get("https://evision.apps.bristol.ac.uk")

    wait = ui.WebDriverWait(driver, 1000)
    # Additional wait to make sure that we actually get logged in
    wait.until(lambda driver: driver.find_elements(by=By.PARTIAL_LINK_TEXT, value="Admissions"))
    return driver

def extractNumberFromFilename(filename):
    number = filename
    if "." in number[-5:]: number = number[:number.rindex(".")]
    number = number[-7:]
    return number.strip()

def hideBrowser(driver):
    driver.set_window_position(0, 40000, windowHandle="current")

def clickLastRadioButton(driver):
    wait = ui.WebDriverWait(driver, 1000)
    radiobuttons = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//input[@type='radio']"))
    radiobuttons[len(radiobuttons)-1].click()

def pickFromDropDown(driver, boxNumber, optionNumber):
    wait = ui.WebDriverWait(driver, 1000)
    dropdowns = []
    while len(dropdowns) < boxNumber+1: dropdowns = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//select"))
    dropdown = Select(dropdowns[boxNumber])
    dropdown.select_by_index(optionNumber)

def insertText(driver, fieldNumber, text):
    wait = ui.WebDriverWait(driver, 1000)
    textboxes = []
    while len(textboxes) < fieldNumber+1: textboxes = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//input[@type='text']"))
    textbox = textboxes[fieldNumber]
    textbox.clear()
    textbox.send_keys(text)

def insertNotes(driver, text):
    wait = ui.WebDriverWait(driver, 1000)
    textbox = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//textarea"))[0]
    textbox.send_keys(text)

def waitUntilWeSeeLink(driver, text):
    wait = ui.WebDriverWait(driver, 1000)
    wait.until(lambda driver: driver.find_elements(by=By.PARTIAL_LINK_TEXT, value=text))[0]

def clickOnLink(driver, text):
    wait = ui.WebDriverWait(driver, 1000)
    link = wait.until(lambda driver: driver.find_elements(by=By.PARTIAL_LINK_TEXT, value=text))[0]
    link.click()

def clickOnLabel(driver, text):
    wait = ui.WebDriverWait(driver, 1000)
    label = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//label[text()='" + text + "']"))[0]
    label.click()

def clickOnButton(driver, text):
    wait = ui.WebDriverWait(driver, 1000)
    button = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//input[@value='" + text + "']"))[0]
    button.click()

def getUsername(driver, studentID):
    clickOnLink(driver, "Student Data")
    clickOnLink(driver, "Lookup Individual Student")
    insertText(driver, 2, studentID)
    clickOnButton(driver, "Search")
    wait = ui.WebDriverWait(driver, 1000)
    cells = []
    while len(cells) < 3: cells = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="*//tbody[@id='data']//tr//td"))
    email = cells[2]
    return email.text.split("@")[0]

def getStudentNumber(driver, username):
    clickOnLink(driver, "Student Data")
    clickOnLink(driver, "Lookup Individual Student")
    insertText(driver, 3, username)
    clickOnButton(driver, "Search")
    wait = ui.WebDriverWait(driver, 1000)
    number = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="*//tbody[@id='data']//tr//td"))[0]
    return number.text

def checkLabel(driver, labelNumber, expectedValue):
    wait = ui.WebDriverWait(driver, 1000)
    labels = []
    while len(labels) < labelNumber+1: labels = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//label"))
    assert expectedValue in labels[labelNumber].text, "The element with the label " + expectedValue + " wasn't found in the expected place !\nThe page may well have changed !!!"

def logAttendanceForStudent(driver, studentNumber, parameters):
    clickOnLink(driver, "Assessment & Progression")
    clickOnLink(driver, "View a tutee")
    # There are some hidden text fields in the page, so the student number textfield has an index of 2
    insertText(driver, 2, studentNumber)
    clickOnButton(driver, "Search")
    # If the student has more than one record, we have to do the extra set of selecting one
    if "Select student programme record" in driver.page_source:
        clickLastRadioButton(driver)
        clickOnButton(driver, "Next")
    clickOnButton(driver, "Log attendance")
    # Make sure the page hasn't been changed by checking the names of some of the labels
    checkLabel(driver, 1, "Personal tutor")
    checkLabel(driver, 4, "Attendance date")
    checkLabel(driver, 8, "Attendance time")
    checkLabel(driver, 9, "Advice given")
    # Box number 1 is the name of the personal tutor - should only have one option in the list !
    pickFromDropDown(driver, 1, 1)
    # Box number 4 is the "Advice given" dropdown - set this to option 1: "Academic Support" !
    pickFromDropDown(driver, 4, 1)
    # If you look at the page source, the date text input is 0, but for some reason we have to use 2 !
    if "date" in parameters: insertText(driver, 2, parameters["date"])
    # If you look at the page source, the time text input is 1, but for some reason we have to use 3 !
    if "time" in parameters: insertText(driver, 3, parameters["time"])
    insertNotes(driver, parameters["notes"])
    # Only uncomment this when we actually want to log attendance
    # clickOnButton(driver, "Confirm")
    waitUntilWeSeeLink(driver, "Mark Flags")
