#!/usr/bin/env python3

import numpy as np


class Coord:

    def __init__(self, y, x):
        self.y = int(y)
        self.x = int(x)
        self._hash = None

    def __add__(self, other):
        return Coord(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Coord(self.y - other.y, self.x - other.x)

    def __mul__(self, other):
        return Coord(self.y * other, self.x * other)

    def __hash__(self):
        if self._hash is None:
            self._hash = (1000003 * self.x) ^ self.y
        return self._hash

    def __eq__(self, other):
        if not isinstance(other, Coord):
            return False
        return self.y == other.y and self.x == other.x

    def __repr__(self):
        return f"{self.y}\t{self.x}"


def solve(board):
    score = 0

    for coord in np.argwhere(board == 0):
        terminals = list()
        dfs(Coord(*coord), board, terminals)
        score += len(terminals)

    return score


def dfs(coord, board, terminals):
    if board[coord.y, coord.x] == 9:
        terminals.append(coord)
        return

    for adjacency in adjacencies(coord, board):
        if board[adjacency.y, adjacency.x] - board[coord.y, coord.x] == 1:
            dfs(adjacency, board, terminals)


def adjacencies(coord, board):
    for delta in (
        Coord(1, 0),
        Coord(-1, 0),
        Coord(0, 1),
        Coord(0, -1),
    ):
        next_pos = coord + delta
        if valid(next_pos, board):
            yield next_pos


def valid(coord, board):
    return coord.y in range(board.shape[0]) and coord.x in range(board.shape[1])


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
