import sys
import utilities

parameters = {}
students = []
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "-d": parameters["date"] = sys.argv[i+1]
    elif sys.argv[i] == "-t": parameters["time"] = sys.argv[i+1]
    else: students.append(sys.argv[i])
    # Step forward the right number of places
    if sys.argv[i][0] == "-": i+=2
    else: i+=1

if len(students) == 0: print("Usage: python " + sys.argv[0] + " [-d DD/MM/YYYY] [-t HH:MM] <student number>...")
else:
    parameters["notes"] = input("Please enter note text for these students: ")
    driver = utilities.initialiseDriver()
    # utilities.hideBrowser(driver)

    for student in students:
        # Get the student number from the parameter (which might be a filename)
        nextStudentNumber = utilities.extractNumberFromFilename(student)
        print("Registering attendance for " + nextStudentNumber)
        utilities.logAttendanceForStudent(driver, nextStudentNumber, parameters)
