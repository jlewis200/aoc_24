#!/usr/bin/env python3

from re import fullmatch
from collections import deque


def solve(equations):
    return sum(solve_equation(equation) for equation in equations)


def solve_equation(equation):
    """
    Enumerate every possible sequence of operations.  Return the target result
    if it's in the set of possible results.
    """
    result, right_operands = equation
    left_operands = {right_operands.popleft()}

    while len(right_operands) > 0:
        left_operands = get_operation_results(left_operands, right_operands.popleft())

    return result if result in left_operands else 0


def get_operation_results(left_operands, right_operand):
    """
    Perform each operation between every left operand and the provided
    right_operand.
    """
    next_left_operands = set()

    for left_operand in left_operands:
        next_left_operands.add(left_operand + right_operand)
        next_left_operands.add(left_operand * right_operand)

    return next_left_operands


def parse(lines):
    parsed = []

    for line in lines:
        match = fullmatch("(?P<result>\d+): (?P<operands>.*)", line.strip())
        result = int(match.group("result"))
        operands = match.group("operands")
        operands = deque(map(int, operands.split()))
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
