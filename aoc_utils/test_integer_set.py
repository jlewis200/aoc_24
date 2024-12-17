import unittest
from .data_structures import IntegerSet


class TestUnion(unittest.TestCase):

    def test_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        set_0 |= set_1
        self.assertEqual(id(set_0), id_0)
        self.assertEqual(id(set_1), id_1)

    def test_not_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        result = set_0 | set_1
        self.assertNotIn(id(result), (id_0, id_1))
        self.assertNotIn(id(result), (id_0, id_1))

    def test_non_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10)) | IntegerSet((20, 30)),
            IntegerSet((0, 10), (20, 30)),
        )

    def test_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10), (20, 30), (40, 50)) | IntegerSet((10, 20), (30, 40)),
            IntegerSet((0, 50)),
        )


class TestIntersection(unittest.TestCase):

    def test_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        set_0 &= set_1
        self.assertEqual(id(set_0), id_0)
        self.assertEqual(id(set_1), id_1)

    def test_not_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        result = set_0 & set_1
        self.assertNotIn(id(result), (id_0, id_1))
        self.assertNotIn(id(result), (id_0, id_1))

    def test_non_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10)) & IntegerSet((20, 30)),
            IntegerSet(),
        )

    def test_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10)) & IntegerSet((5, 30)),
            IntegerSet((5, 10)),
        )

    def test_multi_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10), (20, 30), (40, 50)) & IntegerSet((-10, 2), (8, 42)),
            IntegerSet((0, 2), (8, 10), (20, 30), (40, 42)),
        )


class TestSubtraction(unittest.TestCase):

    def test_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        set_0 -= set_1
        self.assertEqual(id(set_0), id_0)
        self.assertEqual(id(set_1), id_1)

    def test_not_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        result = set_0 - set_1
        self.assertNotIn(id(result), (id_0, id_1))
        self.assertNotIn(id(result), (id_0, id_1))

    def test_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10)) - IntegerSet((-5, 2), (4, 6), (8, 15)),
            IntegerSet((3, 3), (7, 7)),
        )

    def test_non_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10)) - IntegerSet((-10, -1), (11, 20)),
            IntegerSet((0, 10)),
        )


class TestSymmetricDifference(unittest.TestCase):
    """ """

    def test_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        set_0 ^= set_1
        self.assertEqual(id(set_0), id_0)
        self.assertEqual(id(set_1), id_1)

    def test_not_in_place(self):
        set_0 = IntegerSet((0, 10))
        set_1 = IntegerSet((5, 20))
        id_0 = id(set_0)
        id_1 = id(set_1)
        result = set_0 ^ set_1
        self.assertNotIn(id(result), (id_0, id_1))
        self.assertNotIn(id(result), (id_0, id_1))

    def test_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10)) ^ IntegerSet((-5, 2), (4, 6), (8, 15)),
            IntegerSet((-5, -1), (3, 3), (7, 7), (11, 15)),
        )

    def test_multi_overlapping(self):
        self.assertEqual(
            IntegerSet((0, 10), (20, 30), (40, 50)) ^ IntegerSet((4, 6), (25, 45)),
            IntegerSet((0, 3), (7, 10), (20, 24), (31, 39), (46, 50)),
        )

    def test_no_overlap(self):
        self.assertEqual(
            IntegerSet((0, 10), (20, 30)) ^ IntegerSet((-10, -1), (11, 19)),
            IntegerSet((-10, 30)),
        )


class TestMiscellaneous(unittest.TestCase):

    def test_hash(self):
        """
        Ensure identical objects with different id are equal
        """
        set_0 = IntegerSet((0, 10), (20, 30))
        set_1 = IntegerSet((0, 10), (20, 30))
        id_0 = id(set_0)
        id_1 = id(set_1)
        self.assertEqual(set_0, set_1)
        self.assertNotEqual(id_0, id_1)

    def test_contains(self):
        """
        Ensure each set is tested for the supplied element.
        """
        set_0 = IntegerSet((0, 10), (20, 30))
        self.assertIn(0, set_0)
        self.assertIn(10, set_0)
        self.assertIn(20, set_0)
        self.assertIn(30, set_0)
        self.assertNotIn(-1, set_0)
        self.assertNotIn(11, set_0)
        self.assertNotIn(19, set_0)
        self.assertNotIn(31, set_0)

    def test_isdisjoint(self):
        """
        Ensure isdisjoint return true if no common elements, and false if
        common elements exist.
        """
        self.assertFalse(IntegerSet((0, 10)).isdisjoint(IntegerSet((0, 0))))
        self.assertTrue(IntegerSet((0, 10)).isdisjoint(IntegerSet((-1, -1))))
        self.assertTrue(IntegerSet((0, 10)).isdisjoint(IntegerSet((11, 11))))

    def test_issubset(self):
        """
        Validate issubset.
        """
        self.assertTrue(IntegerSet((0, 10)).issubset(IntegerSet((0, 10))))
        self.assertTrue(IntegerSet((0, 1), (9, 10)).issubset(IntegerSet((0, 10))))
        self.assertFalse(IntegerSet((-1, -1), (9, 10)).issubset(IntegerSet((0, 10))))
        self.assertFalse(IntegerSet((0, 1), (11, 11)).issubset(IntegerSet((0, 10))))

    def test_le(self):
        """
        Validate __le__.
        """
        self.assertTrue(IntegerSet((0, 10)) <= IntegerSet((0, 10)))
        self.assertTrue(IntegerSet((0, 1), (9, 10)) <= IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((-1, -1), (9, 10)) <= IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((0, 1), (11, 11)) <= IntegerSet((0, 10)))

    def test_lt(self):
        """
        Validate __lt__.
        """
        self.assertFalse(IntegerSet((0, 10)) < IntegerSet((0, 10)))
        self.assertTrue(IntegerSet((0, 1), (9, 10)) < IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((-1, -1), (9, 10)) < IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((0, 1), (11, 11)) < IntegerSet((0, 10)))

    def test_is_proper_subset(self):
        """ """

    def test_issuperset(self):
        """ """

    def test_is_proper_superset(self):
        """ """

    def test_union(self):
        """ """

    def test_intersection(self):
        """ """

    def test_difference(self):
        """ """

    def test_symmetric_difference(self):
        """ """

    def test_len(self):
        """ """
