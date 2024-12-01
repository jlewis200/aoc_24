#!/usr/bin/env python3

from re import fullmatch
from collections import defaultdict
import numpy as np


def solve(list_0, list_1):
    frequency = defaultdict(
        lambda: 0,
        zip(*np.unique(list_1, return_counts=True)),
    )
    similarity = 0

    for element in list_0:
        similarity += element * frequency[element]

    return similarity


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
    main("test.txt", 31)
    main("input.txt")
