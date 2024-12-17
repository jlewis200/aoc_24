#!/usr/bin/env python3

from re import findall
from math import prod


def solve(pairs):
    return sum(prod(pair) for pair in pairs)


def parse(data):
    parsed = []

    for match in findall("mul\((\d{1,3}),(\d{1,3})\)", data):
        parsed.append(tuple(map(int, match)))

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.read()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test.txt", 161)
    main("input.txt")
