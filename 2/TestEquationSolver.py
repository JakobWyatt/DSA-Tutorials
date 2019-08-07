import unittest
from EquationSolver import solve

class TestEquationSolver(unittest.TestCase):
    def testSingleNum(self):
        self.assertAlmostEqual(1.0, solve("1"), places=3)

    def testAddition(self):
        self.assertAlmostEqual(1.0 + 3.0, solve("1 + 3"), places=3)

    def testDivision(self):
        self.assertAlmostEqual(1.0 / 3.0, solve("1 / 3"), places=3)

    def testPrecedence(self):
        self.assertAlmostEqual(9.0 - 1.0 / 3.0 * 6.0 - 4.0 * 3.0,
            solve("9 - 1 / 3 * 6 - 4 * 3"), places=3)

    def testBrackets(self):
        self.assertAlmostEqual((9.0 - 1.0) / (3.0 * 6.0 - 4.0) * 3.0,
            solve("( 9 - 1 ) / ( 3 * 6 - 4 ) * 3"), places=3)

    def testLecs(self):
        self.assertAlmostEqual((10.3 * (14 + 3.2)) / (5 + 2 - 4 * 3),
            solve("( 10.3 * ( 14 + 3.2 ) ) / ( 5 + 2 - 4 * 3 )"), places=3)

if __name__ == "__main__":
    unittest.main()
