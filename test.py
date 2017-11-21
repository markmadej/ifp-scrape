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


if __name__ == '__main__':
    unittest.main()
