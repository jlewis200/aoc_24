#!/usr/bin/env python3

import re
from math import prod
import numpy as np


def solve(data):
    pairs = []
    enabled = True

    for pair in data:

        match pair:

            case "do()":
                enabled = True

            case "don't()":
                enabled = False

            case _:

                if enabled:
                    pairs.append(pair)

    return sum(prod(pair) for pair in pairs)


def parse(data):
    parsed = []

    for match in re.findall("mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", data):

        if match.startswith("mul"):
            match = re.fullmatch("mul\((\d{1,3}),(\d{1,3})\)", match)
            match = tuple(map(int, match.groups()))

        parsed.append(match)

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
    main("test_1.txt", 48)
    main("input.txt")
