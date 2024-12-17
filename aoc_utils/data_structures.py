"""
Datastructures collection.
"""


class VectorTuple(tuple):
    """
    This class replicates vectorized operations of numpy arrays, with the
    advantage that it's hashable.
    """

    def __new__(self, *args):
        if len(args) == 1 and not isinstance(args[0], tuple):
            args = args[0]
        return tuple.__new__(VectorTuple, args)

    def __add__(self, other):
        return VectorTuple(
            self_element + other_element
            for self_element, other_element in zip(self, other)
        )

    def __sub__(self, other):
        return VectorTuple(
            self_element - other_element
            for self_element, other_element in zip(self, other)
        )

    def __mul__(self, other):
        return VectorTuple(
            self_element * other_element
            for self_element, other_element in zip(self, other)
        )

    def __truediv__(self, other):
        return VectorTuple(
            self_element / other_element
            for self_element, other_element in zip(self, other)
        )

    def __mod__(self, other):
        return VectorTuple(
            self_element % other_element
            for self_element, other_element in zip(self, other)
        )

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))

    def orthogonals(self, board):
        """
        Generate E, N, W, S adjacencies.
        """
        for delta in (
            VectorTuple(0, 1),
            VectorTuple(-1, 0),
            VectorTuple(0, -1),
            VectorTuple(1, 0),
        ):
            next_pos = self + delta
            if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
                yield next_pos

    def diagonals(self, board):
        """
        Generate NE, NW, SW, SE adjacencies.
        """
        for delta in (
            VectorTuple(-1, 1),
            VectorTuple(-1, -1),
            VectorTuple(1, -1),
            VectorTuple(1, 1),
        ):
            next_pos = self + delta
            if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
                yield next_pos


class Interval:
    """
    Interval class to represent contiguous sets of integers.  This
    representation is convenient when the sizes of the sets are very large and
    time/space complexity becomes infeasible.

    start and end are inclusive
    orientation is maintained, so Interval(0, 1) != Interval(1, 0)
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.range = range(min(start, end), max(start, end) + 1)
        self.empty = False
        self._hash = hash((start, end))

    def __repr__(self):
        return str((self.start, self.end))

    def __contains__(self, other):
        return other in self.range

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return self._hash

    def __or__(self, other):
        """
        Union self with other.  Due to the orientation being maintained, this
        is not symmetrical.  The orientation of the left value is maintained.

        Interval(0, 1) | Interval(1, 2) == Interval(0, 2)
        Interval(1, 0) | Interval(1, 2) == Interval(2, 0)
        """
        self.validate_overlap(other)

        values = self.start, self.end, other.start, other.end
        start = min(values)
        end = max(values)

        return Interval(*self._orient_endpoints(start, end))

    def __and__(self, other):
        """
        Intersect self with other.  Orientation of left value is maintained.
        """
        self.validate_overlap(other)

        values = self.start, self.end, other.start, other.end
        _, start, end, _ = sorted(values)

        return Interval(*self._orient_endpoints(start, end))

    def __sub__(self, other):
        """
        Remove the other set from self.  This may result in an empty interval in
        the case of complete overlap, a single interval if no overlap or limited
        overlap, or two intervals if other occurs internal to self.  A tuple of
        2 intervals is always returned.  If a non-empty interval results, it
        will be the first of the 2.
        """
        if not self.overlap(other):
            return (self,)

        intersection = self & other

        start = min(self.start, self.end)
        end = min(other.start, other.end) - 1
        interval_0 = Interval(*self._orient_endpoints(start, end))
        interval_0.empty = start > end

        end = max(self.start, self.end)
        start = max(other.start, other.end) + 1
        interval_1 = Interval(*self._orient_endpoints(start, end))
        interval_1.empty = start > end

        return tuple(
            interval for interval in (interval_0, interval_1) if not interval.empty
        )

    def __len__(self):
        return 1 + max(self.start, self.end) - min(self.start, self.end)

    def __le__(self, other):
        """
        Check if other is a subset of self.
        """
        return len(self & other) == len(other)

    def __xor__(self, other):
        """
        Symmetric difference, xor of set elements.
        """
        return (self - other) + (other - self)

    def isdisjoint(self, other):
        return not self.overlap(other)

    def union(self, *others):
        for other in others:
            self |= other
        return self

    def intersection(self, *other):
        for other in others:
            self &= other
        return self

    def difference(self, other):
        for other in others:
            self -= other
        return self

    def symmetric_difference(self, other):
        for other in others:
            self ^= other
        return self

    def _orient_endpoints(self, start, end):
        if not self.increasing():
            return self.swap(start, end)
        return start, end

    def overlap(self, other):
        return (
            self.start in other
            or self.end in other
            or other.start in self
            or other.end in self
        )

    def validate_overlap(self, other):
        """
        Detect overlap by checking if either endpoint from self is in the other
        interval, or vice versa.
        """
        if not self.overlap(other):
            raise ValueError("Intervals {self} and {other} don't overlap.")

    def increasing(self):
        return self.end > self.start

    @staticmethod
    def swap(value_0, value_1):
        return value_1, value_0
