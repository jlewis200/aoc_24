#!/usr/bin/env python3

from collections import deque
import numpy as np
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import parse


def solve(grid):
    coord = VectorTuple(*np.argwhere(grid == "^")[0])
    grid[coord] = "."
    positions = {coord}

    for delta in delta_generator():

        while not obstructed(coord + delta, grid):
            coord += delta
            positions.add(coord)

            if not (coord + delta).valid(grid):
                return len(positions)


def obstructed(coord, grid):
    return grid[coord] == "#"


def delta_generator():
    deltas = deque(
        [
            VectorTuple(-1, 0),
            VectorTuple(0, 1),
            VectorTuple(1, 0),
            VectorTuple(0, -1),
        ]
    )

    while True:
        delta = deltas.popleft()
        deltas.append(delta)
        yield delta


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 41)
    main("input.txt")
