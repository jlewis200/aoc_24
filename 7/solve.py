#!/usr/bin/env python3

from re import fullmatch
import numpy as np


def solve(equations):
    total = 0

    for equation in equations:
        total += solve_equation(equation)

    return total


def solve_equation(equation):
    result, args = equation
    arg_0_set = {args.pop(0)}

    while len(args) > 0:
        arg_0_set_ = set()
        arg_1 = args.pop(0)

        for arg_0 in arg_0_set:
            arg_0_set_.add(arg_0 + arg_1)
            arg_0_set_.add(arg_0 * arg_1)

        arg_0_set = arg_0_set_

    return result if result in arg_0_set else 0


def parse(lines):
    parsed = []

    for line in lines:
        match = fullmatch("(?P<result>\d+): (?P<operands>.*)", line.strip())
        result = int(match.group("result"))
        operands = match.group("operands")
        operands = list(map(int, operands.split()))
        parsed.append((result, operands))

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 3749)
    main("input.txt")
