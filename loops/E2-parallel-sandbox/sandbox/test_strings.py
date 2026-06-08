import unittest
from strings import shout


class TestStrings(unittest.TestCase):
    def test_shout(self):
        self.assertEqual(shout("hi"), "HI!")
        self.assertEqual(shout("Go"), "GO!")


if __name__ == "__main__":
    unittest.main()
