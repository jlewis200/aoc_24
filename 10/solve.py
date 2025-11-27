#!/usr/bin/env python3

import numpy as np
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import parse


def solve(grid):
    score = 0

    for coord in np.argwhere(grid == 0):
        terminals = set()
        dfs(VectorTuple(coord), grid, terminals)
        score += len(terminals)

    return score


def dfs(coord, grid, terminals):
    if grid[coord] == 9:
        terminals.add(coord)
        return

    for adjacency in coord.orthogonals(grid):
        if grid[adjacency] - grid[coord] == 1:
            dfs(adjacency, grid, terminals)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)).astype(int))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 36)
    main("input.txt")
