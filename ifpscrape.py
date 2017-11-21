from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def main():
    filename = "./allNames.txt";

    loadNamesFromFile(filename)

    driver = setup()

    allNames = nameCrawl(driver)

    printAllNames(allNames)

    saveNamesToFile(filename, allNames)

    #print("Now getting rankings...")
    #for name in allNames:
#        print("Rank for " + name)
#        rData = getRankForPlayer(driver, name)
#        print(rData)

    shutdown(driver)

def shutdown(driver):
    driver.close()

def loadNamesFromFile(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        print("Couldn't open file, continuing with blank list.")
        return set()

    allNames = set()
    nextName = f.readline()
    while nextName != "":
        allNames.add(nextName)
        nextName = f.readline().decode('utf8')
    f.close()
    print("Retrieved " + `len(allNames)` + " from file " + filename)
    return allNames

def saveNamesToFile(filename, names):
    f = open(filename, 'w')
    for name in names:
        try:
            writeName = name + '\n'
            writeName = writeName.encode('utf8')
            f.write(writeName)
        except:
            print("error writing name : " + name)
    f.close()
    print("Wrote " + `len(names)` + " names to the file " + filename)

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

def nameCrawl(driver, prefix = ""):
    allNames = set()
    allChars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for char in allChars:
        searchStr = prefix + char
        loadNamesWithText(driver, searchStr)
        names = getAllVisibleNames(driver)
        print("Got " + `len(names)` + " names for search string " + searchStr)
        allNames.update(names)
        if len(names) >= 48:
            print("Diving deeper, prefix " + searchStr)
            names = nameCrawl(driver, searchStr)
            allNames.update(names)
    return allNames

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
    print("name=" + playerName + " , short name =''" + shorterName + "'")
    elem.send_keys(shorterName)
    time.sleep(5)

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
                print("item text (" + dditem.text + ") did not match player name " + playerName)
                ct = ct + 1
                dditem = driver.find_element_by_id("R_c" + `ct`)
    finally:
        pass

    if foundPlayerRow != None:
        foundPlayerRow.click()
        time.sleep(5)
        elem = driver.find_element_by_id("lblRating")
        rankData = getRankFromText(elem.text)
        print("Data for player " + playerName + ":")
        print(rankData)
        return rankData
    else:
        print("Could not find data for player " + playerName)
        return None

def getRankFromText(ratingString):
    # Format:
    #1447/1673 Singles/Doubles Points
    #2068/2044 Women's Singles/Doubles Points
    openRe = re.compile('(\d+)/(\d+) Singles/Doubles Points')
    womenRe = re.compile('(\d+)/(\d+) Women''s Singles/Doubles Points')

    openSingles = 0
    openDoubles = 0
    womenSingles = 0
    womenDoubles = 0

    openM = openRe.match(ratingString)
    if openM != None:
        openSingles = int(openM.group(1))
        openDoubles = int(openM.group(2))

    womenM = womenRe.match(ratingString)
    if womenM != None:
        womenSingles = int(openM.group(1))
        womenDoubles = int(openM.group(2))

    return (openSingles, openDoubles, womenSingles, womenDoubles)


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
    main()
