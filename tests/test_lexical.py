import unittest
from src.lexical import LexicalGroundingChecker

CTX = "Full-time employees receive 20 days of paid vacation per year."

class T(unittest.TestCase):
    def test_faithful(self):
        r = LexicalGroundingChecker().check("Employees receive 20 days of paid vacation.", CTX)
        self.assertEqual(r.faithfulness, 1.0)
    def test_wrong_number(self):
        r = LexicalGroundingChecker().check("Employees receive 30 days of paid vacation.", CTX)
        self.assertEqual(r.faithfulness, 0.0)
    def test_invented(self):
        r = LexicalGroundingChecker().check("The company offers a free gym membership.", CTX)
        self.assertLess(r.faithfulness, 1.0)

if __name__ == "__main__":
    unittest.main()
