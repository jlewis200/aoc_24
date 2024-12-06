#!/usr/bin/env python3

from collections import deque
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
    coord = Coord(*np.argwhere(board == "^")[0])
    board[coord.y, coord.x] = "."
    positions = {coord}

    for delta in delta_generator():

        while not obstructed(coord + delta, board):
            coord += delta
            positions.add(coord)

            if not valid_coord(coord + delta, board):
                return len(positions)


def obstructed(coord, board):
    return board[coord.y, coord.x] == "#"


def valid_coord(coord, board):
    return coord.x in range(board.shape[1]) and coord.y in range(board.shape[0])


def delta_generator():
    deltas = deque(
        [
            Coord(-1, 0),
            Coord(0, 1),
            Coord(1, 0),
            Coord(0, -1),
        ]
    )

    while True:
        delta = deltas.popleft()
        deltas.append(delta)
        yield delta


def parse(lines):
    parsed = []

    for line in lines:
        parsed.append(list(line.strip()))

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
    main("test_0.txt", 41)
    main("input.txt")
