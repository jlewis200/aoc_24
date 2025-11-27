#!/usr/bin/env python3

from itertools import product
from collections import deque, defaultdict
import numpy as np
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str, parse


def solve(grid, max_cheat_distance, threshold):
    """
    Find total number of cheats exceeding the threshold.
    """
    distances = get_distances(grid)
    cheats = get_cheats(distances, grid, max_cheat_distance, threshold)
    cheat_set = set()

    for cheat_list in cheats.values():
        cheat_set |= set(cheat_list)

    return len(cheat_set)


def get_cheats(distances, grid, max_cheat_distance, threshold):
    """
    Get a dictionary mapping cheat lengths to a set of cheat tuple pairs.  Only
    cheats meeting/exceeding the threshold are included.
    """
    cheats = defaultdict(lambda: set())

    for position, distance in distances.items():
        for adjacency in position.radius(grid, max_cheat_distance):
            if grid[adjacency] == "#":
                continue

            cheat_distance = distances[adjacency] - distances[position]
            cheat_distance -= (adjacency - position).manhattan()

            if cheat_distance >= threshold:
                cheats[cheat_distance].add((position, adjacency))

    return cheats


def get_distances(grid):
    """
    Get a dictionary mapping tuple locations to distance from the start.
    """
    distances = {}
    start = VectorTuple(*np.argwhere(grid == "S"))
    queue = deque([(start, 0)])

    while len(queue) > 0:
        position, distance = queue.popleft()

        if position in distances or grid[position] == "#":
            continue

        distances[position] = distance

        for adjacency in position.orthogonals(grid):
            queue.append((adjacency, distance + 1))

    return distances


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, max_cheat_distance, threshold, expected=None):
    """
    Runtime around 1.5 minutes

    $time ./solve.py
    14
    2492
    1521
    1013106

    real	1m19.160s
    user	1m19.114s
    sys	0m0.974s
    """
    result = solve(parse(read_file(filename)), max_cheat_distance, threshold)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 2, 8, 14)
    main("test_0.txt", 20, 8, 2492)
    main("input.txt", 2, 100)
    main("input.txt", 20, 100)
