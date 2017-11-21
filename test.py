import unittest
import ifpscrape

class TestIfpScrape(unittest.TestCase):

    def test_upper(self):


        pointStrings = [
            "2325/1714 Singles/Doubles Points<br>EXPERT"
            ]

        resultTuples = [
            (2325, 1714, 0, 0)
        ]

        for i in range(0, len(pointStrings)):
            self.assertEqual(ifpscrape.getRankFromText(pointStrings[i]), resultTuples[i])


if __name__ == '__main__':
    unittest.main()
