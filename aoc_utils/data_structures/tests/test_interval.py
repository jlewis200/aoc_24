"""
Test the interval data structure.
"""

import unittest
from ..interval import Interval


class TestUnion(unittest.TestCase):
    """
    Test union operator.
    """

    def test_increasing_increasing_right_overlap(self):
        """
        Test increasing-increasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(10, 20)
        actual = interval_0 | interval_1
        expected = Interval(0, 20)
        self.assertEqual(actual, expected)

    def test_increasing_increasing_left_overlap(self):
        """
        Test increasing-increasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 0)
        actual = interval_0 | interval_1
        expected = Interval(-10, 10)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_right_overlap(self):
        """
        Test increasing-decreasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 10)
        actual = interval_0 | interval_1
        expected = Interval(0, 20)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_left_overlap(self):
        """
        Test increasing-decreasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(0, -10)
        actual = interval_0 | interval_1
        expected = Interval(-10, 10)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_right_overlap(self):
        """
        Test decreasing-decreasing right overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 10)
        actual = interval_0 | interval_1
        expected = Interval(20, 0)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_left_overlap(self):
        """
        Test decreasing-decreasing left overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(0, -10)
        actual = interval_0 | interval_1
        expected = Interval(10, -10)
        self.assertEqual(actual, expected)

    def test_left_contains_right(self):
        """
        Test left contains right.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 | interval_1
        expected = Interval(0, 10)
        self.assertEqual(actual, expected)

    def test_right_contains_left(self):
        """
        Test right contains left.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 | interval_1
        expected = Interval(-1, 11)
        self.assertEqual(actual, expected)

    def test_no_overlap(self):
        """
        Test no overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        with self.assertRaises(ValueError):
            _ = interval_0 | interval_1


class TestIntersection(unittest.TestCase):
    """
    Test & operator.
    """

    def test_increasing_increasing_right_overlap(self):
        """
        Test increasing-increasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, 20)
        actual = interval_0 & interval_1
        expected = Interval(5, 10)
        self.assertEqual(actual, expected)

    def test_increasing_increasing_left_overlap(self):
        """
        Test increasing-increasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 5)
        actual = interval_0 & interval_1
        expected = Interval(0, 5)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_right_overlap(self):
        """
        Test increasing-decreasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 5)
        actual = interval_0 & interval_1
        expected = Interval(5, 10)
        self.assertEqual(actual, expected)

    def test_increasing_decreasing_left_overlap(self):
        """
        Test increasing-decreasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, -10)
        actual = interval_0 & interval_1
        expected = Interval(0, 5)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_right_overlap(self):
        """
        Test decreasing-decreasing right overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 5)
        actual = interval_0 & interval_1
        expected = Interval(10, 5)
        self.assertEqual(actual, expected)

    def test_decreasing_decreasing_left_overlap(self):
        """
        Test decreasing-decreasing left overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(5, -10)
        actual = interval_0 & interval_1
        expected = Interval(5, 0)
        self.assertEqual(actual, expected)

    def test_left_contains_right(self):
        """
        Test left contains right.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 & interval_1
        expected = Interval(1, 9)
        self.assertEqual(actual, expected)

    def test_right_contains_left(self):
        """
        Test right contains left.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 & interval_1
        expected = Interval(0, 10)
        self.assertEqual(actual, expected)

    def test_no_overlap(self):
        """
        Test no overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        with self.assertRaises(ValueError):
            _ = interval_0 | interval_1


class TestSubtraction(unittest.TestCase):
    """
    Test - operator.
    """

    def test_increasing_increasing_right_overlap(self):
        """
        Test increasing-increasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, 20)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 4),))

    def test_increasing_increasing_left_overlap(self):
        """
        Test increasing-increasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 5)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(6, 10),))

    def test_increasing_decreasing_right_overlap(self):
        """
        Test increasing-decreasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 5)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 4),))

    def test_increasing_decreasing_left_overlap(self):
        """
        Test increasing-decreasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, -10)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(6, 10),))

    def test_decreasing_decreasing_right_overlap(self):
        """
        Test decreasing-decreasing right overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 5)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(4, 0),))

    def test_decreasing_decreasing_left_overlap(self):
        """
        Test decreasing-decreasing left overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(5, -10)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(10, 6),))

    def test_left_contains_right(self):
        """
        Test left contains right.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 0), Interval(10, 10)))

    def test_right_contains_left(self):
        """
        Test right contains left.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 - interval_1
        self.assertEqual(actual, tuple())

    def test_no_overlap(self):
        """
        Test no overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        actual = interval_0 - interval_1
        self.assertEqual(actual, (Interval(0, 10),))


class TestSymmetricDifference(unittest.TestCase):
    """
    Test ^ operator.
    """

    def test_increasing_increasing_right_overlap(self):
        """
        Test increasing-increasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, 20)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 4), Interval(11, 20)))

    def test_increasing_increasing_left_overlap(self):
        """
        Test increasing-increasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-10, 5)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(6, 10), Interval(-10, -1)))

    def test_increasing_decreasing_right_overlap(self):
        """
        Test increasing-decreasing right overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(20, 5)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 4), Interval(20, 11)))

    def test_increasing_decreasing_left_overlap(self):
        """
        Test increasing-decreasing left overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(5, -10)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(6, 10), Interval(-1, -10)))

    def test_decreasing_decreasing_right_overlap(self):
        """
        Test decreasing-decreasing right overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(20, 5)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(4, 0), Interval(20, 11)))

    def test_decreasing_decreasing_left_overlap(self):
        """
        Test decreasing-decreasing left overlap.
        """
        interval_0 = Interval(10, 0)
        interval_1 = Interval(5, -10)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(10, 6), Interval(-1, -10)))

    def test_left_contains_right(self):
        """
        Test left contains right.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(1, 9)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 0), Interval(10, 10)))

    def test_right_contains_left(self):
        """
        Test right contains left.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(-1, 11)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(-1, -1), Interval(11, 11)))

    def test_no_overlap(self):
        """
        Test no overlap.
        """
        interval_0 = Interval(0, 10)
        interval_1 = Interval(11, 20)
        actual = interval_0 ^ interval_1
        self.assertEqual(actual, (Interval(0, 10), Interval(11, 20)))


