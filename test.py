import unittest
import ifpmodule
import os

class TestIfpModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.remove('/tmp/testfile1.txt')
            os.remove('/tmp/testfile2.txt')
            os.remove('/tmp/testsequence.txt')
            os.remove('/tmp/testempty.txt')
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove('/tmp/testfile1.txt')
            os.remove('/tmp/testfile2.txt')
            os.remove('/tmp/testsequence.txt')
            os.remove('/tmp/testempty.txt')
        except:
            pass

    def test_upper(self):
        pointStrings = [
            "2325/1714 Singles/Doubles Points<br>EXPERT"
            , "1447/1824 Singles/Doubles Points<br>2116/2060 Women's Singles/Doubles Points<br>EXPERT"
            , "601/601 Singles/Doubles Points<br>BEGINNER"
            , "1472/1925 Singles/Doubles Points<br>5588/7149 Women's Singles/Doubles Points<br>MASTER"
            ]
        resultTuples = [
            (2325, 1714, 0, 0),
            (1447, 1824, 2116, 2060),
            (601, 601, 0, 0),
            (1472, 1925, 5588, 7149)
        ]
        for i in range(0, len(pointStrings)):
            self.assertEqual(ifpmodule.getRankFromText(pointStrings[i]), resultTuples[i])

    # The intention with the next crawl character is that we should be able to save
    # our last completed character, and the crawl can continue seamlessly from there on
    # restart.  If we have a consistent algorithm to determine the next character we can
    # make that happen.
    def test_next_crawl_sequence_same_level(self):
        currentSequence = [
            "A",
            "ABC",
            "MARKMADEJ",
            "CZ",
            "AZZ",
            "Z"
        ]
        nextCrawlSequence = [
            "B",
            "ABD",
            "MARKMADEK",
            "D",
            "B",
            None
        ]
        for i in range(0, len(currentSequence)):
            self.assertEqual(ifpmodule.getNextSameLevelSequence(
                currentSequence[i]), nextCrawlSequence[i])

    def test_next_crawl_sequence_deeper_level(self):
        currentSequence = [
            "A",
            "ABC",
            "MARKMADEJ",
            "CZ",
            "Z"
        ]
        nextCrawlSequence = [
            "AA",
            "ABCA",
            "MARKMADEJA",
            "CZA",
            "ZA",
            None
        ]
        for i in range(0, len(currentSequence)):
            self.assertEqual(ifpmodule.getNextDeeperLevelSequence(
                currentSequence[i]), nextCrawlSequence[i])

    def test_files_write_and_read_same_data(self):
        originalNames = {
            "MARK MADEJ (CO)",
            "TONY SPREDEMAN (FL)",
            "HANNAH DEE SMITH (MS)",
            "MARKUS HAYMAN (MS)"
        }
        filename = '/tmp/testfile1.txt'
        ifpmodule.saveNamesToNewFile(originalNames, filename)
        loadedNames = ifpmodule.loadNamesFromFile(filename)
        self.assertEqual(originalNames, loadedNames)

    def test_append_file(self):
        originalNames1 = {
            "MARK MADEJ (CO)",
            "BETH MADEJ (CO)"
        }
        originalNames2 = {
            "HANNAH DEE SMITH (MS)",
            "MARKUS HAYMAN (MS)"
        }
        filename = '/tmp/testfile2.txt'

        ifpmodule.appendNamesToFile(originalNames1, filename)
        loadedNames1 = ifpmodule.loadNamesFromFile(filename)
        self.assertEqual(originalNames1, loadedNames1)

        ifpmodule.appendNamesToFile(originalNames2, filename)
        loadedNames2 = ifpmodule.loadNamesFromFile(filename)
        combinedNames = originalNames1
        combinedNames.update(originalNames2)
        self.assertEqual(combinedNames, loadedNames2)

    def test_save_and_retrieve_last_sequence(self):
        originalSequence = 'ROFL'
        ifpmodule.saveLastSequenceToFile(originalSequence, '/tmp/testsequence.txt')
        sequenceFromFile = ifpmodule.getLastSequenceFromFile('/tmp/testsequence.txt')
        self.assertEqual(originalSequence, sequenceFromFile)

    def test_get_new_names(self):
        existingNames = {
            "MARK MADEJ (CO)",
            "BETH MADEJ (CO)",
            "HANNAH DEE SMITH (MS)",
            "MARKUS HAYMAN (MS)"
        }
        actualNewName = "TONY SPREDEMAN (FL)"
        newNames = {
            "MARKUS HAYMAN (MS)",
            actualNewName,
            "HANNAH DEE SMITH (MS)"
        }

        derivedNewNames = ifpmodule.getUniqueNewNamesOnlyFromAllNamesAndNewList(existingNames, newNames)
        self.assertEqual(len(derivedNewNames), 1)
        self.assertEqual(list(derivedNewNames)[0], actualNewName)

    def test_empty_file(self):
        names = {
            "MARK MADEJ (CO)",
            "BETH MADEJ (CO)"
        }
        emptyFilename = '/tmp/testempty.txt'
        ifpmodule.saveNamesToNewFile(names, emptyFilename)
        loadedNames = ifpmodule.loadNamesFromFile(emptyFilename)
        self.assertEqual(len(loadedNames), 2)
        ifpmodule.emptyFile(emptyFilename)
        loadedNames = ifpmodule.loadNamesFromFile(emptyFilename)
        self.assertEqual(len(loadedNames), 0)

    def test_create_points_string(self):
        existingNames = [
            "MARK MADEJ (CO)",
            "BETH MADEJ (CO)",
            "HANNAH DEE SMITH (MS)",
            "MARKUS HAYMAN (MS)"
        ]

        points = [
            (1600, 1601, 1602, 1603),
            (1000, 1100, 1200, 1300),
            (1555, 1666, 1777, 1888),
            (5555, 6666, 7777, 8888)
        ]

        desiredPointStrings = [
            "MARK MADEJ (CO)$$$$1600,1601,1602,1603",
            "BETH MADEJ (CO)$$$$1000,1100,1200,1300",
            "HANNAH DEE SMITH (MS)$$$$1555,1666,1777,1888",
            "MARKUS HAYMAN (MS)$$$$5555,6666,7777,8888"
        ]

        for i in range(0, len(existingNames)):
            pointString = ifpmodule.createPointStringFromNameAndPoints(existingNames[i], points[i])
            self.assertEqual(pointString, desiredPointStrings[i])

if __name__ == '__main__':
    unittest.main()
