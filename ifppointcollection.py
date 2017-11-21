import ifpmodule

def main():
    print("Starting point collection process.")
    driver = ifpmodule.setup()
    pointCrawl(driver)
    ifpmodule.shutdown(driver)

def pointCrawl(driver):
    # For each name in the list
        # Check to see if we already have points for that name
        # If not, get points and save to file
        # Save last name processed to file
    namesFilename = 'allNames.txt'
    pointsFilename = 'allPoints.txt'
    sequenceFilename = 'pointsequence.data'

    allNames = ifpmodule.loadNamesFromFile(namesFilename)
    sequence = ifpmodule.getLastPointSequenceFromFile(sequenceFilename)

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


if __name__ == '__main__':
    main()