class TestMiscellaneous(unittest.TestCase):
    """
    Test miscellaneous methods of the Interval class.
    """

    def test_hash(self):
        """
        Test the hash function.
        """
        self.assertEqual(hash(Interval(0, 1)), hash(Interval(0, 1)))
        self.assertNotEqual(hash(Interval(0, 1)), hash(Interval(1, 0)))

    def test_contains(self):
        """
        Test in operator.
        """
        self.assertIn(0, Interval(0, 0))
        self.assertNotIn(1, Interval(0, 0))
        self.assertNotIn(-1, Interval(0, 0))

    def test_isdisjoint(self):
        """
        Test isdisjoint().
        """
        self.assertTrue(Interval(0, 0).isdisjoint(Interval(1, 1)))
        self.assertFalse(Interval(0, 0).isdisjoint(Interval(0, 1)))

    def test_issubset(self):
        """
        Test issubset().
        """
        self.assertTrue(Interval(0, 10) <= Interval(0, 10))
        self.assertFalse(Interval(-1, 10) <= Interval(0, 10))
        self.assertFalse(Interval(0, 11) <= Interval(0, 10))
        self.assertTrue(Interval(0, 10).issubset(Interval(0, 10)))

    def test_is_proper_subset(self):
        """
        Test < operator.
        """
        self.assertTrue(Interval(1, 10) < Interval(0, 10))
        self.assertTrue(Interval(0, 9) < Interval(0, 10))
        self.assertFalse(Interval(0, 10) < Interval(0, 10))
        self.assertFalse(Interval(-1, 10) < Interval(0, 10))
        self.assertFalse(Interval(0, 11) < Interval(0, 10))

    def test_issuperset(self):
        """
        Test >= operator.
        """
        self.assertTrue(Interval(0, 10) >= Interval(0, 10))
        self.assertFalse(Interval(1, 10) >= Interval(0, 10))
        self.assertFalse(Interval(0, 9) >= Interval(0, 10))
        self.assertTrue(Interval(0, 10).issuperset(Interval(0, 10)))

    def test_is_proper_superset(self):
        """
        Test > operator.
        """
        self.assertTrue(Interval(0, 11) > Interval(0, 10))
        self.assertTrue(Interval(-1, 10) > Interval(0, 10))
        self.assertFalse(Interval(0, 10) > Interval(0, 10))
        self.assertFalse(Interval(1, 10) > Interval(0, 10))
        self.assertFalse(Interval(0, 9) > Interval(0, 10))

    def test_union(self):
        """
        Test union() method.
        """
        actual = Interval(0, 1).union(Interval(1, 2), Interval(2, 3))
        self.assertEqual(actual, Interval(0, 3))

    def test_intersection(self):
        """
        Test intersection() method.
        """
        actual = Interval(0, 10).intersection(Interval(3, 9), Interval(1, 6))
        self.assertEqual(actual, Interval(3, 6))

    def test_difference(self):
        """
        Test difference() method.
        """
        actual = Interval(0, 10).difference(Interval(1, 2), Interval(8, 9))
        self.assertEqual(actual, (Interval(0, 0), Interval(3, 7), Interval(10, 10)))

    def test_symmetric_difference(self):
        """
        Test symmetric_difference() method.
        """
        actual = Interval(0, 10).symmetric_difference(Interval(1, 9))
        self.assertEqual(actual, (Interval(0, 0), Interval(10, 10)))

    def test_len(self):
        """
        Test __len___() method.
        """
        self.assertEqual(len(Interval(0, 0)), 1)
        self.assertEqual(len(Interval(0, 9)), 10)
        self.assertEqual(len(Interval(0, 99)), 100)

    def test_repr(self):
        """
        Test __repr__
        """
        start = 1
        end = 2
        interval_0 = Interval(1, 2)
        self.assertEqual(repr(interval_0), str((start, end)))
