import unittest

import voicesep as vs


class Test(unittest.TestCase):

    def setUp(self):

        name = self._testMethodName
        sheet = "{}.xml".format(name)

        self.score = vs.Score(name, sheet)

    def test_str(self):

        pass
        #self.assertEqual(self.name, "test_str")


if __name__ == "__main__":
    unittest.main()
