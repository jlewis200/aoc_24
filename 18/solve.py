#!/usr/bin/env python3

from collections import deque
from aoc_data_structures import VectorTuple


def solve(coords, size, steps):
    """
    BFS to find shortest unweighted path length.
    """
    target = VectorTuple(size, size)
    coords = set(coords[:steps])
    position = VectorTuple(0, 0)
    queue = deque([(position, 0)])
    visited = set()

    while len(queue) > 0 and position != target:
        position, step = queue.popleft()

        for adjacency in position.orthogonals(size + 1):
            if adjacency not in coords and adjacency not in visited:
                queue.append((adjacency, step + 1))
                visited.add(adjacency)

    return step


def parse(lines):
    coords = []

    for line in lines:
        coords.append(VectorTuple(*map(int, line.strip().split(","))))

    return coords


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, size, steps, expected=None):
    result = solve(parse(read_file(filename)), size, steps)
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 6, 12, 22)
    main("input.txt", 70, 1024)
