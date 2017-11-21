import unittest
import ifpscrape

class TestIfpScrape(unittest.TestCase):

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




if __name__ == '__main__':
    unittest.main()
