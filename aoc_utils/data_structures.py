"""
Datastructures collection.
"""

from itertools import chain
from collections import deque
from copy import deepcopy


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
        Check if self is a subset of other.
        """
        return len(self & other) == len(self)

    def __lt__(self, other):
        """
        Check if is a proper subser of other.
        """
        return self != other and self <= other

    def __ge__(self, other):
        """
        Check if self is a superset of other.
        """
        return len(self & other) == len(other)

    def __gt__(self, other):
        """
        Check if is a proper superset of other.
        """
        return self != other and self >= other

    def __xor__(self, other):
        """
        Symmetric difference, xor of set elements.
        """
        return (self - other) + (other - self)

    def isdisjoint(self, other):
        return not self.overlap(other)

    def issubset(self, other):
        return self <= other

    def issuperset(self, other):
        return self >= other

    def union(self, *others):
        for other in others:
            self |= other
        return self

    def intersection(self, *others):
        for other in others:
            self &= other
        return self

    def difference(self, *others):
        left_operands = [self]

        for other in others:
            next_left_operands = []

            for left_operand in left_operands:
                next_left_operands.extend(left_operand - other)

            left_operands = next_left_operands

        return tuple(left_operands)

    def symmetric_difference(self, other):
        return self ^ other

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


class Range:

    def __init__(self, start, stop=None):
        if stop is None:
            stop = start
            start = 0

        self.start = start
        self.stop = stop

    def __contains__(self, other):
        return other >= self.start and other < self.stop

    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return f"Range({self.start}, {self.stop})"


from sortedcontainers import SortedList


class IntegerSet:
    """
    Set of integers with a sparse implementaton.  This is suitable for sets
    with a large number of contiguous integers.
    """

    def __init__(self, *ranges):
        self.intervals = [Interval(*range_) for range_ in ranges]
        self.intervals = SortedList(self.intervals, key=self._interval_sort_function)

    @staticmethod
    def _interval_sort_function(interval):
        return interval.start

    def __repr__(self):
        return "IntegerSet(" + ", ".join(str(range_) for range_ in self.intervals) + ")"

    def __eq__(self, other):
        return self.intervals == other.intervals

    def __or__(self, other):
        copy = deepcopy(self)
        copy |= other
        return copy

    def __and__(self, other):
        copy = deepcopy(self)
        copy &= other
        return copy

    def __sub__(self, other):
        copy = deepcopy(self)
        copy -= other
        return copy

    def __xor__(self, other):
        copy = deepcopy(self)
        copy ^= other
        return copy

    def generate_greater(self, interval_1, idx=None):
        """
        Remove and yield overlapping intervals greater than the supplied interval.
        """
        idx = self.intervals.bisect_left(interval_1) if idx is None else idx
        overlaps = deque()

        while idx < len(self.intervals):

            try:
                interval_0 = self.intervals[idx]

                if interval_0.overlap(interval_1):
                    overlaps.append(interval_0)

                else:
                    break

            except IndexError:
                break

            idx += 1
        yield from overlaps

    def generate_lesser(self, interval_1, idx=None):
        """
        Remove and yield overlapping intervals less than the supplied interval.
        """
        idx = self.intervals.bisect_left(interval_1) if idx is None else idx
        overlaps = deque()

        while idx > 0:
            idx = max(idx - 1, 0)

            try:
                interval_0 = self.intervals[idx]

                if interval_0.overlap(interval_1):
                    overlaps.append(interval_0)

                else:
                    break

            except IndexError:
                break

        yield from overlaps

    def generate_overlaps(self, interval_1):
        idx = self.intervals.bisect_left(interval_1)
        yield from chain(
            self.generate_greater(interval_1, idx),
            self.generate_lesser(interval_1, idx),
        )

    def __ior__(self, other):

        for other_interval in other.intervals:
            for interval in self.generate_overlaps(other_interval):
                other_interval |= interval
                self.intervals.remove(interval)

            self.intervals.add(other_interval)

        return self

    def __iand__(self, other):
        new_intervals = []

        for other_interval in other.intervals:
            for interval in self.generate_overlaps(other_interval):
                new_intervals.append(other_interval & interval)

        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
        return self

    def __isub__(self, other):

        for other_interval in other.intervals:
            for interval in self.generate_overlaps(other_interval):
                self.intervals.update(interval - other_interval)
                self.intervals.remove(interval)

        return self

    def __ixor__(self, other):
        new_intervals = ((self - other) | (other - self)).intervals
        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
        self.consolidate_intervals()
        return self

    def consolidate_intervals(self):
        """
        Consolidate adjacent/overlapping intervals into one larger interval.


        Ex:
        >>> iset = IntegerSet((0, 10), (11, 20))
        >>> iset.consolidate_intervals()
        >>> iset
        IntegerSet((0, 20))
        """
        new_intervals = []
        intervals = deque(self.intervals)

        while len(intervals) > 1:
            interval_0 = intervals.popleft()
            interval_1 = intervals.popleft()

            if interval_0.end + 1 in interval_1:
                interval = Interval(interval_0.start, interval_1.end)
                intervals.appendleft(interval)

            else:
                new_intervals.append(interval_0)
                intervals.appendleft(interval_1)

        new_intervals.extend(intervals)
        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
