#!/usr/bin/env python3

import numpy as np


class VectorTuple(tuple):
    """
    This class replicates vectorized operations of numpy arrays, with the
    advantage that it's hashable.
    """

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

    def within_range(self, *ranges):
        return all(element in range_ for element, range_ in zip(self, ranges))


def solve(board):
    score = 0

    for coord in np.argwhere(board == 0):
        terminals = list()
        dfs(VectorTuple(coord), board, terminals)
        score += len(terminals)

    return score


def dfs(coord, board, terminals):
    if board[coord] == 9:
        terminals.append(coord)
        return

    for adjacency in adjacencies(coord, board):
        if board[adjacency] - board[coord] == 1:
            dfs(adjacency, board, terminals)


def adjacencies(coord, board):
    for delta in (
        VectorTuple((1, 0)),
        VectorTuple((-1, 0)),
        VectorTuple((0, 1)),
        VectorTuple((0, -1)),
    ):
        next_pos = coord + delta
        if next_pos.within_range(range(board.shape[0]), range(board.shape[1])):
            yield next_pos


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(list(map(int, line.strip())))

    return np.array(parsed)


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def main(filename, expected=None):
    result = solve(parse(read_file(filename)))
    print(result)
    if expected is not None:
        assert result == expected


if __name__ == "__main__":
    main("test_0.txt", 81)
    main("input.txt")
