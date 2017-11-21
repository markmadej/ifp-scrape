import ifpmodule


def main():
    print("Starting name crawl process.")
    driver = ifpmodule.setup()
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
        newNames = ifpmodule.getAllVisibleNames(driver)
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
            sequence = ifpmodule.getNextDeeperLevelSequence(sequence)
        else:
            sequence = ifpmodule.getNextSameLevelSequence(sequence)
    print("Congratulations!  You've retrieved all {0} names.".format(len(allNames)))

if __name__ == '__main__':
    main()
