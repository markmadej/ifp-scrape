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
    foundPlayerRow = None
    try :
        dditem = driver.find_element_by_id("R_c" + `ct`)

        while dditem :
            if dditem.text == playerName:
                foundPlayerRow = dditem
                break
            else:
                ct = ct + 1
                dditem = driver.find_element_by_id("R_c" + `ct`)
    finally:
        pass

    if foundPlayerRow != None:
        foundPlayerRow.click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'lblRating'))
        )
        elem = driver.find_element_by_id("lblRating")
        rankData = getRankFromText(elem.text)
        return rankData
    else:
        print("Could not find data for player " + playerName)
        return None

def getRankFromText(ratingString):
    # Format:
    #1447/1673 Singles/Doubles Points
    #2068/2044 Women's Singles/Doubles Points
    # from the "lblRating" field in HTML
    openTuple = getOpenPointsFromString(ratingString)
    womenTuple = getWomensPointsFromString(ratingString)
    return (openTuple[0], openTuple[1], womenTuple[0], womenTuple[1])

def getOpenPointsFromString(ratingString):
    return getPointsFromStringWithRegex(
        '(\d+)/(\d+) Singles/Doubles Points', ratingString
        )

def getWomensPointsFromString(ratingString):
    # This should match without the leading .*\D but in my experience that is
    # not happening and Python regexes need to match the whole string, or at least
    # the match needs to start with the first character.  Shrug.
    return getPointsFromStringWithRegex(
        '.*\D(\d+)/(\d+) Women\'s Singles/Doubles Points', ratingString
        )

def getPointsFromStringWithRegex(regex, ratingString):
    singles = 0
    doubles = 0
    regexp = re.compile(regex)
    match = regexp.match(ratingString)
    if match != None:
        singles = int(match.group(1))
        doubles = int(match.group(2))

    return (singles, doubles)

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
    
def createPointStringFromNameAndPoints(name, pointTuple):
    str = "{0}$$$${1},{2},{3},{4}".format(
        name,
        pointTuple[0],
        pointTuple[1],
        pointTuple[2],
        pointTuple[3]
    )
    return str

if __name__ == '__main__':
    print("This class should not be run directly.  Please look at the README.")
