"""
Datastructures collection.
"""

from itertools import chain
from collections import deque
from copy import deepcopy
from .interval import Interval


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
        self.consolidate_intervals()

    @staticmethod
    def _interval_sort_function(interval):
        return interval.start

    def __repr__(self):
        return "IntegerSet(" + ", ".join(str(range_) for range_ in self.intervals) + ")"

    def __eq__(self, other):
        """
        An integer set is equal if all of their intervals are equal.
        """
        return self.intervals == other.intervals

    def __or__(self, other):
        """
        Union.
        """
        copy = deepcopy(self)
        copy |= other
        return copy

    def __ior__(self, other):
        """
        In-place union.
        """
        for other_interval in other.intervals:
            for interval in self.generate_overlaps(other_interval):
                other_interval |= interval
                self.intervals.remove(interval)

            self.intervals.add(other_interval)

        return self

    def __and__(self, other):
        """
        Intersection.
        """
        copy = deepcopy(self)
        copy &= other
        return copy

    def __iand__(self, other):
        """
        In-place intersection.
        """
        new_intervals = []

        for other_interval in other.intervals:
            for interval in self.generate_overlaps(other_interval):
                new_intervals.append(other_interval & interval)

        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
        return self

    def __sub__(self, other):
        """
        Subtraction.
        """
        copy = deepcopy(self)
        copy -= other
        return copy

    def __isub__(self, other):
        """
        In-place subtraction.
        """
        for other_interval in other.intervals:
            for interval in self.generate_overlaps(other_interval):
                self.intervals.update(interval - other_interval)
                self.intervals.remove(interval)

        return self

    def __xor__(self, other):
        """
        Symmetric difference.
        """
        copy = deepcopy(self)
        copy ^= other
        return copy

    def __ixor__(self, other):
        """
        In-place xor/symmetric difference.
        """
        new_intervals = ((self - other) | (other - self)).intervals
        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
        self.consolidate_intervals()
        return self

    def __contains__(self, other):
        for interval in self.intervals:
            if other in interval:
                return True

        return False

    def __le__(self, other):
        return len(self) == len(self & other)

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return len(other) == len(other & self)

    def __gt__(self, other):
        return self >= other and self != other

    def __len__(self):
        return sum(len(interval) for interval in self.intervals)

    def union(self, *others):
        copy = deepcopy(self)

        for other in others:
            copy |= other

        return copy

    def intersection(self, *others):
        copy = deepcopy(self)

        for other in others:
            copy &= other

        return copy

    def difference(self, *others):
        copy = deepcopy(self)

        for other in others:
            copy -= other

        return copy

    def symmetric_difference(self, other):
        return self ^ other

    def issubset(self, other):
        return self <= other

    def isdisjoint(self, other):
        """
        Retur true if self has no common elements with other.
        """
        return len(self & other) == 0

    def issuperset(self, other):
        return self >= other

    def generate_greater(self, interval_1, idx=None):
        """
        Yield overlapping intervals greater than the supplied interval.  Stop
        iterating at the first non overlapping self interval.
        """
        idx = self.intervals.bisect_left(interval_1) if idx is None else idx
        overlaps = deque()

        while idx < len(self.intervals):

            interval_0 = self.intervals[idx]

            if interval_0.overlap(interval_1):
                overlaps.append(interval_0)

            else:
                break

            idx += 1
        yield from overlaps

    def generate_lesser(self, interval_1, idx=None):
        """
        Yield overlapping intervals less than the supplied interval.  Stop
        iterating at the first non overlapping self interval.
        """
        idx = self.intervals.bisect_left(interval_1) if idx is None else idx
        overlaps = deque()

        while idx > 0:
            idx -= 1

            interval_0 = self.intervals[idx]

            if interval_0.overlap(interval_1):
                overlaps.append(interval_0)

            else:
                break

        yield from overlaps

    def generate_overlaps(self, interval_1):
        """
        Yield every interval of self that overlaps with other interval.  The
        implementation takes advantage of the fact that the intervals are sorted
        to stop iteration at the first self interval that does not overlap with
        other interval.
        """
        idx = self.intervals.bisect_left(interval_1)
        yield from chain(
            self.generate_greater(interval_1, idx),
            self.generate_lesser(interval_1, idx),
        )

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

    def copy(self):
        return deepcopy(self)
