#!/usr/bin/env python3

from re import fullmatch
from dataclasses import dataclass
from collections import defaultdict
from math import prod


class VectorTuple(tuple):
    """
    This class replicates vectorized operations of numpy arrays, with the
    advantage that it's hashable.
    """

    def __new__(self, *args):
        if len(args) == 1 and not isinstance(args[0], tuple):
            args = args[0]
        return tuple.__new__(VectorTuple, args)

    def __add__(self, other):
        return VectorTuple(
            self_element + other_element
            for self_element, other_element in zip(self, other)
        )

    def __sub__(self, other):
        return VectorTuple(
            self_element - other_element
            for self_element, other_element in zip(self, other)
        )

    def __mul__(self, other):
        return VectorTuple(
            self_element * other_element
            for self_element, other_element in zip(self, other)
        )

    def __truediv__(self, other):
        return VectorTuple(
            self_element / other_element
            for self_element, other_element in zip(self, other)
        )

    def __mod__(self, other):
        return VectorTuple(
            self_element % other_element
            for self_element, other_element in zip(self, other)
        )

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))


@dataclass
class Robot:
    position: VectorTuple
    velocity: VectorTuple

    def __hash__(self):
        return hash(self.position) + hash(self.velocity)


def solve(robots, height, width):
    board_size = VectorTuple(height, width)

    for robot in robots:
        robot.position += robot.velocity * VectorTuple(100, 100)
        robot.position %= board_size

    return prod(get_quadrant_counts(robots, height, width))


def get_quadrant_counts(robots, height, width):
    quadrants = get_quadrants(height, width)
    quadrant_counts = defaultdict(lambda: 0)

    for robot in robots:
        for idx, quadrant in enumerate(quadrants):
            if robot.position.within_range(*quadrant):
                quadrant_counts[idx] += 1
                break

    return tuple(quadrant_counts.values())


def get_quadrants(height, width):
    y_mid = height // 2
    x_mid = width // 2
    return (
        (range(0, y_mid), range(0, x_mid)),
        (range(y_mid + 1, height), range(0, x_mid)),
        (range(0, y_mid), range(x_mid + 1, width)),
        (range(y_mid + 1, height), range(x_mid + 1, width)),
    )


def parse(lines):
    parsed = set()

    for line in lines:
        match = fullmatch(
            "p=(?P<x>\d+),(?P<y>\d+) v=(?P<dx>.+),(?P<dy>.+)", line.strip()
        )
        parsed.add(
            Robot(
                VectorTuple(
                    int(match.group("y")),
                    int(match.group("x")),
                ),
                VectorTuple(
                    int(match.group("dy")),
                    int(match.group("dx")),
                ),
            )
        )

    return parsed


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, height, width, expected=None):
    result = solve(parse(read_file(filename)), height, width)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 7, 11, 12)
    main("input.txt", 103, 101)
