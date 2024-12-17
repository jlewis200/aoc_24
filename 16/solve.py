#!/usr/bin/env python3

import re
import math
import itertools
import numpy as np
import networkx as nx
from collections import deque


class VectorTuple(tuple):
    """
    This class replicates vectorized operations of numpy arrays, with the
    advantage that it's hashable.
    """

    def __new__(cls, *args):
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

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))

    def orthogonals(self, board):
        """
        Generate E, N, W, S adjacencies.
        """
        for delta in (
            VectorTuple(0, 1),
            VectorTuple(-1, 0),
            VectorTuple(0, -1),
            VectorTuple(1, 0),
        ):
            next_pos = self + delta
            if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
                yield next_pos


def solve(board):
    print(board_str(board))
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


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


def parse(lines):
    board = []

    for line in lines:
        board.append(list(line.strip()))

    return np.array(board)


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
