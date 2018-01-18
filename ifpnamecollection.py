import ifpmodule


def main():
    print("Starting name crawl process.")
    driver = ifpmodule.setupRemote()
    nameCrawl(driver)
    ifpmodule.shutdown(driver)

def nameCrawl(driver):
    namesFilename = 'allNames.txt'
    sequenceFilename = 'sequence.data'

    allNames = ifpmodule.loadNamesFromFile(namesFilename)
    sequence = ifpmodule.getLastSequenceFromFile(sequenceFilename)
    if (sequence == 'A'):
        # Start fresh because we're at the initial sequence.
        ifpmodule.emptyFile(sequenceFilename)

    while (sequence != None):
        ifpmodule.loadNamesWithText(driver, sequence)
        newNames = getAllVisibleNames(driver)
        goDeeper = (len(newNames) >= 48)
        uniqueNewNames = ifpmodule.getUniqueNewNamesOnlyFromAllNamesAndNewList(allNames, newNames)
        ifpmodule.appendNamesToFile(uniqueNewNames, namesFilename)
        allNames.update(newNames)
        print("Sequence {0} : Saved {1} more names to file, {2} so far.".format(
            sequence,
            len(uniqueNewNames),
            len(allNames)
        ))
        if goDeeper:
            print("Will go deeper, more than 47 entries found.")
        ifpmodule.saveLastSequenceToFile(sequence, sequenceFilename)
        if goDeeper:
            sequence = getNextDeeperLevelSequence(sequence)
        else:
            sequence = getNextSameLevelSequence(sequence)
    print("Congratulations!  You've retrieved all {0} names.".format(len(allNames)))

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
