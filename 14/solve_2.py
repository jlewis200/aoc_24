#!/usr/bin/env python3

from re import fullmatch
from dataclasses import dataclass
from itertools import chain
from collections import deque
import numpy as np
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str


@dataclass
class Robot:
    position: VectorTuple
    velocity: VectorTuple

    def step(self, grid_size):
        self.position += self.velocity
        self.position %= grid_size

    def __hash__(self):
        return hash(self.position) + hash(self.velocity)


def solve(robots, height, width):
    """
    Repeatedly step until over half of the robots are adjacent to another
    robot.
    """
    grid_size = VectorTuple(height, width)
    step = 0
    most = len(robots) / 2  # over half seems like a good definition of "most"

    while get_total_contiguous(robots, grid_size) < most:
        step += 1

        for robot in robots:
            robot.step(grid_size)

        print(f"step:  {step}")

    print(grid_str(get_grid(robots, height, width)))
    return step


def get_total_contiguous(robots, grid_size):
    """
    Find the number of contiguous robots (contiguous - 1 technically).
    """
    positions = {robot.position for robot in robots}
    contiguous_counts = []

    while len(positions) > 0:
        contiguous_counts.append(count_contiguous(positions, grid_size))

    return sum(contiguous_counts)


def count_contiguous(positions, grid_size):
    """
    BFS from an arbitrary starting robot.  If an adjacency is another robot
    position, increment the counter.
    """
    contiguous = 0
    queue = deque([positions.pop()])

    while len(queue) > 0:
        position = queue.popleft()

        for adjacency in position.orthogonals(None):
            adjacency %= grid_size

            if adjacency in positions:
                positions.remove(adjacency)
                queue.append(adjacency)
                contiguous += 1

    return contiguous


def get_grid(robots, height, width):
    grid = np.full((height, width), " ")

    for robot in robots:
        grid[robot.position] = "#"

    return grid



def parse(lines):
    parsed = set()

    for line in lines:
        match = fullmatch(
            r"p=(?P<x>\d+),(?P<y>\d+) v=(?P<dx>.+),(?P<dy>.+)", line.strip()
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
