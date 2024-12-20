#!/usr/bin/env python3

from itertools import product
from collections import deque, defaultdict
import numpy as np


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

    def __mod__(self, other):
        return VectorTuple(
            self_element % other_element
            for self_element, other_element in zip(self, other)
        )

    def __abs__(self):
        return VectorTuple((abs(element) for element in self))

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

    def radius(self, board, size):
        """
        Generate coordinates within a manhattan radius.
        """
        for dx, dy in product(range(-size, size + 1), repeat=2):
            delta = VectorTuple(dy, dx)
            adjacency = self + delta

            if (
                delta == VectorTuple(0, 0)
                or delta.manhattan() > size
                or not adjacency.within_range(
                    range(board.shape[0]),
                    range(board.shape[1]),
                )
            ):
                continue

            yield adjacency

    def manhattan(self):
        """
        Get manhattan magnitude of self.
        """
        return sum(abs(self))


def solve(board, max_cheat_distance, threshold):
    """
    Find total number of cheats exceeding the threshold.
    """
    distances = get_distances(board)
    cheats = get_cheats(distances, board, max_cheat_distance, threshold)
    cheat_set = set()

    for cheat_list in cheats.values():
        cheat_set |= set(cheat_list)

    return len(cheat_set)


def get_cheats(distances, board, max_cheat_distance, threshold):
    """
    Get a dictionary mapping cheat lengths to a set of cheat tuple pairs.  Only
    cheats meeting/exceeding the threshold are included.
    """
    cheats = defaultdict(lambda: set())

    for position, distance in distances.items():
        for adjacency in position.radius(board, max_cheat_distance):
            if board[adjacency] == "#":
                continue

            cheat_distance = distances[adjacency] - distances[position]
            cheat_distance -= (adjacency - position).manhattan()

            if cheat_distance >= threshold:
                cheats[cheat_distance].add((position, adjacency))

    return cheats


def get_distances(board):
    """
    Get a dictionary mapping tuple locations to distance from the start.
    """
    distances = {}
    start = VectorTuple(*np.argwhere(board == "S"))
    queue = deque([(start, 0)])

    while len(queue) > 0:
        position, distance = queue.popleft()

        if position in distances or board[position] == "#":
            continue

        distances[position] = distance

        for adjacency in position.orthogonals(board):
            queue.append((adjacency, distance + 1))

    return distances


def parse(lines):
    board = []

    for line in lines:
        board.append(list(line.strip()))

    return np.array(board)


def board_str(board):
    """
    Return the string representation of a numpy array where each element can be
    represented as a single character.
    """
    return "\n".join("".join(row) for row in board)


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
