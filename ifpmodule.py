from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import sys

def shutdown(driver):
    driver.close()

def saveLastSequenceToFile(sequence, filename):
    try:
        f = open(filename, 'w+')
        f.write(sequence.encode('utf-8'))
    except IOError:
        print("ERROR - Could not save sequence to file!  Last was " + sequence)

def getLastSequenceFromFile(filename):
    try:
        f = open(filename, 'r')
        sequence = f.readline().decode('utf8').rstrip()
        return sequence
    except IOError:
        print("Could not retrieve sequence from file, starting with 'A'.")
        return 'A'

def loadNamesFromFile(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        print("Couldn't open file, continuing with blank list.")
        return set()

    allNames = set()
    nextName = f.readline().decode('utf-8').rstrip()
    while nextName != "":
        allNames.add(nextName)
        nextName = f.readline().decode('utf-8').rstrip()
    f.close()
    return allNames

def saveNamesToNewFile(names, filename):
    f = open(filename, 'w+')
    for name in names:
        try:
            writeName = name + '\n'
            writeName = writeName.encode('utf-8')
            f.write(writeName)
        except:
            print("error writing name : " + name)
    f.close()

def emptyFile(filename):
    f = open(filename, 'w+')
    f.close()

def appendNamesToFile(names, filename):
    f = open(filename, 'a+')
    for name in names:
        try:
            writeName = name + '\n'
            writeName = writeName.encode('utf-8')
            f.write(writeName)
        except:
            print("error writing name : " + name)
    f.close()

def getCorrectDriver():
    if len(sys.argv) < 2:
        print "You need to specify the type of Selenium run you want with a -docker or -local flag."
        sys.exit(1)
    if (sys.argv[1] == '-docker'):
        driver = setupRemote()
        return driver
    if (sys.argv[1] == '-local'):
        driver = setup()
        return driver
    print "Bad Selenium flag.  Use -docker or -local flag."
    sys.exit(1)

def setup():
    print("Entering setup.")
    driver = webdriver.Firefox()
    driver.get("http://ifp.everguide.com/commander/tour/public/PlayerProfile.aspx")
    print("Loaded driver, loaded main page.")
    return driver

def setupRemote():
    try:
        driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX,
                              command_executor='http://127.0.0.1:4444/wd/hub')
        driver.get("http://ifp.everguide.com/commander/tour/public/PlayerProfile.aspx")
        print "Got remote driver : " + str(driver)
        return driver
    except Exception as err:
        print "Couldn't connect remote : " + str(err)
        sys.exit(1)

def getUniqueNewNamesOnlyFromAllNamesAndNewList(allNames, newList):
    return newList - allNames


def loadNamesWithText(driver, searchStr):
    elem = driver.find_element_by_name("R_Input")
    elem.clear()
    elem.send_keys(searchStr)

    # Either wait 1 second, or until you see the Loading div.
    # If it's there, wait until it's gone (or 10 seconds).
    try:
        WebDriverWait(driver, .8).until(
            EC.visibility_of_element_located((By.ID, 'R_LoadingDiv'))
        )
    except:
        # This is fine :dog with burning house:
        # Seriously though it might just have gone by really fast, ignore this.
        pass

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'R_LoadingDiv'))
    )

if __name__ == '__main__':
    print("This class should not be run directly.  Please look at the README.")
