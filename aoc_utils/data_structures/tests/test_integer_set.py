import unittest
from ..integer_set import IntegerSet


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

    def test_contains_empty_set(self):
        """
        Ensure an empty set can be checked.
        """
        set_0 = IntegerSet()
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
        Validate __le__ (subset).
        """
        self.assertTrue(IntegerSet((0, 10)) <= IntegerSet((0, 10)))
        self.assertTrue(IntegerSet((0, 1), (9, 10)) <= IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((-1, -1), (9, 10)) <= IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((0, 1), (11, 11)) <= IntegerSet((0, 10)))

    def test_lt(self):
        """
        Validate __lt__ (proper subset).
        """
        self.assertFalse(IntegerSet((0, 10)) < IntegerSet((0, 10)))
        self.assertTrue(IntegerSet((0, 1), (9, 10)) < IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((-1, -1), (9, 10)) < IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((0, 1), (11, 11)) < IntegerSet((0, 10)))

    def test_issuperset(self):
        """
        Validate superset.
        """
        self.assertTrue(IntegerSet((0, 10)).issuperset(IntegerSet((0, 10))))
        self.assertTrue(IntegerSet((-1, 1), (2, 11)).issuperset(IntegerSet((0, 10))))
        self.assertFalse(IntegerSet((-1, 9)).issuperset(IntegerSet((0, 10))))
        self.assertFalse(IntegerSet((1, 11)).issuperset(IntegerSet((0, 10))))

    def test_ge(self):
        """
        Validate __ge__ (superset).
        """
        self.assertTrue(IntegerSet((0, 10)) >= IntegerSet((0, 10)))
        self.assertTrue(IntegerSet((-1, 1), (2, 11)) >= IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((-1, 9)) >= IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((1, 11)) >= IntegerSet((0, 10)))

    def test_gt(self):
        """
        Validate __gt__ (proper superset).
        """
        self.assertFalse(IntegerSet((0, 10)) > IntegerSet((0, 10)))
        self.assertTrue(IntegerSet((-1, 1), (2, 11)) > IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((-1, 9)) > IntegerSet((0, 10)))
        self.assertFalse(IntegerSet((1, 11)) > IntegerSet((0, 10)))

    def test_union(self):
        self.assertEqual(
            IntegerSet((0, 10)).union(IntegerSet((20, 30)), IntegerSet((40, 50))),
            IntegerSet((0, 10), (20, 30), (40, 50)),
        )

    def test_intersection(self):
        self.assertEqual(
            IntegerSet((0, 10)).intersection(IntegerSet((-10, 8)), IntegerSet((2, 20))),
            IntegerSet((2, 8)),
        )

    def test_difference(self):
        self.assertEqual(
            IntegerSet((0, 10)).difference(IntegerSet((1, 2)), IntegerSet((8, 9))),
            IntegerSet((0, 0), (3, 7), (10, 10)),
        )

    def test_symmetric_difference(self):
        self.assertEqual(
            IntegerSet((0, 10)).symmetric_difference(
                IntegerSet((-5, 2), (4, 6), (8, 15))
            ),
            IntegerSet((-5, -1), (3, 3), (7, 7), (11, 15)),
        )

    def test_copy(self):
        set_0 = IntegerSet((0, 10))
        set_1 = set_0.copy()
        self.assertEqual(set_0, set_1)
        self.assertNotEqual(id(set_0), id(set_1))
        set_0 |= IntegerSet((10, 11))
        self.assertNotEqual(set_0, set_1)

    def test_update(self):
        set_0 = IntegerSet((0, 10))
        id_0 = id(set_0)
        set_0.update(IntegerSet((20, 30)), IntegerSet((30, 40)))
        self.assertEqual(set_0, IntegerSet((0, 10), (20, 40)))
        self.assertEqual(id(set_0), id_0)

    def test_intersection_update(self):
        set_0 = IntegerSet((0, 10))
        id_0 = id(set_0)
        set_0.intersection_update(IntegerSet((-10, 8)), IntegerSet((2, 20)))
        self.assertEqual(set_0, IntegerSet((2, 8)))
        self.assertEqual(id(set_0), id_0)

    def test_difference_update(self):
        set_0 = IntegerSet((0, 10))
        id_0 = id(set_0)
        set_0.difference_update(IntegerSet((-10, 1)), IntegerSet((9, 20)))
        self.assertEqual(set_0, IntegerSet((2, 8)))
        self.assertEqual(id(set_0), id_0)

    def test_symmetric_difference_update(self):
        set_0 = IntegerSet((0, 20))
        id_0 = id(set_0)
        set_0.symmetric_difference_update(IntegerSet((10, 30)))
        self.assertEqual(set_0, IntegerSet((0, 9), (21, 30)))
        self.assertEqual(id(set_0), id_0)

    def test_add(self):
        set_0 = IntegerSet((0, 10))
        set_0.add(12)
        self.assertEqual(set_0, IntegerSet((0, 10), (12, 12)))
        set_0.add(11)
        self.assertEqual(set_0, IntegerSet((0, 12)))

    def test_remove(self):
        set_0 = IntegerSet((0, 10))
        set_0.remove(5)
        self.assertEqual(set_0, IntegerSet((0, 4), (6, 10)))
        with self.assertRaises(KeyError):
            set_0.remove(11)

    def test_discard(self):
        set_0 = IntegerSet((0, 10))
        set_0.discard(5)
        self.assertEqual(set_0, IntegerSet((0, 4), (6, 10)))
        set_0.discard(11)
        self.assertEqual(set_0, IntegerSet((0, 4), (6, 10)))

    def test_pop(self):
        set_0 = IntegerSet((0, 1))
        self.assertIn(set_0.pop(), (0, 1))
        self.assertIn(set_0.pop(), (0, 1))
        with self.assertRaises(KeyError):
            set_0.pop()

    def test_clear(self):
        set_0 = IntegerSet((0, 1))
        set_0.clear()
        self.assertEqual(set_0, IntegerSet())

    def test_iter(self):
        elements = set()

        for element in IntegerSet((0, 2), (10, 12)):
            elements.add(element)

        self.assertEqual(elements, {0, 1, 2, 10, 11, 12})
