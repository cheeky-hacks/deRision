import sys
import utilities

if len(sys.argv) != 2: print("Usage: python " + sys.argv[0] + " <username>")
else:
    driver = utilities.initialiseDriver()
    utilities.clickOnLink(driver, "Student Data")
    utilities.clickOnLink(driver, "Lookup Individual Student")
    utilities.insertText(driver, 3, sys.argv[1])
    utilities.clickOnButton(driver, "Search")
    utilities.clickOnLinkByClass(driver, "evislink", 0)
