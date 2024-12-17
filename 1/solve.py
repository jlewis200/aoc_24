#!/usr/bin/env python3

from re import fullmatch
import numpy as np


def solve(list_0, list_1):
    list_0 = np.array(sorted(list_0))
    list_1 = np.array(sorted(list_1))
    return np.abs(list_0 - list_1).sum()


def parse(lines):
    list_0 = []
    list_1 = []

    for line in lines:
        match = fullmatch("(?P<number_0>\d+)\s+(?P<number_1>\d+)", line.strip())
        list_0.append(int(match.group("number_0")))
        list_1.append(int(match.group("number_1")))

    return list_0, list_1


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(*parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 11)
    main("input.txt")
