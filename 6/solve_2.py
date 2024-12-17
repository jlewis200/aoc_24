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
    y_guard, x_guard = np.argwhere(board == "^")[0]
    total = 0

    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            if (y == y_guard and x == x_guard) or board[y, x] == "#":
                continue

            board_ = board.copy()
            board_[y, x] = "#"

            if is_loop(board_):
                total += 1

    return total


def is_loop(board):
    coord = Coord(*np.argwhere(board == "^")[0])
    board[coord.y, coord.x] = "."
    positions = set((coord,))

    for direction in directions_generator():
        while True:
            delta = get_delta(direction)
            coord_ = coord + delta

            if not valid_coord(coord_, board):
                return False

            if obstruction_present(coord_, board):
                break

            sequence = (coord, coord_)

            if sequence in positions:
                return True

            positions.add(sequence)
            coord = coord_


def obstruction_present(coord, board):
    return board[coord.y, coord.x] == "#"


def valid_coord(coord, board):
    return coord.x in range(board.shape[1]) and coord.y in range(board.shape[0])


def get_delta(direction):
    match direction:

        case "u":
            return Coord(-1, 0)

        case "r":
            return Coord(0, 1)
        case "d":
            return Coord(1, 0)
        case "l":
            return Coord(0, -1)


def directions_generator():
    directions = ["u", "r", "d", "l"]
    directions = deque(directions)

    while True:
        direction = directions.popleft()
        directions.append(direction)
        yield direction


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
    main("test_0.txt", 6)
    main("input.txt")
