#!/usr/bin/env python3

import numpy as np


def solve(locks, keys):
    """
    Add the lock and key together.  If no 2d arrray element is greater than 1,
    then no overlap exists.
    """
    total = 0

    for lock in locks:
        for key in keys:
            result = key + lock

            if result.max() <= 1:
                total += 1

    return total


def parse(data):
    """
    Keys/locks are treated as integer arrays to facillitate overlap comparisons.
    """
    locks = []
    keys = []

    for block in data.split("\n\n"):
        block = block.strip()
        lines = block.split("\n")
        array = np.array(list(list(line) for line in lines))

        # an array is a lock if every top element is "#"
        if (array[0] == "#").all():
            array = array == "#"
            locks.append(array.astype(int))

        # an array is a key if every bottom element is "#"
        elif (array[-1] == "#").all():
            array = array == "#"
            keys.append(array.astype(int))

    return locks, keys


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
