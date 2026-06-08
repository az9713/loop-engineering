import unittest
from dates import is_weekend


class TestDates(unittest.TestCase):
    def test_is_weekend(self):
        self.assertTrue(is_weekend(5))    # Saturday
        self.assertTrue(is_weekend(6))    # Sunday
        self.assertFalse(is_weekend(0))   # Monday
        self.assertFalse(is_weekend(4))   # Friday


if __name__ == "__main__":
    unittest.main()
