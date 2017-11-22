import ifpmodule

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

if __name__ == '__main__':
    main()
