import unittest
from .data_structures import Interval


class TestUnion(unittest.TestCase):

    def test_increasing_increasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(10, 20)
        actual = interval_0 | interval_1
        expected = Interval(0, 20)
        self.assertEqual(actual, expected)

    def test_increasing_increasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 0)
        actual = interval_0 | interval_1
        expected = Interval(-10, 10)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 10)
        actual = interval_0 | interval_1
        expected = Interval(0, 20)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(0, -10)
        actual = interval_0 | interval_1
        expected = Interval(-10, 10)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_right_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 10)
        actual = interval_0 | interval_1
        expected = Interval(20, 0)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_left_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(0, -10)
        actual = interval_0 | interval_1
        expected = Interval(10, -10)
        self.assertEqual(actual, expected)

    def test_left_contains_right(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 | interval_1
        expected = Interval(0, 10)
        self.assertEqual(actual, expected)

    def test_right_contains_left(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 | interval_1
        expected = Interval(-1, 11)
        self.assertEqual(actual, expected)

    def test_no_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        with self.assertRaises(ValueError):
            actual = interval_0 | interval_1


class TestIntersection(unittest.TestCase):

    def test_increasing_increasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, 20)
        actual = interval_0 & interval_1
        expected = Interval(5, 10)
        self.assertEqual(actual, expected)

    def test_increasing_increasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 5)
        actual = interval_0 & interval_1
        expected = Interval(0, 5)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 5)
        actual = interval_0 & interval_1
        expected = Interval(5, 10)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, -10)
        actual = interval_0 & interval_1
        expected = Interval(0, 5)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_right_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 5)
        actual = interval_0 & interval_1
        expected = Interval(10, 5)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_left_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(5, -10)
        actual = interval_0 & interval_1
        expected = Interval(5, 0)
        self.assertEqual(actual, expected)

    def test_left_contains_right(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 & interval_1
        expected = Interval(1, 9)
        self.assertEqual(actual, expected)

    def test_right_contains_left(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 & interval_1
        expected = Interval(0, 10)
        self.assertEqual(actual, expected)

    def test_no_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        with self.assertRaises(ValueError):
            actual = interval_0 | interval_1


class TestSubtraction(unittest.TestCase):

    def test_increasing_increasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, 20)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 4),))

    def test_increasing_increasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 5)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(6, 10),))

    def test_increasing_decreasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 5)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 4),))

    def test_increasing_decreasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, -10)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(6, 10),))

    def test_decreasing_decreasing_right_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 5)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(4, 0),))

    def test_decreasing_decreasing_left_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(5, -10)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(10, 6),))

    def test_left_contains_right(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 0), Interval(10, 10)))

    def test_right_contains_left(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 - interval_1
        self.assertEqual(actual, tuple())

    def test_no_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 10),))


class TestSymmetricDifference(unittest.TestCase):

    def test_increasing_increasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, 20)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 4), Interval(11, 20)))

    def test_increasing_increasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 5)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(6, 10), Interval(-10, -1)))

    def test_increasing_decreasing_right_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 5)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 4), Interval(20, 11)))

    def test_increasing_decreasing_left_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, -10)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(6, 10), Interval(-1, -10)))

    def test_decreasing_decreasing_right_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 5)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(4, 0), Interval(20, 11)))

    def test_decreasing_decreasing_left_overlap(self):
        interval_0 = Interval(10, 0)
        interval_1 = Interval(5, -10)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(10, 6), Interval(-1, -10)))

    def test_left_contains_right(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 0), Interval(10, 10)))

    def test_right_contains_left(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(-1, -1), Interval(11, 11)))

    def test_no_overlap(self):
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 10), Interval(11, 20)))


class TestMiscellaneous(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(hash(Interval(0, 1)), hash(Interval(0, 1)))
        self.assertNotEqual(hash(Interval(0, 1)), hash(Interval(1, 0)))
