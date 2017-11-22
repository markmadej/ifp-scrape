from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def shutdown(driver):
    driver.close()

def saveLastSequenceToFile(sequence, filename):
    try:
        f = open(filename, 'w+')
        f.write(sequence.encode('utf8'))
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
    nextName = f.readline().decode('utf8').rstrip()
    while nextName != "":
        allNames.add(nextName)
        nextName = f.readline().decode('utf8').rstrip()
    f.close()
    return allNames

def saveNamesToNewFile(names, filename):
    f = open(filename, 'w+')
    for name in names:
        try:
            writeName = name + '\n'
            writeName = writeName.encode('utf8')
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
            writeName = writeName.encode('utf8')
            f.write(writeName)
        except:
            print("error writing name : " + name)
    f.close()

def setup():
    print("Entering setup.")
    driver = webdriver.Firefox()
    driver.get("http://ifp.everguide.com/commander/tour/public/PlayerProfile.aspx")
    print("Loaded driver, loaded main page.")
    return driver

def getUniqueNewNamesOnlyFromAllNamesAndNewList(allNames, newList):
    return newList - allNames


def loadNamesWithText(driver, searchStr):
    elem = driver.find_element_by_name("R_Input")
    elem.clear()
    elem.send_keys(searchStr)
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'R_LoadingDiv'))
    )

if __name__ == '__main__':
    print("This class should not be run directly.  Please look at the README.")
