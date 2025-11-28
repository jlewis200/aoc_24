#!/usr/bin/env python3

from collections import deque
import numpy as np
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import parse


def solve(grid):
    y_guard, x_guard = np.argwhere(grid == "^")[0]
    total = 0

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] in ("#", "^"):
                continue

            grid_ = grid.copy()
            grid_[y, x] = "#"

            if is_loop(grid_):
                total += 1

    return total


def is_loop(grid):
    coord = VectorTuple(map(int, np.argwhere(grid == "^")[0]))
    grid[coord] = "."
    positions = set((coord,))

    for direction in directions_generator():
        while True:
            delta = get_delta(direction)
            coord_ = coord + delta

            if not coord_.valid(grid):
                return False

            if obstruction_present(coord_, grid):
                break

            sequence = (coord, coord_)

            if sequence in positions:
                return True

            positions.add(sequence)
            coord = coord_


def obstruction_present(coord, grid):
    return grid[coord] == "#"


def get_delta(direction):
    match direction:

        case "u":
            return VectorTuple(-1, 0)
        case "r":
            return VectorTuple(0, 1)
        case "d":
            return VectorTuple(1, 0)
        case "l":
            return VectorTuple(0, -1)


def directions_generator():
    directions = ["u", "r", "d", "l"]
    directions = deque(directions)

    while True:
        direction = directions.popleft()
        directions.append(direction)
        yield direction


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 6)
    main("input.txt")
