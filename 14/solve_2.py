#!/usr/bin/env python3

from re import fullmatch
from dataclasses import dataclass
from itertools import chain
from collections import deque
import numpy as np


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

    def adjacencies(self):
        for delta in (
            VectorTuple(1, 0),
            VectorTuple(-1, 0),
            VectorTuple(0, 1),
            VectorTuple(0, -1),
        ):
            yield self + delta

    def diagonals(self):
        for delta in (
            VectorTuple(1, 1),
            VectorTuple(-1, -1),
            VectorTuple(-1, 1),
            VectorTuple(1, -1),
        ):
            yield self + delta


@dataclass
class Robot:
    position: VectorTuple
    velocity: VectorTuple

    def step(self, board_size):
        self.position += self.velocity
        self.position %= board_size

    def __hash__(self):
        return hash(self.position) + hash(self.velocity)


def solve(robots, height, width):
    """
    Repeatedly step until over half of the robots are adjacent to another
    robot.
    """
    board_size = VectorTuple(height, width)
    step = 0
    most = len(robots) / 2  # over half seems like a good definition of "most"

    while get_total_contiguous(robots, board_size) < most:
        step += 1

        for robot in robots:
            robot.step(board_size)

        print(f"step:  {step}")

    print(str_board(get_board(robots, height, width)))
    return step


def get_total_contiguous(robots, board_size):
    """
    Find the number of contiguous robots (contiguous - 1 technically).
    """
    positions = {robot.position for robot in robots}
    contiguous_counts = []

    while len(positions) > 0:
        contiguous_counts.append(count_contiguous(positions, board_size))

    return sum(contiguous_counts)


def count_contiguous(positions, board_size):
    """
    BFS from an arbitrary starting robot.  If an adjacency is another robot
    position, increment the counter.
    """
    contiguous = 0
    queue = deque([positions.pop()])

    while len(queue) > 0:
        position = queue.popleft()

        for adjacency in position.adjacencies():
            adjacency %= board_size

            if adjacency in positions:
                positions.remove(adjacency)
                queue.append(adjacency)
                contiguous += 1

    return contiguous


def get_board(robots, height, width):
    board = np.full((height, width), " ")

    for robot in robots:
        board[robot.position] = "#"

    return board


def str_board(board):
    board_str = ""
    for row in board:
        for col in row:
            board_str += f"{col}"
        board_str += "\n"
    return board_str


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
    main("input.txt", 103, 101)
