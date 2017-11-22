import ifpmodule
import re

def main():
    print("Starting point collection process.")
    driver = ifpmodule.setup()
    pointCrawl(driver)
    ifpmodule.shutdown(driver)

def pointCrawl(driver):
    namesFilename = 'allNames.txt'
    pointsFilename = 'allPoints.txt'
    batchSaveSize = 10
    currentBatchSize = 0
    totalSaved = 0

    allNames = ifpmodule.loadNamesFromFile(namesFilename)
    allPoints = loadPointsFromFile(pointsFilename)
    pointNames = set(allPoints.keys())
    namesNeedingPoints = getNamesWithoutPointsFromAllNamesAndPointNames(allNames, pointNames)
    print("There are {0} names found without points.".format(len(namesNeedingPoints)))
    pointsToSave = dict()
    for name in namesNeedingPoints:
        print("Retrieving points for " + name)
        points = ifpmodule.getRankForPlayer(driver, name)
        if points != None:
            pointsToSave[name] = points;
            currentBatchSize = currentBatchSize + 1
            if (currentBatchSize >= batchSaveSize):
                ifpmodule.appendPointsToFile(pointsToSave, pointsFilename)
                totalSaved += len(pointsToSave)
                pointsToSave.clear()
                currentBatchSize = 0
                print("Saved batch of {0} point totals, {1} total this session.").format(
                    batchSaveSize, totalSaved
                )

def loadPointsFromFile(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        print("Couldn't open file, continuing with blank dictionary.")
        return dict()

    allPoints = dict()
    nextPointStr = f.readline().decode('utf8').rstrip()
    while nextPointStr != "":
        (name, points) = deserializePoints(nextPointStr)
        allPoints[name] = points
        nextPointStr = f.readline().decode('utf8').rstrip()
    f.close()
    return allPoints

def getNamesWithoutPointsFromAllNamesAndPointNames(allNames, namesWithPoints):
    return allNames - namesWithPoints

def deserializePoints(pointStr):
    nameAndPoints = pointStr.split("$$$$") # Separates the two halves of the string
    name = nameAndPoints[0]
    points = nameAndPoints[1].split(',')
    pointTuple = (int(points[0]), int(points[1]), int(points[2]), int(points[3]))
    return (name, pointTuple)

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

def createPointStringFromNameAndPoints(name, pointTuple):
    str = "{0}$$$${1},{2},{3},{4}".format(
        name,
        pointTuple[0],
        pointTuple[1],
        pointTuple[2],
        pointTuple[3]
    )
    return str

def savePointsToNewFile(pointDict, filename):
    f = open(filename, 'w+')
    for name in list(pointDict.keys()):
        try:
            points = pointDict[name];
            writeStr = createPointStringFromNameAndPoints(name, points) + "\n"
            writeStr = writeStr.encode('utf8')
            f.write(writeStr)
        except:
            print("error writing points string : " + name)
    f.close()

def appendPointsToFile(pointDict, filename):
    f = open(filename, 'a+')
    for name in list(pointDict.keys()):
        try:
            points = pointDict[name];
            writeStr = createPointStringFromNameAndPoints(name, points) + "\n"
            writeStr = writeStr.encode('utf8')
            f.write(writeStr)
        except:
            print("error writing points string : " + name)
    f.close()

if __name__ == '__main__':
    main()
