#!/usr/bin/env python3

import numpy as np
from itertools import product


def solve(locks, keys):
    """
    Add the 2d arrays of lock and key together.  If no element is greater than
    1, then no overlap exists.
    """
    total = 0

    for lock, key in product(locks, keys):
        if (key + lock).max() <= 1:
            total += 1

    return total


def parse(data):
    """
    Keys/locks are treated as integer arrays to facillitate overlap comparisons.

    An array is a lock if every top element is "#" (mapped to 1), and a key if
    every bottom element is "#" (mapped to 1).
    """
    locks = []
    keys = []

    for array in parse_arrays(data):
        if (array[0] == 1).all():
            locks.append(array)

        elif (array[-1] == 1).all():
            keys.append(array)

    return locks, keys


def parse_arrays(data):
    """
    Parse input data into numpy arrays mapping "#" to 1 and "." to 0.
    """
    arrays = []

    for block in data.split("\n\n"):
        block = block.strip()
        lines = block.split("\n")
        array = np.array(list(map(list, lines)))
        arrays.append((array == "#").astype(int))

    return arrays


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 3)
    main("input.txt")
