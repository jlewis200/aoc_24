"""
Datastructures collection.
"""

from itertools import chain
from collections import deque
from copy import deepcopy
from sortedcontainers import SortedList
from .interval import Interval


class IntegerSet:
    """
    Set of integers with a sparse implementation.  This is suitable for sets
    with a large number of contiguous integers.
    """

    def __init__(self, *intervals):
        intervals = map(lambda interval: Interval(*interval), intervals)
        self.intervals = SortedList(intervals, key=self._interval_sort_function)
        self.consolidate_intervals()

    def __repr__(self):
        intervals = ", ".join(str(range_) for range_ in self.intervals)
        return f"IntegerSet({intervals})"

    def __iter__(self):
        for interval in self.intervals:
            yield from range(interval.start, interval.end + 1)

    def __eq__(self, other):
        """
        An integer set is equal if all of their intervals are equal.
        """
        return self.intervals == other.intervals

    def __or__(self, other):
        """
        Union.
        """
        return self.union(other)

    def __and__(self, other):
        """
        Intersection.
        """
        return self.intersection(other)

    def __sub__(self, other):
        """
        Subtraction.
        """
        return self.difference(other)

    def __xor__(self, other):
        """
        Symmetric difference.
        """
        return self.symmetric_difference(other)

    def __ior__(self, other):
        """
        In-place union.
        """
        for other_interval in other.intervals:
            for interval in self._generate_overlaps(other_interval):
                other_interval |= interval
                self.intervals.remove(interval)
            self.intervals.add(other_interval)
        self.consolidate_intervals()

        return self

    def __iand__(self, other):
        """
        In-place intersection.
        """
        new_intervals = []
        for other_interval in other.intervals:
            for interval in self._generate_overlaps(other_interval):
                new_intervals.append(other_interval & interval)
        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
        return self

    def __isub__(self, other):
        """
        In-place subtraction.
        """
        for other_interval in other.intervals:
            for interval in self._generate_overlaps(other_interval):
                self.intervals.update(interval - other_interval)
                self.intervals.remove(interval)
        return self

    def __ixor__(self, other):
        """
        In-place xor/symmetric difference.
        """
        new_intervals = ((self - other) | (other - self)).intervals
        self.intervals = SortedList(new_intervals, key=self._interval_sort_function)
        self.consolidate_intervals()
        return self

    def __contains__(self, other):
        """
        Does self contain other?
        """
        idx = self.intervals.bisect_left(Interval(other, other))
        contains = False

        try:
            contains |= other in self.intervals[idx]
        except IndexError:
            pass

        try:
            contains |= other in self.intervals[idx - 1]
        except IndexError:
            pass

        return contains

    def __le__(self, other):
        """
        Return is self a subset of other.
        """
        return len(self) == len(self & other)

    def __lt__(self, other):
        """
        Return is self a proper subset of other.
        """
        return self <= other and self != other

    def __ge__(self, other):
        """
        Return is self a superset of other.
        """
        return len(other) == len(other & self)

    def __gt__(self, other):
        """
        Return is self a proper superset of other.
        """
        return self >= other and self != other

    def __len__(self):
        """
        Return number of elements in the set.
        """
        return sum(len(interval) for interval in self.intervals)

    def union(self, *others):
        """
        self | other_0 | other_1 | ...
        """
        copy = deepcopy(self)

        for other in others:
            copy |= other

        return copy

    def intersection(self, *others):
        """
        self & other_0 & other_1 & ...
        """
        copy = deepcopy(self)

        for other in others:
            copy &= other

        return copy

    def difference(self, *others):
        """
        self - other_0 - other_1 - ...
        """
        copy = deepcopy(self)

        for other in others:
            copy -= other

        return copy

    def symmetric_difference(self, other):
        copy = deepcopy(self)
        copy ^= other
        return copy

    def issubset(self, other):
        return self <= other

    def isdisjoint(self, other):
        """
        Return true if self has no common elements with other.
        """
        return len(self & other) == 0

    def issuperset(self, other):
        return self >= other

    def copy(self):
        return deepcopy(self)

    def update(self, *others):
        for other in others:
            self |= other
        return self

    def intersection_update(self, *others):
        for other in others:
            self &= other
        return self

    def difference_update(self, *others):
        for other in others:
            self -= other
        return self

    def symmetric_difference_update(self, other):
        self ^= other
        return self

    def add(self, element):
        self |= IntegerSet((element, element))

    def remove(self, element):
        if element not in self:
            raise KeyError
        self -= IntegerSet((element, element))

    def discard(self, element):
        self -= IntegerSet((element, element))

    def pop(self):
        if len(self) == 0:
            raise KeyError
        element = self.intervals[0].start
        self -= IntegerSet((element, element))
        return element

    def clear(self):
        self.intervals.clear()

    @staticmethod
    def _interval_sort_function(interval):
        return interval.start

    def _generate_overlaps(self, interval_1):
        """
        Yield every interval of self that overlaps with other interval.  The
        implementation takes advantage of the fact that the intervals are sorted
        to stop iteration at the first self interval that does not overlap with
        other interval.
        """
        idx = self.intervals.bisect_left(interval_1)
        yield from chain(
            self._generate_greater(interval_1, idx),
            self._generate_lesser(interval_1, idx),
        )

    def _generate_greater(self, interval_1, idx=None):
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

    def _generate_lesser(self, interval_1, idx=None):
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
