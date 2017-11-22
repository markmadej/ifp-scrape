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

def saveLastPointSequenceToFile(filename):
    saveLastSequenceToFile(filename)

def getLastPointSequenceFromFile(filename):
    # Same as the original, just returning None instead of 'A' if the file is empty.
    lastSeq = getLastSequenceFromFile(filename)
    if lastSeq == 'A':
        return None
    else:
        return lastSeq

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

def printAllNames(names):
    print("Found a total of " + `len(names)` + " names :")
    for name in sorted(names):
        print("- " + name)

def setup():
    print("Entering setup.")
    driver = webdriver.Firefox()
    driver.get("http://ifp.everguide.com/commander/tour/public/PlayerProfile.aspx")
    print("Loaded driver, loaded main page.")
    return driver

def getUniqueNewNamesOnlyFromAllNamesAndNewList(allNames, newList):
    return newList - allNames

def getNextSameLevelSequence(sequence):
    if sequence is None:
        return 'A'
    if sequence == 'Z':
        return None

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    lastSequenceChar = sequence[-1]
    if lastSequenceChar == 'Z':
        # Drop back one level
        sequence = sequence[0:-1]
        # Calling getNextSameLevelSequence again will recursively
        # remove multiple Zs from the end if needed
        return getNextSameLevelSequence(sequence)
    else:
        idx = alphabet.find(lastSequenceChar)
        return sequence[0:-1] + alphabet[idx+1]

def getNextDeeperLevelSequence(sequence):
    return sequence + 'A'

def loadNamesWithText(driver, searchStr):
    elem = driver.find_element_by_name("R_Input")
    elem.clear()
    elem.send_keys(searchStr)
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, 'R_LoadingDiv'))
    )

def getRankForPlayer(driver, playerName):
    elem = driver.find_element_by_name("R_Input")
    elem.clear()

    # First chop off the trailing (state) from the end - doesnt work with IFP interface
    parenLoc = playerName.find('(')
    shorterName = playerName[0:parenLoc-1]
    elem.send_keys(shorterName)
    time.sleep(3)

    # Dropdown should be populated.  Find the right item and click on it
    ct = 0

    try :
        foundPlayerRow = None
        dditem = driver.find_element_by_id("R_c" + `ct`)

        while dditem :
            if dditem.text == playerName:
                foundPlayerRow = dditem
                break
            else:
                ct = ct + 1
                dditem = driver.find_element_by_id("R_c" + `ct`)

        if foundPlayerRow != None:
            foundPlayerRow.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'lblRating'))
            )
            elem = driver.find_element_by_id("lblRating")
            rankData = getRankFromText(elem.text)
            return rankData

    except:
        print("Could not retrieve data for player " + playerName)
        return None

def getAllVisibleNames(driver):
    names = set()
    ct = 0
    try :
        dditem = driver.find_element_by_id("R_c" + `ct`)

        while dditem :
            names.add(dditem.text)
            ct = ct + 1
            dditem = driver.find_element_by_id("R_c" + `ct`)
        return names
    finally:
        return names

if __name__ == '__main__':
    print("This class should not be run directly.  Please look at the README.")
