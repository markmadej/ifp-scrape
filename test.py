import unittest
import ifpscrape
import os

class TestIfpScrape(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.remove('/tmp/testfile1.txt')
            os.remove('/tmp/testfile2.txt')
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove('/tmp/testfile1.txt')
            os.remove('/tmp/testfile2.txt')
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
            self.assertEqual(ifpscrape.getRankFromText(pointStrings[i]), resultTuples[i])

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
            "Z"
        ]
        nextCrawlSequence = [
            "B",
            "ABD",
            "MARKMADEK",
            "D",
            None
        ]
        for i in range(0, len(currentSequence)):
            self.assertEqual(ifpscrape.getNextSameLevelSequence(
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
            self.assertEqual(ifpscrape.getNextDeeperLevelSequence(
                currentSequence[i]), nextCrawlSequence[i])

    def test_files_write_and_read_same_data(self):
        originalNames = {
            "MARK MADEJ (CO)",
            "TONY SPREDEMAN (FL)",
            "HANNAH DEE SMITH (MS)",
            "MARKUS HAYMAN (MS)"
        }
        filename = '/tmp/testfile1.txt'
        ifpscrape.saveNamesToNewFile(originalNames, filename)
        loadedNames = ifpscrape.loadNamesFromFile(filename)
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

        ifpscrape.appendNamesToFile(originalNames1, filename)
        loadedNames1 = ifpscrape.loadNamesFromFile(filename)
        self.assertEqual(originalNames1, loadedNames1)

        ifpscrape.appendNamesToFile(originalNames2, filename)
        loadedNames2 = ifpscrape.loadNamesFromFile(filename)
        combinedNames = originalNames1
        combinedNames.update(originalNames2)
        self.assertEqual(combinedNames, loadedNames2)

if __name__ == '__main__':
    unittest.main()
