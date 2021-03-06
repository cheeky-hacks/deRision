import os, time
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def initialiseDriver():
    # Python 2 version of selenium seems only to support page load strategy specified via "capabilities"
    capabilities = DesiredCapabilities().CHROME
    capabilities["pageLoadStrategy"] = "eager"
    # Python 3 version of selenium specifies page load strategy via "options"
    options = Options()
    options.page_load_strategy = "eager"
    driverBinaries = os.listdir("driver")
    for binaryFilename in driverBinaries:
        if (binaryFilename[0] != "."): driver = webdriver.Chrome(desired_capabilities=capabilities, options=options, executable_path="driver" + os.sep + binaryFilename)
    driver.get("https://evision.apps.bristol.ac.uk")
    waitUntilWeSeeContent(driver, "Sign in")
    username = os.path.expanduser("~")[-7:]
    insertTextByID(driver,"MUA_CODE.DUMMY.MENSYS",username)
    # Set focus to be password field (so the user can just type it in !)
    clickOnElementByID(driver,"PASSWORD.DUMMY.MENSYS")
    # Wait until the user have entered the password and we are actually logged in before returning
    waitUntilWeSeeLink(driver, "Admissions")
    return driver

def extractNumberFromFilename(filename):
    number = filename
    if "." in number[-5:]: number = number[:number.rindex(".")]
    number = number[-7:]
    return number.strip()

def hideBrowser(driver):
    driver.set_window_position(0, 40000, windowHandle="current")

def clickOnElementByID(driver, id):
    wait = ui.WebDriverWait(driver, 1000)
    element = wait.until(lambda driver: driver.find_elements(by=By.ID, value=id))[0]
    element.click()

def clickLastRadioButton(driver):
    wait = ui.WebDriverWait(driver, 1000)
    radiobuttons = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//input[@type='radio']"))
    radiobuttons[len(radiobuttons)-1].click()

def selectCurrentlyRegisteredEnrolment(driver):
    wait = ui.WebDriverWait(driver, 1000)
    currentEnrolment = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//td[contains(text(), 'REGISTERED')]"))[0]
    radiobutton = currentEnrolment.find_elements(by=By.XPATH, value="../td[1]/div/label/input[@type='radio']")[0]
    radiobutton.click()

def pickFromDropDown(driver, boxNumber, optionNumber):
    wait = ui.WebDriverWait(driver, 1000)
    dropdowns = []
    while len(dropdowns) < boxNumber+1: dropdowns = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//select"))
    dropdown = Select(dropdowns[boxNumber])
    dropdown.select_by_index(optionNumber)

def insertTextByID(driver, id, text):
    wait = ui.WebDriverWait(driver, 1000)
    textfield = wait.until(lambda driver: driver.find_elements(by=By.ID, value=id))[0]
    textfield.send_keys(text)

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
    # Make sure it's a long, long wait
    wait = ui.WebDriverWait(driver, 999999)
    wait.until(lambda driver: driver.find_elements(by=By.PARTIAL_LINK_TEXT, value=text))

def waitUntilWeSeeContent(driver, text):
    while text not in driver.page_source: time.sleep(1)

def clickOnLink(driver, text):
    wait = ui.WebDriverWait(driver, 1000)
    link = wait.until(lambda driver: driver.find_elements(by=By.PARTIAL_LINK_TEXT, value=text))[0]
    link.click()

def clickOnLinkByClass(driver, classname, linkNumber):
    wait = ui.WebDriverWait(driver, 1000)
    links = []
    while len(links) < linkNumber+1:links = wait.until(lambda driver: driver.find_elements(by=By.XPATH, value="//a[@class='" + classname + "']"))
    links[linkNumber].click()

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
    waitUntilWeSeeContent(driver, "Back")
    # If the student has more than one record, we have to do the extra set of selecting one
    if "Select student programme record" in driver.page_source:
        selectCurrentlyRegisteredEnrolment(driver)
        clickOnButton(driver, "Next")
    # Wait for page to settle
    time.sleep(2)
    clickOnButton(driver, "Log attendance")
    # Make sure the page hasn't been changed by checking the names of some of the labels
    checkLabel(driver, 1, "Personal tutor")
    checkLabel(driver, 4, "Attendance date")
    checkLabel(driver, 8, "Attendance time")
    checkLabel(driver, 9, "Advice given")
    # Box number 1 is the name of the personal tutor - should only have one option in the list !
    pickFromDropDown(driver, 1, 1)
    # Box number 4 is the "Advice given" dropdown - set this to option 1: "Academic Support" !
    # pickFromDropDown(driver, 4, 1) # This dropdown was changed to some kind of styled list in a eVision update
    # If you look at the page source, the date text input is 0, but for some reason we have to use 2 !
    if "date" in parameters: insertText(driver, 2, parameters["date"])
    # If you look at the page source, the time text input is 1, but for some reason we have to use 3 !
    if "time" in parameters: insertText(driver, 3, parameters["time"])
    insertNotes(driver, parameters["notes"])
    # Only uncomment this when we happy that the script is robust and we don't want to include a pause-before-commit
    # clickOnButton(driver, "Confirm")
    waitUntilWeSeeContent(driver, "Personal Tutoring: Tutee details")
