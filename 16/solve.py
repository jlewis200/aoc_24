#!/usr/bin/env python3

import re
import math
import itertools
import numpy as np
import networkx as nx
from collections import deque
from aoc_data_structures import VectorTuple
from aoc_data_structures.grid_helpers import grid_str, parse


def solve(board):
    print(grid_str(board))
    pos = VectorTuple(*np.argwhere(board == "S"))
    min_cost = bfs(board, pos)
    return min_cost


def bfs(board, position):
    costs = {
        VectorTuple(1, 0): np.full_like(board, 2**32, dtype=int),
        VectorTuple(-1, 0): np.full_like(board, 2**32, dtype=int),
        VectorTuple(0, 1): np.full_like(board, 2**32, dtype=int),
        VectorTuple(0, -1): np.full_like(board, 2**32, dtype=int),
    }
    costs[VectorTuple(0, 1)][position] = 0
    queue = deque([(position, VectorTuple(0, 1))])

    while len(queue) > 0:
        position, delta = queue.popleft()

        for adjacency in position.orthogonals(board):
            if board[adjacency] == "#":
                continue

            if adjacency - position == delta:
                cost = costs[delta][position] + 1
            else:
                cost = costs[delta][position] + 1001

            if costs[adjacency - position][adjacency] > cost:
                costs[adjacency - position][adjacency] = cost
                queue.append((adjacency, adjacency - position))

    end = VectorTuple(*np.argwhere(board == "E"))
    return np.array(list(costs.values()))[:, end[0], end[1]].min()


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 7036)
    main("test_1.txt", 11048)
    main("input.txt")
