"""
Test the vector tuple class.
"""

import unittest
from ..vector_tuple import VectorTuple


class TestVectorTuple(unittest.TestCase):
    """
    Test the vector tuple class.
    """

    def test_add(self):
        self.assertEqual(
            VectorTuple(1, 1) + VectorTuple(1, 2),
            VectorTuple(2, 3),
        )
